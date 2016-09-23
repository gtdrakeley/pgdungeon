import random
import math
import geometry
from utils import interval_scaler


class Room(geometry.Rectangle):
    @classmethod
    def from_constraints(cls, origin, dims, vinterval=(1.0, 1.0)):
        part_x, part_y = origin
        part_w, part_h = dims
        low_variance, high_variance = vinterval
        min_w, max_w = math.floor(part_w * low_variance), math.ceil(part_w * high_variance)
        min_h, max_h = math.floor(part_h * low_variance), math.ceil(part_h * high_variance)
        if min_w == max_w and min_h == max_h:
            w, h = max_w, max_h
        elif min_w == max_w:
            w = max_w
            h = random.randint(min_h, max_h)
        elif min_h == max_h:
            h = max_h
            w = random.randint(min_w, max_w)
        elif max_w - min_w > max_h - min_h:
            scaler = interval_scaler((min_w, max_w), (min_h, max_h))
            w = random.randint(min_w, max_w)
            h = scaler(w)
        else:
            scaler = interval_scaler((min_h, max_h), (min_w, max_w))
            h = random.randint(min_w, max_w)
            w = scaler(h)
        x = random.randint(part_x, part_x+max_w-w)
        y = random.randint(part_y, part_y+max_h-h)
        '''
        print('Part x, y, w, h:', part_x, part_y, part_w, part_h)
        print('Variance l, h:', low_variance, high_variance)
        print('Width m, M:', min_w, max_w)
        print('Height m, M:', min_h, max_h)
        print('Room w, h:', w, h)
        print('Room x, y:', x, y)
        input('[ENTER]')
        print()
        '''
        return cls(x, y, w, h)

    def to_grid(self, grid):
        for x in range(self.x+1, self.xe):
            for y in range(self.y+1, self.ye):
                grid[y][x] = ' '
