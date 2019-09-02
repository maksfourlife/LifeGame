import time
import os
import sys
import random as rn


def chance(_chance: int):
    return rn.randint(0, 100) <= _chance


class Clock:
    def __init__(self):
        self.time = time.time()

    def elapsed(self):
        return time.time() - self.time

    def restart(self):
        self.time = time.time()


class Surface:
    def __init__(self, width, height, rock_gen_rate, creature_gen_rate):
        self.cells = [[' ' for i in range(width)] for y in range(height)]
        self.width = width
        self.height = height
        self.rock_gen_rate = rock_gen_rate
        self.creature_gen_rate = creature_gen_rate
        self.gen_rocks()
        self.gen_creatures()

    def get_cell(self, x, y):
        return self.cells[y][x]

    def set_cell(self, x, y, value):
        self.cells[y][x] = value

    def gen_rocks(self):
        for y in range(self.height):
            for x in range(self.width):
                if chance(self.rock_gen_rate):
                    self.set_cell(x, y, 'С')

    def gen_creatures(self):
        for y in range(self.height):
            for x in range(self.width):
                if chance(self.creature_gen_rate) and self.get_cell(x, y) == ' ':
                    self.set_cell(x, y, 'Р' if rn.randint(0, 1) == 0 else 'К')

    def get_neighbours(self, x, y):
        _neighbours = []
        if x > 0:
            _neighbours.append(self.get_cell(x-1, y))
            if y > 0:
                _neighbours.append(self.get_cell(x-1, y-1))
            if y < self.height-1:
                _neighbours.append(self.get_cell(x-1, y+1))
        if x < self.width-1:
            _neighbours.append(self.get_cell(x+1, y))
            if y > 0:
                _neighbours.append(self.get_cell(x+1, y-1))
            if y < self.height-1:
                _neighbours.append(self.get_cell(x+1, y+1))
        if y > 0:
            _neighbours.append(self.get_cell(x, y-1))
        if y < self.height-1:
            _neighbours.append(self.get_cell(x, y+1))
        return _neighbours

    def kill_creatures(self):
        for y in range(self.height):
            for x in range(self.width):
                curr_creature = self.get_cell(x, y)
                neighbours_count = self.get_neighbours(x, y).count(curr_creature)
                if neighbours_count >= 4 or neighbours_count < 2:
                    self.set_cell(x, y, ' ')

    def create_creatures(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) == ' ':
                    neighbours = self.get_neighbours(x, y)
                    fish_count = neighbours.count('Р')
                    shrimp_count = neighbours.count('К')
                    if fish_count > shrimp_count:
                        if fish_count == 3:
                            self.set_cell(x, y, 'Р')
                    else:
                        if shrimp_count == 3:
                            self.set_cell(x, y, 'К')


class Game:
    def __init__(self, width, height, rock_gen_rate, creature_gen_rate, speed):
        self.speed = speed
        self.surface = Surface(width, height, rock_gen_rate, creature_gen_rate)
        self.clock = Clock()

    def run(self):
        self.clear()
        self.display()
        self.clock.restart()

        while True:
            if self.clock.elapsed() > self.speed:

                self.clear()

                self.surface.kill_creatures()
                self.surface.create_creatures()

                self.display()

                self.clock.restart()

    @staticmethod
    def clear():
        os.system("cls")

    def display(self):
        print()
        print('*' * (self.surface.width + 2))
        for y in range(self.surface.height):
            print('*', end='')
            for x in range(self.surface.width):
                print(self.surface.get_cell(x, y), end='')
            print('*')

        print('*' * (self.surface.width + 2))


def main():
    if len(sys.argv) == 1:
        print("Enter args with comma and space between them:\nWidth: _, Height: _, ChanceToGenRock: _,"
              "ChanceToGenCreature: _, GameSpeed: _")
        args = input().split(", ")
        args = [int(i) for i in args]
    else:
        args = [int(sys.argv[i]) for i in range(1, len(sys.argv))]
    game = Game(*args)
    game.run()


if __name__ == "__main__":
    main()
