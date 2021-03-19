from typing import List, Set


class DepthFirstSearch:
    def __init__(self, adjacency: List[List[int]]):
        self._stack: List[int] = []
        self._first_group: Set[int] = set()
        self._second_group: Set[int] = set()
        self._adjacency_list = adjacency
        self._visited: Set[int] = set()

    def start(self):
        self._first_group.add(1)
        self._stack.append(1)
        while len(self._stack):
            current_node = self._stack.pop()
            if current_node in self._visited:
                continue
            if current_node in self._first_group:
                self._add(self._adjacency_list[current_node], self._first_group, self._second_group)
            else:
                self._add(self._adjacency_list[current_node], self._second_group, self._first_group)
            self._visited.add(current_node)

    def _add(self, nodes: List[int], group_check: Set[int], group_add: Set[int]):
        for node in nodes:
            if node in group_check:
                raise ValueError()
            group_add.add(node)
            self._stack.append(node)

    def __str__(self):
        first = list(self._first_group)
        second = list(self._second_group)
        first.sort()
        second.sort()
        if second[0] < first[0]:
            first, second = second, first
        return f"{' '.join(list(map(str, first)))} 0\n{' '.join(list(map(str, second)))} 0"


if __name__ == '__main__':
    with open('input.txt') as f:
        input_str = f.read().strip()
    adjacency_list = [list(map(int, line.split(' ')[:-1])) for line in input_str.split('\n')[1:]]
    dfs = DepthFirstSearch([[]] + adjacency_list)
    output = 'N'
    try:
        dfs.start()
    except ValueError:
        pass
    else:
        output = f'Y\n{dfs}'
    with open('output.txt', 'w') as f:
        f.write(output)
