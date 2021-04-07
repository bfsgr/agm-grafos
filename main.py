# EQUIPE: Ana Laura Schoffen Rodrigues e Bruno Fusieger Santana
# RAs: 115456 e 112646
from typing import List, Dict
from collections import deque
from random import *


class Vertice:
    """
    Representa um vértice de um grafo com um número, uma lista de adjacências
    e uma valor de distância
    """

    def __init__(self, num: int) -> None:
        """
        Cria um novo vértice com o número num e com uma lista de adjacências vazia.
        E também um número distance que é usado durante o BFS

        Em geral este construtor não é chamado diretamente mas é chamado pelo
        construtor da classe Grafo.
        """
        self.num = num
        self.visitado = False
        self.pai = None
        self.d = None
        self.adj: List[Vertice] = []

    def __str__(self) -> str:
        return "Vertice(%d)" % self.num


class Grafo:
    """
    Representa um grafo não orientado
    """

    def __init__(self, n: int) -> None:
        """
        Cria um novo grafo com n vértices com os números 0, 1, ..., n-1.
        """
        self.vertices = [Vertice(i) for i in range(n)]
        self.num_arrestas = 0
        self.num_vertices = n

    def addAresta(self, u: int, v: int):
        """
        Adiciona a aresta (u, v) ao grafo.

        u e v precisam ser vértices válidos, isto é precisam ser um valor
        entre 0 e n - 1, onde n é a quantidade de vértices do grafo.

        Este método não verifica se a aresta (u, v) já existe no grafo.
        """
        self.num_arrestas += 1
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])


def vertice_mais_distante(g: Grafo, v: int) -> int:
    """
    Versão modificada do BFS que calcula o vértice com distância máxima no grafo g em
    relação ao vértice v. Assume-se que v sempre está no grafo g
    Retorna o número do vértice com distância máxima em relação à v
    """

    for x in g.vertices:
        x.visitado = False
        x.d = None
        x.pai = None

    q = deque(maxlen=g.num_vertices)

    g.vertices[v].d = 0
    g.vertices[v].visitado = True

    q.append(g.vertices[v])

    v_max_distance = g.vertices[v]

    while not len(q) == 0:
        node: Vertice = q.popleft()

        for vertex in node.adj:
            if not vertex.visitado:
                vertex.d = node.d + 1
                vertex.visitado = True
                q.append(vertex)

                if vertex.d > v_max_distance.d:
                    v_max_distance = vertex

    return v_max_distance.num


def verificar_arvore(g: Grafo) -> bool:
    """
    Verifica se um grafo é uma árvore, usando uma versão modificada do BFS
    Retorna True se o grafo é uma árvore, False caso contrário
    Usamos a definição de que qualquer grafo conexo com n vértices e n - 1 arestas é uma árvore
    """

    if g.num_arrestas != g.num_vertices - 1:
        return False

    for x in g.vertices:
        x.visitado = False
        x.d = None
        x.pai = None

    q = deque(maxlen=g.num_vertices)

    g.vertices[0].d = 0
    g.vertices[0].visitado = True

    q.append(g.vertices[0])

    processados = 1

    while not len(q) == 0:
        node: Vertice = q.popleft()

        for v in node.adj:
            if not v.visitado:
                v.d = node.d + 1
                v.pai = node.num
                v.visitado = True
                processados += 1
                q.append(v)

    return processados == g.num_vertices


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
        v.visitado = False
    u = g.vertices[0]
    u.visitado = True

    while g.num_arrestas < n - 1:
        v = g.vertices[randrange(0, n)]
        if not v.visitado:
            g.addAresta(u.num, v.num)
            v.visitado = True
        u = v
    return g


def main():
    """
    Executa os testes da função bfs
    """
    # Grafo da figura 22.2 do Cormen
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

    assert vertice_mais_distante(g, 0)

    """
    Executa os testes das funções diametro e verificar_arvore 
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

    """
    Testa a geração de árvores pelo random_tree_random_walk com múltiplos números de vértices
    e cada número de vértices é testado 100 vezes.
    Retorna o resultado dos testes no arquivo randomwalk.txt no formato esperado pelo programa plot.py
    """
    runs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    resultado: Dict[int, float] = dict()
    for r in runs:
        diametros = []
        for i in range(0, 100):
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


if __name__ == '__main__':
    main()
