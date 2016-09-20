import random
import geometry
import room


class DungeonPartition(geometry.Rectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.fpart = None
        self.spart = None
        self.feature = None

    def partition(self, depth, mdim=(2, 2), bdim=None):
        if not bdim:
            bdim = mdim
        if depth < 1:
            return 1
        elif self.w <= bdim[0] and self.h <= bdim[1]:
            return 1
        elif self.w <= mdim[0] * 2 and self.h <= mdim[1] * 2:
            return 1
        elif self.w <= mdim[0] * 2 or self.w <= bdim[0]:
            bound = random.randint(mdim[1], self.h-mdim[1])
            self.fpart = DungeonPartition(self.x, self.y, self.w, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w, self.h-bound)
        elif self.h <= mdim[1] * 2 or self.h <= bdim[1]:
            bound = random.randint(mdim[0], self.w-mdim[0])
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h)
            self.spart = DungeonPartition(self.x+bound, self.y, self.w-bound, self.h)
        elif random.random() < 0.5:
            # bound = self.w // 2
            bound = random.randint(mdim[0], self.w-mdim[0])
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h)
            self.spart = DungeonPartition(self.x+bound, self.y, self.w-bound, self.h)
            # return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        else:
            # bound = self.h // 2
            bound = random.randint(mdim[1], self.h-mdim[1])
            self.fpart = DungeonPartition(self.x, self.y, self.w, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w, self.h-bound)
            # return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        return self.fpart.partition(depth - 1, mdim, bdim) + self.spart.partition(depth - 1, mdim, bdim)

    def generate_rooms(self, wrange, hrange, mdim=None):
        if self.fpart:
            self.fpart.generate_rooms(wrange, hrange, mdim)
            self.spart.generate_rooms(wrange, hrange, mdim)
        else:
            self.feature = room.Room.from_constraints((self.x, self.y), (self.w, self.h), wrange, hrange)

    def gridify(self, grid):
        if self.fpart:
            self.fpart.gridify(grid)
            self.spart.gridify(grid)
        else:
            self.feature.to_grid(grid)


class DungeonFloor(DungeonPartition):
    def __init__(self, w, h):
        super().__init__(0, 0, w, h)

    def partition(self, depth, mdim=(2, 2), bdim=None):
        if not bdim:
            bdim = mdim
        if depth < 1:
            return 1
        elif self.w <= bdim[0] and self.h <= bdim[1]:
            return 1
        elif self.w <= mdim[0] * 2 and self.h <= mdim[1] * 2:
            return 1
        elif self.w <= mdim[0] * 2 or self.w <= bdim[0]:
            bound = random.randint(mdim[1], self.h-mdim[1])
            self.fpart = DungeonPartition(self.x, self.y, self.w-1, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w-1, (self.h-1)-bound)
        elif self.h <= mdim[1] * 2 or self.h <= bdim[1]:
            bound = random.randint(mdim[0], self.w-mdim[0])
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h-1)
            self.spart = DungeonPartition(self.x+bound, self.y, (self.w-1)-bound, self.h-1)
        elif random.random() < 0.5:
            # bound = self.w // 2
            bound = random.randint(mdim[0], self.w-mdim[0])
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h-1)
            self.spart = DungeonPartition(self.x+bound, self.y, (self.w-1)-bound, self.h-1)
            # return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        else:
            # bound = self.h // 2
            bound = random.randint(mdim[1], self.h-mdim[1])
            self.fpart = DungeonPartition(self.x, self.y, self.w-1, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w-1, (self.h-1)-bound)
            # return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        return self.fpart.partition(depth - 1, mdim, bdim) + self.spart.partition(depth - 1, mdim, bdim)

    """
    def partition(self, depth, ):
        if depth < 1:
            return 1
        elif random.random() < 0.5:
            bound = (self.w - 1) // 2
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h-1)
            self.spart = DungeonPartition(self.x+bound, self.y, (self.w-1)-bound, self.h-1)
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        else:
            bound = (self.h - 1) // 2
            self.fpart = DungeonPartition(self.x, self.y, self.w-1, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w-1, (self.h-1)-bound)
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
    """

if __name__ == '__main__':
    init = input('W, H, R: ').split()
    d = DungeonFloor(int(init[0]), int(init[1]))
    print('\n')
    print("Number of Rooms: ", d.partition(int(init[2])))
    print()
    d.generate_rooms((100, 100), (100, 100))
    grid = [['#' for _ in range(d.w)] for _ in range(d.h)]
    d.gridify(grid)
    s = '\n'.join(''.join(row) for row in grid)
    print(s)
