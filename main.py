# EQUIPE: Ana Laura Schoffen Rodrigues e Bruno Fusieger Santana
# RAs: 115456 e 112646
from typing import List, Dict
from collections import deque
from random import choice, random


class Vertice:
    """
    Representa um vértice de um grafo com um número, uma lista de adjacências,
    uma valor de distância, uma flag de visitado, um atributo pai, um posto e um rank
    """

    def __init__(self, num: int) -> None:
        """
        Cria um novo vértice com o número num e com uma lista de adjacências vazia.
        E também cria:
            d: um número distance que é usado durante o BFS
            visitado: 'cor' do vértice usado no BFS
            pai: vértice pai usado no BFS
            post: um posto usado no mst-kruskal
            rank: ranking usado no mst-kruskal

        Em geral este construtor não é chamado diretamente mas é chamado pelo
        construtor da classe Grafo.
        """
        self.num = num
        self.visitado = False
        self.pai = None
        self.d = None
        self.adj: List[Vertice] = []

        self.p = self
        self.rank = 0

    def __str__(self) -> str:
        return "Vertice(%d)" % self.num


class Grafo:
    """
    Representa um grafo não orientado por meio de uma lista de adjacências
    """

    def __init__(self, n: int) -> None:
        """
        Cria um novo grafo com n vértices com os números 0, 1, ..., n-1.
        Também registra o numero de vértices e arrestas do grafo
        Cria um dicionário para guardar os pesos das arestas
        """
        self.vertices = [Vertice(i) for i in range(n)]
        self.num_arrestas = 0
        self.num_vertices = n
        self.pesos = dict()

    def addAresta(self, u: int, v: int, peso=None):
        """
        Adiciona a aresta (u, v) ao grafo.

        u e v precisam ser vértices válidos, isto é precisam ser um valor
        entre 0 e n - 1, onde n é a quantidade de vértices do grafo.

        Se um terceiro argumento por passado, ele é interpretado como peso e registrado no dicionário de pesos

        Este método não verifica se a aresta (u, v) já existe no grafo.
        """
        self.num_arrestas += 1
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])

        if peso:
            self.pesos[tuple(sorted((u, v)))] = peso

    def bfs(self, v: int):
        """
        Função BFS básica que calcula as distâncias relativas ao vértice v
        Assume-se que v é um vértice válido no grafo.
        """
        for x in self.vertices:
            x.visitado = False
            x.d = None
            x.pai = None

        q = deque(maxlen=self.num_vertices)

        self.vertices[v].d = 0
        self.vertices[v].visitado = True

        q.append(self.vertices[v])

        while not len(q) == 0:
            node: Vertice = q.popleft()
            for vertex in node.adj:
                if not vertex.visitado:
                    vertex.d = node.d + 1
                    vertex.pai = node
                    vertex.visitado = True

                    q.append(vertex)

def vertice_mais_distante(g: Grafo, v: int) -> int:
    """
    Usa a função BFS para calcular o vértice acessível com distância máxima no grafo g em
    relação ao vértice v.
    Assume-se que v sempre está no grafo g
    Retorna o número do vértice acessível com distância máxima em relação à v
    """

    g.bfs(v)
    maior: Vertice = g.vertices[v]
    for v in g.vertices:
        if v.d and v.d > maior.d:
            maior = v

    return maior.num

def verificar_arvore(g: Grafo) -> bool:
    """
    Verifica se um grafo é uma árvore, usando o BFS
    Retorna True se o grafo é uma árvore, False caso contrário
    Usamos a definição de que qualquer grafo conexo com n vértices e n - 1 arestas é uma árvore
    """

    if g.num_arrestas != g.num_vertices - 1:
        return False

    g.bfs(0)

    for v in g.vertices:
        if not v.visitado:
            return False

    return True


