from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует игровой объект."""
        self.position = (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объектов. Переопределяется в дочерних классах"""
        raise NotImplementedError(
            'Метод не определен в дочернем классе.'
        )


class Apple(GameObject):
    """Класс яблока появляющегося на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR, occupied_position=None):
        """Инициализирует объект яблочко."""
        super().__init__(body_color)
        self.randomize_position(occupied_position)

    def randomize_position(self, occupied_position=None):
        """Устанавливает случайную позицию для яблока в пределах поля."""
        while True:
            position_x = (randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
                          * GRID_SIZE)
            position_y = (randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
                          * GRID_SIZE)
            if (
                occupied_position is None
                or (position_x, position_y) not in occupied_position
            ):
                self.position = (position_x, position_y)
                break

    def draw(self):
        """Отрисовывает объект яблочко на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, управляющий движением и состоянием змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует объект змейка."""
        super().__init__(body_color)
        self.reset(direction=RIGHT)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну ячейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH,
                    (head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop() if len(self.positions) > self.length
            else None
        )

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает объект змейка на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self, direction=choice([UP, DOWN, LEFT, RIGHT])):
        """Сбрасывает положение змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = direction
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш на клавиатуре."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, управляющая игровым циклом."""
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
