#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from itertools import product


class Problem:
    """Абстрактный класс для формальной задачи."""

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, a, s1):
        return 1

    def h(self, node):
        return 0

    def __str__(self):
        return "{}({!r}, {!r})".format(
            type(self).__name__, self.initial, self.goal
        )


class Node:
    """Узел в дереве поиска."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(
            state=state, parent=parent, action=action, path_cost=path_cost
        )

    def __repr__(self):
        return "<{}>".format(self.state)

    def __len__(self):
        return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other):
        return self.path_cost < other.path_cost


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem, node):
    """Раскрываем узел, создав дочерние узлы."""
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    """Последовательность действий, чтобы добраться до этого узла."""
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    """Последовательность состояний, чтобы добраться до этого узла."""
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


class MatrixPathProblem(Problem):
    """Задача поиска пути в матрице символов."""

    def __init__(self, matrix, start_char):
        self.matrix = matrix
        self.start_char = start_char
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.initial = self.find_start_positions()
        self.goal = None  # Целевое состояние не определено

    def find_start_positions(self):
        """Находим все позиции начального символа в матрице."""
        positions = []
        for r, c in product(range(self.rows), range(self.cols)):
            if self.matrix[r][c] == self.start_char:
                positions.append((r, c))
        return positions

    def actions(self, state):
        """Возвращаем список допустимых действий из состояния."""
        r, c = state
        possible_actions = [
            (dr, dc)
            for dr, dc in product([-1, 0, 1], repeat=2)
            if (dr != 0 or dc != 0)
            and 0 <= r + dr < self.rows
            and 0 <= c + dc < self.cols
            and ord(self.matrix[r + dr][c + dc]) == ord(self.matrix[r][c]) + 1
        ]
        return possible_actions

    def result(self, state, action):
        """Возвращаем новое состояние после применения действия."""
        r, c = state
        dr, dc = action
        return (r + dr, c + dc)

    def is_goal(self, state):
        """Переопределяем метод, но цель не определена явно."""
        return False


def depth_first_search(problem):
    """Поиск в глубину для нахождения самого длинного пути."""

    def recursive_dfs(node, visited):
        visited.add(node.state)
        max_length = 0
        for child in expand(problem, node):
            if child.state not in visited:
                length = recursive_dfs(child, visited)
                max_length = max(max_length, length)
        visited.remove(node.state)
        return 1 + max_length

    max_path_length = 0
    for start_state in problem.initial:
        node = Node(start_state)
        max_path_length = max(max_path_length, recursive_dfs(node, set()))
    return max_path_length


if __name__ == "__main__":
    matrix = [
        ["M", "N", "O", "P", "Q"],
        ["L", "K", "J", "I", "R"],
        ["A", "B", "C", "D", "E"],
        ["Z", "Y", "X", "W", "V"],
        ["U", "T", "S", "F", "G"],
    ]

    start_char = "A"
    problem = MatrixPathProblem(matrix, start_char)
    result = depth_first_search(problem)
    print(
        f"Длина самого длинного пути, начиная с символа '{start_char}': "
        f"{result}"
    )