def diameter(g: Grafo) -> int:
    """
    Calcula o diametro da árvore g.
    O diametro é a maior distância entre dois nós folha.
    Assume-se que g é uma árvore válida
    Caso o grafo g não seja uma árvore o retorno dessa função é imprevisível
    """

    vertex_a = vertice_mais_distante(g, 0)

    vertex_b = vertice_mais_distante(g, vertex_a)

    return g.vertices[vertex_b].d


def random_tree_random_walk(n: int) -> Grafo:
    """
    Gera uma árvore com n vértices usando o algoritmo de passeio aleatório e retorna a respectiva árvore
    """
    g = Grafo(n)
    for v in g.vertices:
        v.pai = None
        v.d = None
        v.visitado = False
    u = g.vertices[0]
    u.visitado = True

    while g.num_arrestas < n - 1:
        v = choice(g.vertices)
        if not v.visitado:
            g.addAresta(u.num, v.num)
            v.visitado = True
        u = v
    return g


def make_set(v: Vertice):
    """
    Faz do vértice o seu próprio conjunto
    Função relacionada ao algoritmo de kruskal
    """
    v.p = v
    v.rank = 0


def find_set(v: Vertice) -> Vertice:
    """
    Procura a raiz da árvore de conjunto
    Função relacionada ao algoritmo de kruskal
    """
    if v != v.p:
        v.p = find_set(v.p)
    return v.p


def union(x: Vertice, y: Vertice):
    """
    Faz a união de dois conjuntos disjuntos
    Função relacionada ao algoritmo de kruskal
    """
    link(find_set(x), find_set(y))


def link(x: Vertice, y: Vertice):
    """
    Une o vértice raiz com menor rank ao vértice com maior rank
    Função relacionada ao algoritmo de kruskal
    """
    if x.rank > y.rank:
        y.p = x
    else:
        x.p = y
        if x.rank == y.rank:
            y.rank += 1


def mst_kruskal(g: Grafo) -> Grafo:
    """
    A partir de um grafo com arrestas com peso, constrói uma árvore geradora mínima
    """
    arvore = Grafo(g.num_vertices)

    for vertex in g.vertices:
        make_set(vertex)

    ordenado = sorted(g.pesos, key=g.pesos.get)

    for (u, v) in ordenado:
        if find_set(g.vertices[u]) != find_set(g.vertices[v]):
            arvore.addAresta(u, v)
            union(g.vertices[u], g.vertices[v])

    return arvore


def random_tree_kruskal(n: int) -> Grafo:
    """
    Gera um grafo completo com n vértices e pesos aleatórios para as arrestas e
    executa o algoritmo de kruskal para criar uma árvore geradora mínima do grafo.
    """
    g = Grafo(n)
    for u in range(0, n):
        for v in range(u + 1, n):
            g.addAresta(u, v, random())

    tree = mst_kruskal(g)

    return tree


