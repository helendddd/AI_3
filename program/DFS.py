#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


class Problem:
    """Абстрактный класс для формальной задачи."""

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):
        """Возвращает возможные действия для данного состояния."""
        raise NotImplementedError

    def result(self, state, action):
        """Возвращает результат применения действия к состоянию."""
        raise NotImplementedError

    def is_goal(self, state):
        """Проверка, является ли состояние целевым."""
        return state == self.goal

    def action_cost(self, s, a, s1):
        """Возвращает стоимость действия."""
        return 1

    def h(self, node):
        """Эвристическая функция, по умолчанию 0."""
        return 0

    def __str__(self):
        return f"{type(self).__name__}({self.initial!r}, {self.goal!r})"


class Node:
    """Узел в дереве поиска."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(
            state=state, parent=parent, action=action, path_cost=path_cost
        )

    def __repr__(self):
        return f"<{self.state}>"

    def __len__(self):
        return len(self.parent)

    def __lt__(self, other):
        if self.parent is None:
            return 0
        return 1 + (self.path_cost < other.path_cost)


failure = Node("failure", path_cost=math.inf)  # Алгоритм не смог найти решение
cutoff = Node("cutoff", path_cost=math.inf)  # Прерывание поиска


def expand(problem, node):
    """Раскрытие узла, создание дочерних узлов."""
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    """Возвращает последовательность действий до узла."""
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    """Возвращает последовательность состояний до узла."""
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


class ItalyGraphProblem(Problem):
    """Задача поиска пути между двумя населёнными пунктами в Италии."""

    def __init__(self, graph, initial, goal):
        super().__init__(initial=initial, goal=goal)
        self.graph = graph

    def actions(self, state):
        """Возвращает соседей (действия) для данного состояния."""
        return self.graph.get(state, [])

    def result(self, state, action):
        """Возвращает результат применения действия (сосед)."""
        return action

    def action_cost(self, s, a, s1):
        """Возвращает стоимость перехода между двумя пунктами."""
        return self.graph[s][s1]

    def is_goal(self, state):
        """Проверка, является ли состояние целевым."""
        return state == self.goal


def depth_first_search(problem):
    """Поиск в глубину для нахождения минимального расстояния."""
    frontier = [Node(problem.initial)]
    explored = set()

    while frontier:
        node = frontier.pop()

        if node.state in explored:
            continue

        explored.add(node.state)

        if problem.is_goal(node.state):
            return path_states(node), node.path_cost

        for child in expand(problem, node):
            frontier.append(child)

    return None, math.inf


if __name__ == "__main__":
    graph = {
        "Турин": {
            "Иврея": 51,
            "Новара": 95,
            "Милан": 140,
            "Асти": 56,
            "Кунео": 98,
        },
        "Иврея": {"Турин": 51, "Биелла": 25},
        "Биелла": {"Иврея": 25, "Верчелли": 43},
        "Новара": {"Турин": 95, "Милан": 52, "Генуя": 151, "Павия": 42},
        "Верчелли": {"Биелла": 43, "Алессандрия": 57},
        "Варезе": {"Милан": 60, "Павия": 94},
        "Милан": {
            "Турин": 140,
            "Новара": 52,
            "Варезе": 60,
            "Бергамо": 60,
            "Брешиа": 91,
            "Кремона": 91,
            "Пьянценца": 69,
            "Генуя": 52,
            "Павия": 42,
        },
        "Бергамо": {"Милан": 60, "Брешиа": 51},
        "Брешиа": {"Милан": 91, "Верона": 73, "Кремона": 58, "Бергамо": 51},
        "Верона": {"Брешиа": 73, "Модена": 105},
        "Кремона": {"Брешиа": 58, "Милан": 96, "Павия": 77},
        "Пьяченца": {"Милан": 69, "Парма": 74, "Генуя": 144},
        "Парма": {"Пьяченца": 74, "Реджо-Эмилия": 28},
        "Реджо-Эмилия": {"Парма": 28, "Модена": 25},
        "Модена": {"Верона": 105, "Реджо-Эмилия": 25},
        "Генуя": {"Новара": 151, "Пьяченца": 144, "Милан": 161},
        "Алессандрия": {"Верчелли": 57, "Асти": 38},
        "Асти": {"Турин": 56, "Алессандрия": 38, "Кунео": 104},
        "Кунео": {"Турин": 98, "Асти": 104},
        "Павия": {"Варезе": 94, "Милан": 42, "Кремона": 77},
    }

    # Создание задачи для поиска пути
    A = input("Введите начальный город: ")
    B = input("Введите конечный город: ")
    problem = ItalyGraphProblem(graph, "Милан", "Алессандрия")

    # Поиск в глубину
    path, cost = depth_first_search(problem)

    if path:
        print("Путь:", path)
        print("Стоимость:", cost)
    else:
        print("Путь не найден.")
