import random
import geometry


class DungeonPartition(geometry.Rectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.fpart = None
        self.spart = None
        self.room = None

    def partition(self, depth):
        # print('Partition at {}: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(depth, self.x, self.y, self.xe, self.ye, self.w, self.h))
        if depth < 1:
            print('Partition at {}: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(depth, self.x, self.y, self.xe, self.ye, self.w, self.h))
            # print("\tTerminating")
            return 1
        elif depth & 0x1 and (True or random.random() < 0.5):
            bound = self.center.x
            self.fpart = DungeonPartition(self.x, self.y, bound, self.h)
            self.spart = DungeonPartition(bound, self.y, self.w-bound, self.h)
            # print('\tBounds: {}'.format(bound))
            # print('\tVertical Split')
            # print('\t\tFirst Partition: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(self.fpart.x, self.fpart.y, self.fpart.xe, self.fpart.ye, self.fpart.w, self.fpart.h))
            # print('\t\tSecond Partition: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(self.spart.x, self.spart.y, self.spart.xe, self.spart.ye, self.spart.w, self.spart.h))
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)
        else:
            bound = self.center.y
            self.fpart = DungeonPartition(self.x, self.y, self.w, bound)
            self.spart = DungeonPartition(self.x, bound, self.w, self.h-bound)
            # print('\tBounds: {}'.format(bound))
            # print('\tHorizontal Split')
            # print('\t\tFirst Partition: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(self.fpart.x, self.fpart.y, self.fpart.xe, self.fpart.ye, self.fpart.w, self.fpart.h))
            # print('\t\tSecond Partition: x {}, y {}, xe {}, ye {}, w {}, h {}'.format(self.spart.x, self.spart.y, self.spart.xe, self.spart.ye, self.spart.w, self.spart.h))
            return self.fpart.partition(depth-1) + self.spart.partition(depth-1)

    def fill_array(self, array, depth=0):
        if self.fpart:
            self.spart.fill_array(array, depth+1)
            self.fpart.fill_array(array, depth+1)
        for x in range(self.x, self.xe):
            array[self.y][x] = chr(65+depth)
            # array[self.ye-1][x] = chr(65+depth)
        for y in range(self.y, self.ye):
            array[y][self.x] = chr(65+depth)
            # array[y][self.xe-1] = chr(65+depth)


if __name__ == '__main__':
    init = input('W, H, R: ').split()
    d = DungeonPartition(0, 0, int(init[0]), int(init[1]))
    print('\n')
    print("Number of Rooms: ", d.partition(int(init[2])))
    print()
    array = [[' ' for _ in range(d.w)] for _ in range(d.h)]
    d.fill_array(array)
    s = '\n'.join(''.join(row) for row in array)
    print(s)