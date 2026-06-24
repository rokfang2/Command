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

