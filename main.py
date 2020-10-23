#berkeozgurarslan

import pygame
import random
import linalg

pygame.font.init()

WIDTH, HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()


class Cell:
    cells = []
    color_dict = {1: (125,0,125), 2: (0,0,255), 3: (0,255,0), 4: (0, 255, 255) }

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.growth = 5
        self.color = self.color_dict[vel]

    def move(self, foods):
        food_dist = []
        for food in foods:
            food_dist.insert(foods.index(food), self.pos.dist_between(food.pos))
            sorted_list = food_dist.copy()
            sorted_list.sort()
            for i in food_dist:
                if i == sorted_list[0]:
                    destination = foods[food_dist.index(i)].pos
                    break
            v = self.pos.scalar_multiple(-1)
            direction = linalg.addition(destination, v)
            direction_unit = direction.scalar_multiple(1/direction.norm)
            velocity = direction_unit.scalar_multiple(self.vel)
            for i in range(self.pos.rowcount):
                self.pos.itself[i][0] += velocity.itself[i][0]
            new_pos = [a[0] for a in self.pos.itself]
            self.pos = linalg.vector(new_pos)

    def eat(self, food):
        if self.pos.dist_between(food.pos) < 5:
            Food.foods.remove(food)
            self.growth += 5

    def split(self):
        if self.growth >= 15:
            cell1 = Cell(linalg.addition(self.pos, linalg.vector((0, 15))), self.vel)
            cell2 = Cell(linalg.addition(self.pos, linalg.vector((0,-15))), self.vel)
            self.cells.append(cell1)
            self.cells.append(cell2)
            self.cells.remove(self)

    def collide(self, cell):
        if self.pos.dist_between(cell.pos) < self.growth or self.pos.dist_between(cell.pos) < cell.growth:
            neg = cell.pos.scalar_multiple(-1)
            adjust_vect = linalg.addition(self.pos, neg)
            adjust_unit = adjust_vect.scalar_multiple(1 / adjust_vect.norm)
            velocity = adjust_unit.scalar_multiple(self.vel)
            for i in range(self.pos.rowcount):
                self.pos.itself[i][0] += velocity.itself[i][0]
            new_pos = [a[0] for a in self.pos.itself]
            self.pos = linalg.vector(new_pos)

    def draw(self):
        pygame.draw.circle(WIN,self.color, (int(self.pos.itself[0][0]), int(self.pos.itself[1][0])), self.growth * 2)


class Food:
    foods = []

    def __init__(self, pos):
        self.pos = pos

    def draw(self):
        pygame.draw.circle(WIN, (255,0,0), (self.pos.itself[0][0], self.pos.itself[1][0]), 10)


for i in range(10):
    Cell.cells.append(Cell(linalg.vector((random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100))), random.randrange(1,5)))


def main():
    counter = 0
    run = True

    def draw():
        WIN.fill((100,100,100))

        for cell in Cell.cells:
            cell.draw()

        for food in Food.foods:
            food.draw()

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(Food.foods) <= 5:
            Food.foods.append(Food(linalg.vector((random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100)))))

        for cell in Cell.cells:
            cell.move(Food.foods)
            for cell1 in Cell.cells:
                if cell1 != cell:
                    cell.collide(cell1)
            for food in Food.foods:
                cell.eat(food)
            cell.split()

        if counter % 150 == 0:
            for cell in Cell.cells:
                if cell.growth >=1:
                    cell.growth -= 1
                if cell.growth == 0:
                    Cell.cells.remove(cell)

        counter += 1

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            purple = [i for i in Cell.cells if i.vel == 1]
            blue = [i for i in Cell.cells if i.vel == 2]
            green = [i for i in Cell.cells if i.vel == 3]
            cyan = [i for i in Cell.cells if i.vel == 4]

            font = pygame.font.SysFont('freesans', 40, True)
            label1 = font.render(f'Number of purple cells: {len(purple)}', 1 , (255,255,255))
            label2 = font.render(f'Number of blue cells: {len(blue)}', 1 , (255,255,255))
            label3 = font.render(f'Number of green cells: {len(green)}', 1 , (255,255,255))
            label4 = font.render(f'Number of cyan cells: {len(cyan)}', 1 , (255,255,255))

            for i in range(200):
                WIN.blit(label1, (300, 200))
                WIN.blit(label2, (300, 250))
                WIN.blit(label3, (300, 300))
                WIN.blit(label4, (300, 350))
                pygame.display.update()


main()
