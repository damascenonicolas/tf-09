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

class Atalho(Item):
    __slots__ = ["__destino"]

    def __init__(self, nome, destino, pai=None):
        self.__destino = None
        super().__init__(nome, pai)
        self.redirecionar(destino)

    @property
    def destino(self):
        return self.__destino

    def redirecionar(self, novo_destino):
        if novo_destino == self:
            raise ValueError("Um atalho nao pode apontar para si mesmo")
        
        verificador = self.pai
        while verificador is not None:
            if verificador == novo_destino:
                raise ValueError("Um atalho nao pode apontar para uma pasta ancestral")
            verificador = verificador.pai

        self.__destino = novo_destino

    def tamanho(self):
        return 1

    def mostrar(self, recuo=""):
        print(f"{recuo}{self.nome} -> {self.__destino.caminho()}")

raiz = Pasta("C:")
users = Pasta("Users", raiz)
usuario = Pasta("damascenonicolas", users)
desktop = Pasta("Desktop", usuario)

arquivo_texto = Arquivo("documento.txt", 500, desktop)
pasta_projetos = Pasta("Projetos", desktop)
arquivo_codigo = Arquivo("main.py", 1200, pasta_projetos)

atalho_documento = Atalho("atalho_doc", arquivo_texto, desktop)
atalho_pasta = Atalho("atalho_projeto", pasta_projetos, desktop)

print("--- ARVORE COMPLETA ---")
raiz.mostrar()

print("\n--- ESPACO TOTAL ---")
lista_itens = [arquivo_texto, desktop, Lixeira()]
print(f"Espaco Total calculado: {espaco_total(lista_itens)} bytes")

print("\n--- TENTATIVAS DE FALHA ---")
tentar(lambda: setattr(atalho_documento, "destino", arquivo_codigo))
tentar(lambda: atalho_documento.redirecionar(atalho_documento))
tentar(lambda: atalho_documento.redirecionar(desktop))
