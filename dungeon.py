import random
import geometry


class DungeonPartition(geometry.Rectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.fpart = None
        self.spart = None
        self.room = None

    def partition(self, depth):
        if depth < 1:
            return 1
        elif random.random() < 0.5:
            bound = self.w // 2
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h)
            self.spart = DungeonPartition(self.x+bound, self.y, self.w-bound, self.h)
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        else:
            bound = self.h // 2
            self.fpart = DungeonPartition(self.x, self.y, self.w, bound)
            self.spart = DungeonPartition(self.x, self.y+bound, self.w, self.h-bound)
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)

    def fill_array(self, array, depth=0):
        if self.fpart:
            self.spart.fill_array(array, depth+1)
            self.fpart.fill_array(array, depth+1)
        else:
            for x in range(self.x+1, self.xe):
                for y in range(self.y+1, self.ye):
                    array[y][x] = ' '


class DungeonFloor(DungeonPartition):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def partition(self, depth):
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

if __name__ == '__main__':
    init = input('W, H, R: ').split()
    d = DungeonFloor(0, 0, int(init[0]), int(init[1]))
    print('\n')
    print("Number of Rooms: ", d.partition(int(init[2])))
    print()
    array = [['#' for _ in range(d.w)] for _ in range(d.h)]
    d.fill_array(array)
    s = '\n'.join(''.join(row) for row in array)
    print(s)