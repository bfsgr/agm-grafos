from typing import List
from collections import deque

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
        self.distance = None
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
        self.nodes = n

    def addAresta(self, u: int, v: int):
        """
        Adiciona a aresta (u, v) ao grafo.

        u e v precisam ser vértices válidos, isto é precisam ser um valor
        entre 0 e n - 1, onde n é a quantidade de vértices do grafo.

        Este método não verifica se a aresta (u, v) já existe no grafo.
        """
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])

    def reset_distance(self):
        """
        Define o atributo distance de todos os vértices como None
        """
        for v in self.vertices:
            v.distance = None

    def bfs(self, v: int) -> int:
        """
        Versão modificada do BFS que calcula o vértice com distância máxima no grafo g em
        relação ao vértice v. Assume-se que v sempre está no grafo g
        """
        
        self.reset_distance()

        q = deque(maxlen=self.nodes)

        self.vertices[v].distance = 0
        self.vertices[v].visited = True

        q.append(v)

        v_max_distance = v

        while not len(q) == 0:
            node = q.popleft()

            for vertex in self.vertices[node].adj:
                if vertex.distance is None:
                    vertex.distance = self.vertices[node].distance + 1
                    q.append(vertex.num)

                    if vertex.distance > self.vertices[v_max_distance].distance:
                        v_max_distance = vertex.num

        return v_max_distance


def diameter(g: Grafo) -> int:
    """
    Calcula o diametro da árvore (grafo) g
    """

    vertex_a = g.bfs(0)

    vertex_b = g.bfs(vertex_a)

    return g.vertices[vertex_b].distance


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
    g.addAresta(5, 5)

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


if __name__ == '__main__':
    main()
