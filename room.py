import random
import geometry
from utils import percent


class Room(geometry.Rectangle):
    @classmethod
    def from_constraints(cls, origin, dims, wrange, hrange, mdim=None):
        if mdim:
            min_w = max(percent(dims[0], wrange[0]), mdim[0])
            max_w = max(percent(dims[0], wrange[1]), mdim[0])
            min_h = max(percent(dims[1], hrange[0]), mdim[1])
            max_h = max(percent(dims[1], hrange[1]), mdim[1])
        else:
            min_w = percent(dims[0], wrange[0])
            max_w = percent(dims[0], wrange[1])
            min_h = percent(dims[1], hrange[0])
            max_h = percent(dims[1], hrange[1])
        w = random.randint(min_w, max_w)
        h = random.randint(min_h, max_h)
        x = random.randint(origin[0], origin[0]+max_w-w)
        y = random.randint(origin[1], origin[1]+max_h-h)
        return cls(x, y, w, h)

    def to_grid(self, grid):
        for x in range(self.x+1, self.xe):
            for y in range(self.y+1, self.ye):
                grid[y][x] = ' '
