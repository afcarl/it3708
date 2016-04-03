import math
from grid import Grid, Item


class Direction:
    East = 0
    North = 90
    West = 180
    South = 270

    DIRECTIONS = {
        0: East,
        90: North,
        180: West,
        270: South
    }

    def __init__(self):
        pass

    @staticmethod
    def rotate(direction, rotation_amount):
        new_direction = (direction + rotation_amount) % 360
        return Direction.DIRECTIONS[new_direction]


class Agent(object):
    FIRING_THRESHOLD = 0.0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.East
        self.grid = None
        self.ann = None
        self.num_food_consumed = 0
        self.num_poison_consumed = 0

    def set_grid(self, grid):
        self.grid = grid
        self.consume_item()

    def set_ann(self, ann):
        self.ann = ann

    def consume_item(self):
        # consume any item at the current position on the grid
        cell = self.grid.get_cell(self.x, self.y)
        if cell != Item.Nothing:
            if cell == Item.Food:
                self.num_food_consumed += 1
            elif cell == Item.Poison:
                self.num_poison_consumed += 1
            self.grid.clear_cell(self.x, self.y)

    def move(self, relative_direction):
        if relative_direction != 0:
            self.direction = Direction.rotate(self.direction, relative_direction)
        rad = math.radians(self.direction)
        self.x = (self.x + int(round(math.cos(rad)))) % Grid.WIDTH
        self.y = (self.y - int(round(math.sin(rad)))) % Grid.HEIGHT
        self.consume_item()

    def sense(self):
        forward_rad = math.radians(self.direction)
        forward_x = (self.x + int(round(math.cos(forward_rad)))) % Grid.WIDTH
        forward_y = (self.y - int(round(math.sin(forward_rad)))) % Grid.HEIGHT
        left_rad = math.radians(self.direction + 90)
        left_x = (self.x + int(round(math.cos(left_rad)))) % Grid.WIDTH
        left_y = (self.y - int(round(math.sin(left_rad)))) % Grid.HEIGHT
        right_rad = math.radians(self.direction - 90)
        right_x = (self.x + int(round(math.cos(right_rad)))) % Grid.WIDTH
        right_y = (self.y - int(round(math.sin(right_rad)))) % Grid.HEIGHT

        forward_cell = self.grid.get_cell(forward_x, forward_y)
        left_cell = self.grid.get_cell(left_x, left_y)
        right_cell = self.grid.get_cell(right_x, right_y)

        return (
            1 if forward_cell == Item.Food else 0,
            1 if left_cell == Item.Food else 0,
            1 if right_cell == Item.Food else 0,
            1 if forward_cell == Item.Poison else 0,
            1 if left_cell == Item.Poison else 0,
            1 if right_cell == Item.Poison else 0
        )

    def move_autonomously(self):
        sensor_data = self.sense()
        motor_output = self.ann.activate(sensor_data)
        max_motor_output = max(motor_output)
        if max_motor_output > self.FIRING_THRESHOLD:
            argmax = motor_output.index(max_motor_output)
            direction = (argmax - 1) * 90
            self.move(direction)
