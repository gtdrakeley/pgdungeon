class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Rectangle(Point):
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.xe, self.ye = x + w, y + h
        self.w, self.h = w, h
        self.center = Point((self.xe - self.x) // 2,
                            (self.ye - self.y) // 2)

    def grid(self, grid):
        for x in range(self.x+1, self.xe):
            for y in range(self.y+1, self.ye):
                grid[y][x] = ' '
