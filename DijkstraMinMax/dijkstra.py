from typing import List, Dict, Tuple, Optional, Set


class Node:
    def __init__(self, name: int):
        self._name = name
        self.last: Node = None
        self.weight: float = float('inf')
        self.next: List[Node] = []
        self.visited: bool = False

    @property
    def name(self):
        return self._name

    def __hash__(self):
        return self._name


class Graph:
    def __init__(self, graph: List[str]):
        self._graph = self._parser(graph)

    def _parser(self, graph: List[str]) -> Dict[Tuple[int, int], int]:
        result = dict()
        for startNode in range(len(graph)):
            line = graph[startNode].split(' ')[:-1]
            for i in range(0, len(line) - 1, 2):
                result[(int(line[i]), startNode + 1)] = int(line[i + 1])
        return result

    def get(self, start_node: Node, end_node: Node) -> Optional[int]:
        return self._graph.get((start_node.name, end_node.name), None)


class Dijkstra:
    _nodes_list: List[Node]
    _nodes_set: Set[Node]
    _graph: Graph

    def __init__(self, count: int, graph: Graph):
        self._nodes: Dict[int, Node] = {name: Node(name) for name in range(1, count + 1)}
        self._graph = graph
        self.count = count
        self._add_nodes()

    def _add_nodes(self):
        for first in self._nodes.values():
            for second in self._nodes.values():
                if self._graph.get(first, second):
                    first.next.append(second)

    def _find_min(self, nodes: List[Node]) -> Optional[Node]:
        max_weight = float('inf')
        n: Node = None
        for node in nodes:
            if not node.visited and node.weight <= max_weight:
                n = node
                max_weight = node.weight
        return n

    def _find_max(self, nodes: List[Node]) -> Node:
        max_weight = float('-inf')
        n: Node = None
        for node in nodes:
            if not node.visited and node.weight > max_weight:
                n = node
                max_weight = node.weight
        return n

    def find(self, start: int, end: int) -> str:
        startNode = self._nodes.get(start)
        endNode = self._nodes.get(end)
        for node in startNode.next:
            weight = self._graph.get(startNode, node)
            if weight:
                node.weight = weight
                node.last = startNode
        current_node = startNode
        while not endNode.visited and current_node:
            max_node = self._find_min(current_node.next)
            current_node.visited = True
            if not max_node:
                current_node = current_node.last
                continue
            if self._graph.get(current_node, max_node) < max_node.weight:
                max_node.weight = self._graph.get(current_node, max_node)
                max_node.last = current_node
            current_node = max_node
        node = endNode
        if not node.visited:
            return 'N'
        buffer = []
        while node:
            buffer.append(str(node.name))
            node = node.last
        return 'Y\n' + ' '.join(buffer[::-1]) + f'\n{endNode.weight}'


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = int(f.readline())
        arr = [f.readline().strip() for _ in range(lines)]
        start, end = int(f.readline()), int(f.readline())
        graph = Graph(arr)
        dijkstra = Dijkstra(lines, graph)
    with open('output.txt', 'w') as f:
        f.write(dijkstra.find(start, end))
