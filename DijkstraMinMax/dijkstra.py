from typing import List, Dict, Tuple, Optional, Set


class Node:
    def __init__(self, name: int):
        self._name = name
        self.last: Node = None
        self.weight: float = None

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
        self._nodes_list = [Node(name) for name in range(1, count + 1)]
        self._nodes_set = set(self._nodes_list)
        self._nodes_list.insert(0, None)
        self._graph = graph
        self.count = count

    def _find_min(self) -> Optional[Node]:
        min_weight = float('inf')
        result: Node = None
        for node in self._nodes_set:
            if node.weight and node.weight <= min_weight:
                min_weight = node.weight
                result = node
        return result

    def find(self, start: int, end: int) -> str:
        startNode = self._nodes_list[start]
        endNode = self._nodes_list[end]
        # startNode.weight = float('inf')
        self._nodes_set.remove(startNode)
        for node in self._nodes_set:
            weight = self._graph.get(startNode, node)
            if weight:
                node.weight = weight
                node.last = startNode
        for _ in range(1, self.count - 1):
            current_node = self._find_min()
            self._nodes_set.remove(current_node)
            for node in self._nodes_set:
                weight = self._graph.get(current_node, node)
                if not weight:
                    continue
                if not node.weight or weight > node.weight:
                    node.weight = weight
                    node.last = current_node
        node = endNode
        if not node.weight:
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
