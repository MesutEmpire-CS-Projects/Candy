import random

import pygame

class Empty(Exception):
    def __init__(self, message="The container is empty."):
        self.message = message
        super().__init__(self.message)


# Define the Stack class
class Stack:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
        else:
            raise Empty()

    def top(self):
        if not self.is_empty():
            return self._items[-1]
        else:
            raise Empty()

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
CANDY_SIZE = (90, 35)
SPRING_WIDTH = 50
SPRING_HEIGHT = 300
SPRING_CONSTANT = 0.8
CANDY_FORCE = 10

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Stack Dispenser")
font = pygame.font.Font('freesansbold.ttf', 20)

# Initialize the Stack
candy_stack = Stack()

class Button:
    def __init__(self, name, x, y):
        self._name = name
        self._width = 150
        self._height = 50
        self._rect = pygame.rect.Rect(x, y, self._width, self._height)
        self._enabled = True

    def draw(self):
        pygame.draw.rect(screen, 'black', self._rect, 2)
        text = font.render(self._name, True, 'black')
        screen.blit(text, (self._rect.centerx - text.get_width() // 2, self._rect.centery - text.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)

    def get_name(self):
        return self._name


class Display:
    def __init__(self):
        self._result = None
        self._color = 'black'

    def show(self):
        text = font.render(str(self._result), True, self._color)
        textRect = pygame.rect.Rect(750, 100, 50, 100)
        screen.blit(text, textRect)

    def set_result(self, info, color='black'):
        self._result = info
        self._color = color

    def reset_result(self):
        self._result = None

    def get_result(self):
        return self._result


class Candy:
    def __init__(self, color):
        self._label = random.randint(0, 1000)
        self._color = color

    def draw(self, x, y):
        candyRect = pygame.rect.Rect(x, y, CANDY_SIZE[0], CANDY_SIZE[1])
        pygame.draw.ellipse(screen, self._color, candyRect)
        text = font.render(str(self._label), True, 'black')
        textRect = pygame.rect.Rect(x - 40, y + 5, CANDY_SIZE[0], CANDY_SIZE[1])
        screen.blit(text, textRect)

    def get_candy(self):
        return self._label


class Dispenser:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._width = SPRING_WIDTH * 4
        self._height = SPRING_HEIGHT

    def draw(self):
        pygame.draw.lines(screen, 'black', False, [(self._x, self._y), (self._x, self._y + self._height),
                                                   (self._x + self._width, self._y + self._height),
                                                   (self._x + self._width, self._y)], 2)


class Spring:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._height = SPRING_HEIGHT
        self._top_plate_x = WIDTH // 2 - SPRING_WIDTH * 2  # self._rect = pygame.Rect(self._x, self._y, SPRING_WIDTH, self._height)

    def draw(self):
        pygame.draw.line(screen, 'black', (self._top_plate_x, self._y), (self._top_plate_x + SPRING_WIDTH * 4, self._y),
                         8)
        image = pygame.image.load('spring.png')
        image = pygame.transform.scale(image, (SPRING_WIDTH, self._height))
        screen.blit(image, (self._x, self._y, 5, self._height))

    def adjust(self, operation):
        extension = CANDY_FORCE / SPRING_CONSTANT
        if operation == 'push':
            if self._height - extension >= 25:
                self._height -= extension
                self._y += extension
        elif operation == 'pop':
            if self._height + extension > SPRING_HEIGHT:
                self._height = SPRING_HEIGHT
            else:
                self._height += extension
                self._y -= extension

    @property
    def get_y(self):
        return self._y


spring = Spring(WIDTH // 2 - SPRING_WIDTH // 2, HEIGHT // 2)
dispenser = Dispenser(WIDTH // 2 - SPRING_WIDTH * 2, HEIGHT // 2)
display_info = Display()

buttons = [Button('Pop', 10, 10), Button('Push', 10, 70), Button('Top', 10, 130), Button('Is Empty', 10, 190),
    Button('Len', 10, 250)]


def add_candy():
    if not candy_stack.is_empty():
        spring.adjust('push')
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    candy = Candy(color)
    candy_stack.push(candy)
    display_info.reset_result()


def remove_candy():
    try:
        candy = candy_stack.pop()
        if candy is not None:
            spring.adjust('pop')
            display_info.set_result(f'Popped : {candy.get_candy()}')
    except Empty:
        display_info.set_result("Error : Stack is empty", 'red')


def is_empty():
    if candy_stack.is_empty():
        display_info.set_result("Error : Stack is empty", 'red')
    else:
        display_info.set_result("Stack is not empty.")


def get_length():
    display_info.set_result(f"Stack Length : {len(candy_stack)}")


def get_top_candy():
    try:
        top_candy = candy_stack.top()
        display_info.set_result(f"Top Candy Label : {top_candy.get_candy()}")
    except Empty:
        display_info.set_result('Error : Stack is empty', 'red')


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(mouse_pos):
                    if button.get_name() == 'Pop':
                        remove_candy()
                    elif button.get_name() == 'Push':
                        add_candy()
                    elif button.get_name() == 'Top':
                        get_top_candy()
                    elif button.get_name() == 'Is Empty':
                        is_empty()
                    elif button.get_name() == 'Len':
                        get_length()

    screen.fill('white')

    # Draw the dispenser
    dispenser.draw()

    if display_info.get_result():
        display_info.show()

    spring.draw()

    # Draw the candies in the stack
    x = WIDTH // 2 - CANDY_SIZE[0] // 2
    y = spring.get_y - CANDY_SIZE[1]
    for candy in candy_stack._items:
        candy.draw(x, y)
        y -= CANDY_SIZE[1] + 3

    # Draw buttons
    for button in buttons:
        button.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

