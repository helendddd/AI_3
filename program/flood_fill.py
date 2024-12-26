#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class FloodFillProblem:
    """
    Класс, представляющий задачу заливки области с заданным цветом.
    """

    def __init__(self, matrix, start_node, target_color, replacement_color):
        self.matrix = matrix
        self.start_node = start_node
        self.target_color = target_color
        self.replacement_color = replacement_color

    def is_valid(self, x, y):
        """
        Проверяет, находится ли узел в пределах матрицы и имеет целевой цвет.
        """
        rows, cols = len(self.matrix), len(self.matrix[0])
        return (
            0 <= x < rows
            and 0 <= y < cols
            and self.matrix[x][y] == self.target_color
        )

    def fill(self):
        """
        Выполняет алгоритм заливки, начиная с начального узла.
        """
        start_x, start_y = self.start_node

        # Если начальный узел уже окрашен в цвет замены, ничего не делаем.
        if self.matrix[start_x][start_y] == self.replacement_color:
            return self.matrix

        def dfs(x, y):
            """
            Рекурсивная функция для выполнения заливки.
            """
            if not self.is_valid(x, y):
                return

            # Заменяем цвет текущего узла
            self.matrix[x][y] = self.replacement_color

            # Рекурсивно обрабатываем соседей
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                dfs(x + dx, y + dy)

        # Запускаем заливку
        dfs(start_x, start_y)
        return self.matrix


def main():
    """
    Основная функция для создания задачи и выполнения алгоритма заливки.
    """
    matrix = [
        ["Y", "Y", "Y", "Y", "G", "G", "G", "G", "G", "G"],
        ["Y", "Y", "Y", "Y", "Y", "Y", "G", "X", "X", "X"],
        ["G", "G", "G", "G", "G", "G", "G", "X", "X", "X"],
        ["W", "W", "W", "W", "W", "G", "G", "X", "X", "X"],
        ["W", "R", "R", "R", "R", "R", "G", "X", "X", "X"],
        ["W", "W", "W", "R", "R", "G", "G", "X", "X", "X"],
        ["W", "B", "W", "R", "R", "R", "R", "R", "R", "X"],
        ["W", "B", "B", "B", "B", "R", "R", "X", "X", "X"],
        ["W", "B", "B", "X", "B", "B", "B", "B", "X", "X"],
        ["W", "B", "B", "X", "X", "X", "X", "X", "X", "X"],
    ]

    start_node = (3, 9)
    target_color = "X"
    replacement_color = "C"

    # Создаем задачу заливки
    problem = FloodFillProblem(
        matrix, start_node, target_color, replacement_color
    )

    # Выполняем заливку
    result = problem.fill()

    # Выводим результат
    for row in result:
        print(row)


if __name__ == "__main__":
    main()