def main():
    """
    Executa um teste básico do BFS
    """
    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(0, 2)
    g.addAresta(1, 2)

    g.bfs(0)

    assert g.vertices[0].pai is None
    assert g.vertices[0].visitado is True
    assert g.vertices[0].d == 0

    assert g.vertices[1].pai is g.vertices[0]
    assert g.vertices[1].visitado is True
    assert g.vertices[1].d == 1

    assert g.vertices[2].pai is g.vertices[0]
    assert g.vertices[2].visitado is True
    assert g.vertices[2].d == 1

    """
    Executa os testes da função verificar_mais_distante
    """
    # Grafo da figura 22.2 do Cormen (versão não orientada)
    g = Grafo(6)
    g.addAresta(0, 1)
    g.addAresta(0, 3)
    g.addAresta(1, 4)
    g.addAresta(2, 4)
    g.addAresta(2, 5)
    g.addAresta(3, 1)
    g.addAresta(4, 3)

    assert vertice_mais_distante(g, 0) == 5
    assert vertice_mais_distante(g, 2) == 0

    g = Grafo(10)
    g.addAresta(0, 3)
    g.addAresta(2, 9)
    g.addAresta(3, 2)
    g.addAresta(3, 8)
    g.addAresta(6, 9)
    g.addAresta(8, 6)
    g.addAresta(3, 1)
    g.addAresta(6, 7)
    g.addAresta(7, 4)
    g.addAresta(4, 1)

    assert vertice_mais_distante(g, 0) == 7

    """
    Executa os testes das funções diâmetro e verificar_arvore
    """

    g = Grafo(6)
    g.addAresta(0, 1)
    g.addAresta(0, 4)
    g.addAresta(1, 2)
    g.addAresta(1, 3)
    g.addAresta(4, 5)

    assert diameter(g) == 4
    assert verificar_arvore(g) is True

    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(0, 2)

    assert diameter(g) == 2
    assert verificar_arvore(g) is True

    g = Grafo(6)
    g.addAresta(0, 1)
    g.addAresta(0, 2)
    g.addAresta(2, 3)
    g.addAresta(3, 4)
    g.addAresta(1, 5)

    assert diameter(g) == 5
    assert verificar_arvore(g) is True

    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(0, 2)
    g.addAresta(1, 2)

    assert verificar_arvore(g) is False

    # Grafo da figura 23.1 Cormen
    g = Grafo(9)
    g.addAresta(0, 1, 4)
    g.addAresta(0, 7, 8)
    g.addAresta(1, 7, 11)
    g.addAresta(7, 8, 7)
    g.addAresta(1, 2, 8)
    g.addAresta(7, 6, 1)
    g.addAresta(8, 2, 2)
    g.addAresta(8, 6, 6)
    g.addAresta(6, 5, 2)
    g.addAresta(2, 5, 4)
    g.addAresta(2, 3, 7)
    g.addAresta(3, 4, 9)
    g.addAresta(3, 5, 14)
    g.addAresta(4, 5, 10)

    saida = mst_kruskal(g)
    assert verificar_arvore(saida) is True
    assert diameter(saida) == 7

    """
    Testa a geração de árvores pelo random_tree_random_walk com múltiplos números de vértices
    e cada número de vértices é testado 10 vezes.
    Retorna o resultado dos testes no arquivo randomwalk.txt no formato esperado pelo programa plot.py
    """
    runs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    resultado: Dict[int, float] = dict()
    print("Algoritmo Random-Walk - 10 iterações por N")
    for r in runs:
        print("Medindo N = " + str(r))
        diametros = []
        for _ in range(0, 10):
            g = random_tree_random_walk(r)
            if verificar_arvore(g):
                diametros.append(diameter(g))
            else:
                raise AssertionError("o grafo gerado por 'random_tree_random_walk' não é um árvore")

        if len(diametros) != 0:
            resultado[r] = sum(diametros) / len(diametros)

    with open("randomwalk.txt", 'w') as f:
        for key, val in resultado.items():
            f.write('%d %f\n' % (key, val))

    """
    Testa a geração de árvores pelo random_tree_kruskal com múltiplos números de vértices
    e cada número de vértices é testado 10 vezes.
    Retorna o resultado dos testes no arquivo kruskal.txt no formato esperado pelo programa plot.py
    """
    runs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    resultado: Dict[int, float] = dict()
    print("Algoritmo Kruskal - 10 iterações por N")
    for r in runs:
        print("Medindo N = " + str(r))
        diametros = []
        for _ in range(0, 10):
            g = random_tree_kruskal(r)
            if verificar_arvore(g):
                diametros.append(diameter(g))
            else:
                raise AssertionError("o grafo gerado por 'random_tree_kruskal' não é um árvore")

        if len(diametros) != 0:
            resultado[r] = sum(diametros) / len(diametros)

    with open("kruskal.txt", 'w') as f:
        for key, val in resultado.items():
            f.write('%d %f\n' % (key, val))


if __name__ == '__main__':
    main()
