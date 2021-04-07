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

    def bfs(self, v: int) -> int:
        """
        Versão modificada do BFS que calcula o vértice com distância máxima no grafo g em
        relação ao vértice v. Assume-se que v sempre está no grafo g
        Retorna o número do vértice com distância máxima em relação à v
        """

        for x in self.vertices:
            x.visitado = False
            x.d = None
            x.pai = None

        q = deque(maxlen=self.num_vertices)

        self.vertices[v].d = 0
        self.vertices[v].visitado = True

        q.append(self.vertices[v])

        v_max_distance = self.vertices[v]

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


def diameter(g: Grafo) -> int:
    """
    Calcula o diametro da árvore g.
    O diametro é a maior distância entre dois nós folha.
    Assume-se que g é uma árvore válida
    """

    vertex_a = g.bfs(0)

    vertex_b = g.bfs(vertex_a)

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


def test_bfs():
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

    max_v = g.bfs(0)

    assert max_v == 5

    max_v = g.bfs(2)

    assert max_v == 0

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

    max_v = g.bfs(0)

    assert max_v == 7


def main():
    test_bfs()

    g = Grafo(6)
    g.addAresta(0, 1)
    g.addAresta(0, 4)
    g.addAresta(1, 2)
    g.addAresta(1, 3)
    g.addAresta(4, 5)

    assert diameter(g) == 4

    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(0, 2)

    assert diameter(g) == 2

    g = Grafo(6)
    g.addAresta(0, 1)
    g.addAresta(0, 2)
    g.addAresta(2, 3)
    g.addAresta(3, 4)
    g.addAresta(1, 5)

    assert diameter(g) == 5

    runs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    resultado: Dict[int, float] = dict()
    for r in runs:
        diametros = []
        for i in range(0, 25):
            g = random_tree_random_walk(r)
            diametros.append(diameter(g))

        resultado[r] = sum(diametros) / len(diametros)

    with open("randomwalk.txt", 'w') as f:
        for key, val in resultado.items():
            f.write('%d %f\n' % (key, val))


if __name__ == '__main__':
    main()
