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


def is_valid_move(nx, ny, rows, cols, path):
    """Проверяет, находится ли (nx, ny) в матрице и посещена ли она."""
    return 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in path


class MatrixWordSearchProblem(Problem):
    """Задача поиска слов в матрице символов."""

    def __init__(self, board, dictionary):
        super().__init__(initial=None)
        self.board = board
        self.dictionary = set(dictionary)
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0
        self.prefixes = self._build_prefix_set(dictionary)

    def _build_prefix_set(self, words):
        """Создает множество всех префиксов из списка слов."""
        prefixes = set()
        for word in words:
            for i in range(len(word)):
                prefixes.add(word[: i + 1])
        return prefixes

    def actions(self, state):
        """Возвращает список допустимых действий из текущего состояния."""
        (x, y, path) = state
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny, self.rows, self.cols, path):
                yield (nx, ny)

    def result(self, state, action):
        """Возвращает новое состояние после применения действия."""
        (x, y, path) = state
        (nx, ny) = action
        new_path = path + [(nx, ny)]
        return (nx, ny, new_path)

    def is_goal(self, state):
        """Проверяет, является ли текущее состояние целевым."""
        (x, y, path) = state
        word = "".join(self.board[i][j] for i, j in path)
        return word in self.dictionary

    def find_words_from(self, x, y):
        """Ищет все слова, начинающиеся с позиции (x, y)."""
        found_words = set()
        stack = [(x, y, [(x, y)])]
        while stack:
            state = stack.pop()
            (cx, cy, path) = state
            word = "".join(self.board[i][j] for i, j in path)
            if word in self.dictionary:
                found_words.add(word)
            if word in self.prefixes:
                for action in self.actions(state):
                    new_state = self.result(state, action)
                    stack.append(new_state)
        return found_words

    def find_all_words(self):
        """Ищет все слова в матрице."""
        found_words = set()
        for x, y in product(range(self.rows), range(self.cols)):
            found_words.update(self.find_words_from(x, y))
        return found_words


if __name__ == "__main__":
    board = [
        ["К", "О", "Т", "И"],
        ["А", "Р", "Т", "О"],
        ["Т", "А", "К", "С"],
        ["И", "Т", "О", "К"],
    ]

    dictionary = ["КОТ", "ТОК", "КИТ", "ТАК", "АРТ", "СОК"]
    problem = MatrixWordSearchProblem(board, dictionary)
    found_words = problem.find_all_words()
    print(found_words)
