from queue import Queue
from typing import Optional, Set, List, Tuple


class CoordinatesException(Exception):
    def __init__(self, message: str):
        self.message = f'Coordinates - {message} not exist!'


class Node:
    def __init__(self, x: str, y: str):
        self._x = x
        self._y = y
        self.last: Node = None

    @property
    def x(self) -> Optional[str]:
        return self._x

    @property
    def y(self) -> Optional[str]:
        return self._y

    def __hash__(self):
        return f'{self._x}{self._y}'.__hash__()


class BreadthFirstSearch:
    _alph_oX: str = 'abcdefgh'
    _alph_oY: str = '12345678'
    _steps: List[Tuple[int, int]] = [
        (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)  # (dx, dy)
    ]

    def __init__(self, start: str, end: str):
        self._queue_nodes: Queue[Node] = Queue()
        self._open_nodes: Set[Node] = set()
        self._target: Node = self._create_node(end[0], end[1], 0, 0)
        self._bad_nodes: Set[Node] = {self._create_node(self._target.x, self._target.y, -1, 1),
                                      self._create_node(self._target.x, self._target.y, 1, 1),
                                      self._create_node(self._target.x, self._target.y, -1, -1),
                                      self._create_node(self._target.x, self._target.y, 1, -1)}
        self._start = self._create_node(start[0], start[1], 0, 0)
        if self._start:
            self._start.last = None
            self._queue_nodes.put(self._start)

    def find(self) -> Optional[str]:
        while not self._queue_nodes.empty():
            node = self._queue_nodes.get()
            if node.__hash__() == self._target.__hash__():
                buffer = []
                while node:
                    buffer.append(f'{node.x}{node.y}')
                    node = node.last
                return '\n'.join(buffer[::-1])
            for dx, dy in self._steps:
                new_node = self._create_node(node.x, node.y, dx, dy)
                if new_node and new_node not in self._bad_nodes \
                        and new_node not in self._open_nodes:
                    new_node.last = node
                    self._queue_nodes.put(new_node)
            self._open_nodes.add(node)
        return 'Way is not exist!'

    def _create_node(self, x: str, y: str, dx: int, dy: int) -> Optional[Node]:
        index_X: int = self._alph_oX.find(x)
        index_Y: int = self._alph_oY.find(y)
        if index_X < 0 or index_Y < 0:
            raise CoordinatesException(f'{x}{y}')
        index_X += dx
        index_Y += dy
        if index_X < len(self._alph_oX) and index_Y < len(self._alph_oY) and index_X >= 0 and index_Y >= 0:
            return Node(x=self._alph_oX[index_X], y=self._alph_oY[index_Y])


if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()
    try:
        bfs = BreadthFirstSearch(*input_data.strip().split())
        output_data = bfs.find()
    except CoordinatesException as exc:
        print(exc.message)
    else:
        with open('output.txt', 'w') as f:
            f.write(output_data)

