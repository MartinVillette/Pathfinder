import pygame as py
import sys
from random import uniform

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.position = pos
        self.g = None
        self.h = None
        self.f = None

class PathFinding:
    def __init__(self, mode='grid', grid_size=20):
        self.mode = mode
        self.window()
        self.grid(grid_size)

    def window(self):
        self.window_size = (750, 750)  # Window size
        self.display = py.display.set_mode(self.window_size)  # Create window

    def grid(self, grid_size):
        # Create background
        py.draw.rect(self.display, [0, 0, 0], [0, 0, self.window_size[0], self.window_size[1]])
        
        self.grid_size = (grid_size, grid_size)  # Grid size
        self.border = 2  # Border size between squares
        self.box_size = (min(self.window_size) / min(self.grid_size)) - self.border  # Square size

        # Initialize grid values
        self.grid_values = [[uniform(0, 1) if self.mode == 'noise' else 0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        self.start_point = (0, 0)
        self.end_point = (self.grid_size[0] - 1, self.grid_size[1] - 1)
        self.move_start = self.move_end = False
        self.finish = False

        # Draw initial grid
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.draw_rect(i, j)

    def draw_rect(self, i, j, state=''):
        x, y = int(self.box_size * i + self.border * i), int(self.box_size * j + self.border * j)
        
        if (i, j) == self.start_point:
            color = [255, 0, 0]  # Red for start point
        elif (i, j) == self.end_point:
            color = [0, 255, 0]  # Green for end point
        elif self.grid_values[i][j] == 1:
            color = [30, 30, 30]  # Dark gray for walls
        else:
            if state == 'visited':
                color = [150, 0, 255]  # Purple for visited nodes
            elif state == 'explored':
                color = [0, 150, 255]  # Blue for explored nodes
            elif state == 'final_path':
                color = [150, 150, 255]  # Light blue for final path
            else:
                c = 255 - (self.grid_values[i][j] * 255) if self.mode == 'noise' else 255
                color = [c, c, c]  # Grayscale for empty cells
        
        py.draw.rect(self.display, color, [x, y, self.box_size, self.box_size])

    def draw_path(self, node):
        if node.parent:
            x1, y1 = self.get_center_coords(node.position)
            x2, y2 = self.get_center_coords(node.parent.position)
            py.draw.line(self.display, [255, 200, 0], (x1, y1), (x2, y2), int(self.box_size/3))

    def get_center_coords(self, position):
        i, j = position
        return (int(self.box_size * i + self.border * i + (self.box_size / 2)),
                int(self.box_size * j + self.border * j + (self.box_size / 2)))

    def click_coords(self):
        # Convert mouse position to grid coordinates
        x = int(py.mouse.get_pos()[0] / (self.box_size + self.border))
        y = int(py.mouse.get_pos()[1] / (self.box_size + self.border))
        return x, y

    def left_click(self):
        if self.finish:
            return
        x, y = self.click_coords()

        if self.grid_values[x][y] != 1 and ((x, y) == self.start_point or self.move_start):
            self.move_start = True
            if (x, y) != self.start_point and (x, y) != self.end_point:
                temp = self.start_point
                self.start_point = (x, y)
                self.draw_rect(temp[0], temp[1])
                self.draw_rect(x, y)
        elif self.grid_values[x][y] != 1 and ((x, y) == self.end_point or self.move_end):
            self.move_end = True
            if (x, y) != self.end_point:
                temp = self.end_point
                self.end_point = (x, y)
                self.draw_rect(temp[0], temp[1])
                self.draw_rect(x, y)
        elif self.grid_values[x][y] == 0 and self.mode != 'noise':
            self.grid_values[x][y] = 1
            self.draw_rect(x, y)

    def right_click(self):
        x, y = self.click_coords()
        if self.grid_values[x][y] == 1 and (x, y) != self.start_point and (x, y) != self.end_point and not self.finish:
            self.grid_values[x][y] = 0
            self.draw_rect(x, y)

    def neighbours(self, parent):
        def euclidean(x, y, cost):
            dx = abs(x - self.end_point[0])
            dy = abs(y - self.end_point[1])
            return cost * (dx**2 + dy**2)**.5

        moves = [(0, 1), (-1, 0), (1, 0), (0, -1)]
        for dx, dy in moves:
            x, y = parent.position[0] + dx, parent.position[1] + dy
            if 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1] and (x, y) not in self.visited and self.grid_values[x][y] != 1:
                cost = (self.grid_values[x][y]) * 10 if self.mode == 'noise' else 10

                child_node = Node(parent, (x, y))
                child_node.g = parent.g + cost
                child_node.h = euclidean(x, y, cost)
                child_node.f = child_node.g + child_node.h

                self.to_visit.append(child_node)

        py.display.update()
        self.to_visit.sort(key=lambda x: x.h)

    def a_star_search(self):
        self.start_node = Node(None, self.start_point)
        self.start_node.g = self.start_node.h = self.start_node.f = 0

        self.end_node = Node(None, self.end_point)
        self.end_node.g = self.end_node.h = self.end_node.f = 0

        current_node = self.start_node

        self.visited = [self.start_node.position]
        self.to_visit = []

        while current_node.position != self.end_node.position:
            self.neighbours(current_node)

            if not self.to_visit:
                print('No path found')
                return

            current_node = min(self.to_visit, key=lambda x: x.f)
            self.visited.append(current_node.position)
            self.to_visit = [node for node in self.to_visit if node.position != current_node.position]

        self.draw_final_path(current_node)

    def draw_final_path(self, current_node):
        while current_node.position != self.start_point:
            self.draw_path(current_node)
            current_node = current_node.parent
        self.finish = True

def restart(app, mode=None):
    del app
    return PathFinding(mode)

def main():
    py.init()
    app = PathFinding()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    app.a_star_search()
                if event.key == py.K_r:
                    app = restart(app, app.mode)
                if event.key == py.K_n:
                    app = restart(app, 'noise')
                if event.key == py.K_m:
                    app = restart(app, 'maze')
                if event.key == py.K_g:
                    app = restart(app, 'grid')
            if event.type == py.MOUSEBUTTONUP:
                app.move_start = app.move_end = False

        if py.mouse.get_pressed() == (1, 0, 0):  # Left click
            app.left_click()
        elif py.mouse.get_pressed() == (0, 0, 1):  # Right click
            app.right_click()
        
        py.display.update()

if __name__ == "__main__":
    main()