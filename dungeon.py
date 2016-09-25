import random
import geometry
import room
import math


class DungeonPartition(geometry.Rectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.fpart = None
        self.spart = None
        self.feature = None

    def partition(self, depth, variance=0.0):
        if depth < 1:
            return 1
        elif random.random() < 0.5:
            offset = self.w / 2 * variance
            bound = random.randint(math.floor(self.w/2 - offset), math.ceil(self.w/2 + offset))
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h)
            self.spart = DungeonPartition(self.x+bound, self.y, self.w-bound, self.h)
            '''
            print('Vertical')
            print('\tOffset, Bound:', offset, bound)
            print('\tPart1 x, y, w, h:', self.x, self.y, bound, self.h)
            print('\tPart2 x, y, w, h:', self.x+bound, self.y, self.w-bound, self.h)
            '''
        else:
            offset = self.h / 2 * variance
            bound = random.randint(math.floor(self.h/2 - offset), math.ceil(self.h/2 + offset))
            self.fpart = DungeonPartition(self.x, self.y, self.w, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w, self.h-bound)
            '''
            print('Horizontal')
            print('\tOffset, Bound:', offset, bound)
            print('\tPart1 x, y, w, h:', self.x, self.y, self.w, bound)
            print('\tPart2 x, y, w, h:', self.x, self.y+bound, self.w, self.h-bound)
            '''
        '''
        input('[ENTER]')
        print()
        '''
        return self.fpart.partition(depth-1, variance) + self.spart.partition(depth-1, variance)

    def generate_rooms(self, vinterval=(1.0, 1.0)):
        if self.fpart:
            self.fpart.generate_rooms(vinterval)
            self.spart.generate_rooms(vinterval)
        else:
            self.feature = room.Room.from_constraints((self.x, self.y), (self.w, self.h), vinterval)

    def gridify(self, grid):
        if self.fpart:
            self.fpart.gridify(grid)
            self.spart.gridify(grid)
        else:
            self.feature.to_grid(grid)


class DungeonFloor(DungeonPartition):
    def __init__(self, w, h):
        super().__init__(0, 0, w, h)

    def partition(self, depth, variance=0.0):
        if depth < 1:
            return 1
        elif random.random() < 0.5:
            offset = (self.w-1) / 2 * variance
            bound = random.randint(math.floor(self.w/2 - offset), math.ceil(self.w/2 + offset))
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h-1)
            self.spart = DungeonPartition(self.x+bound, self.y, self.w-bound-1, self.h-1)
            '''
            print('Vertical')
            print('\tOffset, Bound:', offset, bound)
            print('\tPart1 x, y, w, h:', self.x, self.y, bound, self.h-1)
            print('\tPart2 x, y, w, h:', self.x+bound, self.y, self.w-bound-1, self.h-1)
            '''
        else:
            offset = (self.h-1) / 2 * variance
            bound = random.randint(math.floor(self.h/2 - offset), math.ceil(self.h/2 + offset))
            self.fpart = DungeonPartition(self.x, self.y, self.w-1, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w-1, self.h-bound-1)
            '''
            print('Horizontal')
            print('\tOffset, Bound:', offset, bound)
            print('\tPart1 x, y, w, h:', self.x, self.y, self.w-1, bound)
            print('\tPart2 x, y, w, h:', self.x, self.y+bound, self.w-1, self.h-bound-1)
            '''
        '''
        input('[ENTER]')
        print()
        '''
        return self.fpart.partition(depth-1, variance) + self.spart.partition(depth-1, variance)

    @staticmethod
    def from_prompts():
        uin = input('Floor Width, Height: ')
        w, h = eval(uin)
        d = DungeonFloor(w, h)
        print('Partitioning')
        uin = input('\tNumber of Splits: ')
        depth = int(uin)
        uin = input('\tPartition Variance: ')
        variance = eval(uin)
        d.partition(depth, variance)
        uin = input('Room Variance Interval: ')
        vinterval = eval(uin)
        d.generate_rooms(vinterval)
        grid = [['#' for _ in range(d.w)] for _ in range(d.h)]
        d.gridify(grid)
        s = '\n'.join(''.join(row) for row in grid)
        print('\n\n{}'.format(s))
        return d


if __name__ == '__main__':
    DungeonFloor.from_prompts()
