from collections import deque


# Classe que representa o historico do Git como um grafo dirigido aciclico,
# guardando commits, mensagens e branches em dicionarios e contando os passos de cada operacao.
class MiniGit:
    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__contador",
        "__passos",
    )

    # Inicializa o repositorio vazio com a branch main sem apontar para nenhum commit (0 passos).
    def __init__(self):
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    # Devolve a quantidade de passos gastos pela ultima operacao realizada.
    @property
    def passos(self):
        return self.__passos

    # Cria um novo commit filho do commit da branch atual e avanca o ponteiro da branch (2 passos).
    def commitar(self, mensagem):
        if not mensagem:
            raise ValueError("A mensagem do commit nao pode ser vazia")
        self.__contador += 1
        identificador = f"c{self.__contador}"
        commit_anterior = self.__branches[self.__branch_atual]
        lista_pais = []
        if commit_anterior is not None:
            lista_pais.append(commit_anterior)
        self.__pais[identificador] = lista_pais
        self.__mensagens[identificador] = mensagem
        self.__branches[self.__branch_atual] = identificador
        self.__passos = 2
        return identificador

    # Consulta e devolve a mensagem associada a um commit pelo seu identificador (1 passo).
    def mensagem(self, commit):
        if commit not in self.__mensagens:
            raise ValueError(f"Commit inexistente: {commit}")
        self.__passos = 1
        return self.__mensagens[commit]

    # Devolve uma tupla com os identificadores dos pais de um commit (1 passo).
    def pais(self, commit):
        if commit not in self.__pais:
            raise ValueError(f"Commit inexistente: {commit}")
        self.__passos = 1
        return tuple(self.__pais[commit])

