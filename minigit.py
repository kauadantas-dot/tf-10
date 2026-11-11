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

    # Devolve o nome da branch em que o repositorio esta posicionado no momento.
    @property
    def branch_atual(self):
        return self.__branch_atual

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

    # Cria uma nova branch apontando para o commit atual da branch ativa (1 passo).
    def criar_branch(self, nome):
        if nome in self.__branches:
            raise ValueError(f"A branch ja existe: {nome}")
        if self.__branches[self.__branch_atual] is None:
            raise ValueError("Ainda nao ha commits para criar uma branch")
        self.__branches[nome] = self.__branches[self.__branch_atual]
        self.__passos = 1

    # Muda a branch ativa para a branch informada (1 passo).
    def trocar_branch(self, nome):
        if nome not in self.__branches:
            raise ValueError(f"Branch inexistente: {nome}")
        self.__branch_atual = nome
        self.__passos = 1

    # Cria um commit de uniao com dois pais na branch atual e avanca seu ponteiro (2 passos).
    def mesclar(self, nome):
        if nome not in self.__branches:
            raise ValueError(f"Branch inexistente: {nome}")
        if nome == self.__branch_atual:
            raise ValueError("Nao e possivel mesclar uma branch com ela mesma")
        self.__contador += 1
        identificador = f"c{self.__contador}"
        commit_atual = self.__branches[self.__branch_atual]
        commit_origem = self.__branches[nome]
        self.__pais[identificador] = [commit_atual, commit_origem]
        self.__mensagens[identificador] = f"merge de {nome}"
        self.__branches[self.__branch_atual] = identificador
        self.__passos = 2
        return identificador

