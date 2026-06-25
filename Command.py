import sys
from abc import ABC, abstractmethod

class Pessoa:
    def __init__(self, id_pessoa: int, nome: str):
        self.id = id_pessoa
        self.nome = nome


class Command(ABC):
    @abstractmethod
    def execute(self, args: list, db: dict):
        pass

class NewCommand(Command):
    def execute(self, args: list, db: dict):
        if len(args) < 2:
            print("Erro: Comando 'new' requer ID e nome.")
            return
        id_pessoa = int(args[1])
        nome = " ".join(args[2:])
        db[id_pessoa] = Pessoa(id_pessoa, nome)
        print(f"Pessoa criada: ID={id_pessoa}, Nome={nome}")

class DeleteCommand(Command):
    def execute(self, args: list, db: dict):
        if len(args) < 2:
            print("Erro: Comando 'delete' requer ID.")
            return
        id_pessoa = int(args[1])
        if id_pessoa in db:
            del db[id_pessoa]
            print(f"Pessoa com ID={id_pessoa} deletada.")
        else:
            print(f"Erro: Pessoa com ID={id_pessoa} não encontrada.")

class GetCommand(Command):
    def execute(self, args: list, db: dict):
        if len(args) < 2:
            print("Erro: Comando 'get' requer ID.")
            return
        id_pessoa = int(args[1])
        pessoa = db.get(id_pessoa)
        if pessoa:
           print(f"ID: {pessoa.id} | Nome: {pessoa.nome}")
        else:
            print(f"Erro: Pessoa com ID={id_pessoa} não encontrada.")


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]

    db = {}
    commands = {
        "new": NewCommand(),
        "delete": DeleteCommand(),
        "get": GetCommand(),
    }

    if not argv or argv[0] in {"-h", "--help", "help"}:
        print("Uso:")
        print("  python Command.py new <id> <nome>")
        print("  python Command.py delete <id>")
        print("  python Command.py get <id>")
        return 0

    command_name = argv[0].lower()
    command = commands.get(command_name)

    if command is None:
        print(f"Erro: comando '{command_name}' desconhecido.")
        print("Use --help para ver os comandos disponíveis.")
        return 1

    try:
        command.execute(argv, db)
    except ValueError:
        print("Erro: ID deve ser um número inteiro.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

