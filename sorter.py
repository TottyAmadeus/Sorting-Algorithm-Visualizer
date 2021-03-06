
import pygame
import random
import math

pygame.init()


class Settings:

    # Colors
    BLACK = 0, 0, 0,
    WHITE = 255, 255, 255
    MAX_GRAD = 160
    MIN_GRAD = 30
    BG_COLOR = BLACK

    # Paddings
    BORDER = 60
    TOP = 150

    # Text
    FONT = pygame.font.SysFont('hack', 13)

    # Iteration
    iterations = 0

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.window.fill(self.BG_COLOR)
        pygame.display.set_caption("Sorting Algorithm Vizualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)
        self.spacing = 2
        self.bar_width = round((self.width - self.BORDER) / len(lst))
        self.bar_height = round(
            (self.height - self.TOP) / (self.max_value - self.min_value))
        self.start_x = 10


def map_range(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def draw(setting, sort, algo, asc):

    setting.window.fill(setting.BG_COLOR)

    infotext = setting.FONT.render(f"Sorting Algorithm: {algo.__name__} | Order: {'Ascending' if asc else 'Descending'} | {'Sorting...'if sort else 'In Standby'}", 1, setting.WHITE)
    infotext_rect = infotext.get_rect()
    infotext_rect.left = 6
    infotext_rect.top = 5
    setting.window.blit(infotext, infotext_rect)

    itertext = setting.FONT.render(f"{setting.iterations} {'iterations' if (setting.iterations != 1) else 'iteration'}", 1, setting.WHITE)
    itertext_rect = itertext.get_rect()
    itertext_rect.right = setting.width - 6
    itertext_rect.top = 5
    setting.window.blit(itertext, itertext_rect)

    ctrls = setting.FONT.render(f"Controls:", 1, setting.WHITE)
    ctrls_rect = ctrls.get_rect()
    ctrls_rect.left = 6
    ctrls_rect.top = 35
    setting.window.blit(ctrls, ctrls_rect)

    keys = setting.FONT.render(f"R - Reset | Return - Start | Arrows: Algorithm / Order", 1, setting.WHITE)
    keys_rect = keys.get_rect()
    keys_rect.left = 6
    keys_rect.top = 50
    setting.window.blit(keys, keys_rect)

    draw_list(setting)
    pygame.display.update()


def draw_list(setting):
    lst = setting.lst
    for i, val in enumerate(lst):
        x = setting.start_x + i * setting.bar_width
        y = setting.height - (val - setting.min_value) * setting.bar_height

        grad = map_range(val, setting.min_value,setting.max_value, setting.MIN_GRAD, setting.MAX_GRAD)

        color = (grad, grad, grad)

        pygame.draw.rect(setting.window, color,
                         (x, y, setting.bar_width, setting.height))


def gen_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst
  

def bubble_sort(setting, asc = True):
    lst = setting.lst
    for i in range(len(lst) -1):
        for j in range(0, len(lst) - 1 - i):
            if (lst[j] > lst[j+1] and asc) or (lst[j] < lst[j+1] and not asc):
                setting.iterations += 1
                lst[j] , lst[j+1] = lst[j+1] , lst[j]
                yield True


def selection_sort(setting, asc = True):
    lst = setting.lst
    for i in range(len(lst)):
        index = i
        for j in range(i+1, len(lst)):
            if (lst[index] > lst[j] and asc) or (lst[index] < lst[j] and not asc):
                setting.iterations += 1
                index = j
        lst[i] , lst[index] = lst[index] , lst[i]
        yield True


def main():
    running = True
    n = 200
    min_val = 10
    max_val = 100
    sorting = False
    ascending = True

    algorithm_list = [bubble_sort, selection_sort]
    algorithm_num = 0
    algorithm = bubble_sort
    sorting_generator = None
    lst = gen_list(n, min_val, max_val)
    setting = Settings(800, 600, lst)
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        
        draw(setting, sorting, algorithm, ascending)

        pygame.display.update()

        for event in pygame.event.get():
            keys=pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue
            
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed() 

                if key[pygame.K_r]:
                    lst = gen_list(n, min_val, max_val)
                    setting.set_list(lst)
                    setting.iterations = 0
                    sorting = False

                if key[pygame.K_RETURN] and not sorting:
                    sorting = True
                    setting.iterations = 0
                    sorting_generator = algorithm(setting, ascending)

                if key[pygame.K_UP] and not sorting:
                    setting.iterations = 0
                    ascending = True

                if key[pygame.K_DOWN] and not sorting:
                    setting.iterations = 0
                    ascending = False

                if key[pygame.K_LEFT] and not sorting:
                    setting.iterations = 0
                    algorithm_num -= 1
                    if algorithm_num < 0:
                        algorithm_num = 0
                    algorithm = algorithm_list[algorithm_num]

                if key[pygame.K_RIGHT] and not sorting:
                    setting.iterations = 0
                    algorithm_num += 1
                    if algorithm_num > 1:
                        algorithm_num = 1
                    algorithm = algorithm_list[algorithm_num]

    pygame.quit()


if __name__ == "__main__":
    main()
