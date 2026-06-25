import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from Command import DeleteCommand, GetCommand, NewCommand, main


class CommandTests(unittest.TestCase):

    def run_with_stdout(self, func, *args, **kwargs):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = func(*args, **kwargs)

        output = buffer.getvalue()

        # Exibe no terminal o que o programa imprimiu
        if output:
            print(output, end="")

        return result, output

    def run_script(self, *args):
        script_path = Path(__file__).resolve().parent / "Command.py"
        completed = subprocess.run(
            [sys.executable, str(script_path), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode, completed.stdout, completed.stderr

    def test_no_arguments(self):
        print("\nTESTE: Ajuda")
        result, output = self.run_with_stdout(main, [])

        self.assertEqual(result, 0)
        self.assertIn("Uso:", output)

    def test_unknown_command(self):
        print("\nTESTE: Comando inválido")
        result, output = self.run_with_stdout(main, ["update", "1"])

        self.assertEqual(result, 1)
        self.assertIn("comando 'update' desconhecido", output)

    def test_new_command(self):
        print("\nTESTE: Criar pessoa")

        db = {}
        command = NewCommand()

        result, output = self.run_with_stdout(
            command.execute,
            ["new", "1", "Ana", "Silva"],
            db
        )

        print(f"Pessoa armazenada -> ID={db[1].id}, Nome={db[1].nome}")

        self.assertIsNone(result)
        self.assertIn("Pessoa criada", output)

    def test_id_and_name(self):
        print("\nTESTE: Criar pessoa sem argumentos")

        db = {}
        command = NewCommand()

        result, output = self.run_with_stdout(command.execute, ["new"], db)

        self.assertEqual(db, {})
        self.assertIn("Comando 'new' requer ID e nome", output)

    def test_finds_person(self):
        print("\nTESTE: Buscar pessoa")

        db = {
            1: type("PessoaFake", (), {
                "id": 1,
                "nome": "Ana Silva"
            })()
        }

        command = GetCommand()

        result, output = self.run_with_stdout(command.execute, ["get", "1"], db)

        print(f"Pessoa encontrada -> {db[1].nome}")

        self.assertIn("ID: 1 | Nome: Ana Silva", output)

    def test_missing_person(self):
        print("\nTESTE: Pessoa inexistente")

        db = {}
        command = GetCommand()

        result, output = self.run_with_stdout(command.execute, ["get", "1"], db)

        self.assertIn("Pessoa com ID=1 não encontrada", output)

    def test_requires_id(self):
        print("\nTESTE: Buscar sem ID")

        db = {}
        command = GetCommand()

        result, output = self.run_with_stdout(command.execute, ["get"], db)

        self.assertIn("Comando 'get' requer ID", output)

    def test_removes_person(self):
        print("\nTESTE: Deletar pessoa")

        db = {
            1: type("PessoaFake", (), {
                "id": 1,
                "nome": "Ana Silva"
            })()
        }

        command = DeleteCommand()

        result, output = self.run_with_stdout(command.execute, ["delete", "1"], db)

        print("Pessoa removida do banco.")

        self.assertNotIn(1, db)
        self.assertIn("Pessoa com ID=1 deletada.", output)

    def test_delete_missing_person(self):
        print("\nTESTE: Deletar pessoa inexistente")

        db = {}
        command = DeleteCommand()

        result, output = self.run_with_stdout(command.execute, ["delete", "1"], db)

        self.assertIn("Pessoa com ID=1 não encontrada", output)

    def test_delete_id(self):
        print("\nTESTE: Deletar sem ID")

        db = {}
        command = DeleteCommand()

        result, output = self.run_with_stdout(command.execute, ["delete"], db)

        self.assertIn("Comando 'delete' requer ID", output)

    def test_invalid_id(self):
        print("\nTESTE: ID inválido")

        result, output = self.run_with_stdout(main, ["get", "abc"])

        self.assertEqual(result, 1)
        self.assertIn("ID deve ser um número inteiro", output)

    def test_created_person(self):
        print("\nTESTE CLI: Criar pessoa")

        returncode, stdout, stderr = self.run_script("new", "1", "Ana", "Silva")

        print(stdout)

        self.assertEqual(returncode, 0)
        self.assertEqual(stderr, "")

    def test_prints_usage(self):
        print("\nTESTE CLI: Ajuda")

        returncode, stdout, stderr = self.run_script("--help")

        print(stdout)

        self.assertEqual(returncode, 0)
        self.assertEqual(stderr, "")


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False)