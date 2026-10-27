from abc import ABC, abstractmethod

class Medivel(ABC):
    @abstractmethod
    def tamanho(self):
        pass

class Item(Medivel):
    __slots__ = ["nome", "pai"]

    def __init__(self, nome, pai=None):
        self.nome = nome
        self.pai = pai
        if pai is None:
            return
        pai.adicionar(self)

    def mover_para(self, novo_pai):
        if self.pai is not None:
            self.pai.remover(self)
        self.pai = novo_pai
        if novo_pai is None:
            return
        novo_pai.adicionar(self)

    def caminho(self):
        if self.pai is None:
            return self.nome
        return f"{self.pai.caminho()}/{self.nome}"

class Arquivo(Item):
    __slots__ = ["__tamanho"]

    def __init__(self, nome, tamanho_bytes, pai=None):
        self.__tamanho = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        return self.__tamanho

    def mostrar(self, recuo=""):
        print(f"{recuo}{self.nome} ({self.tamanho()} bytes)")

class Pasta(Item):
    __slots__ = ["filhos"]

    def __init__(self, nome, pai=None):
        self.filhos = []
        super().__init__(nome, pai)

    def adicionar(self, item):
        self.filhos.append(item)

    def remover(self, item):
        self.filhos.remove(item)

    def tamanho(self):
        total = 0
        for filho in self.filhos:
            total = total + filho.tamanho()
        return total

    def mostrar(self, recuo=""):
        print(f"{recuo}[{self.nome}]")
        for child in self.filhos:
            child.mostrar(recuo + "  ")

class Lixeira(Item):
    __slots__ = ["filhos"]

    def __init__(self, nome="Lixeira", pai=None):
        self.filhos = []
        super().__init__(nome, pai)

    def adicionar(self, item):
        self.filhos.append(item)

    def tamanho(self):
        total = 0
        for filho in self.filhos:
            total = total + filho.tamanho()
        return total

    def mostrar(self, recuo=""):
        print(f"{recuo}{self.nome} ({self.tamanho()} bytes em arquivos deletados)")

def espaco_total(itens):
    total = 0
    for item in itens:
        total = total + item.tamanho()
    return total

def tentar(funcao):
    try:
        funcao()
    except Exception as erro:
        print(f"Erro: {erro}")
