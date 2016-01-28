from boid import Boid
import math
import gfx
import object_collection


class Predator(Boid):
    DEFAULT_SPEED = 8
    BOID_COHESION_WEIGHT = .02
    BOID_COHESION_WEIGHT_MULTIPLIER = 1.0
    BOID_ALIGNMENT_WEIGHT = 1
    BOID_ALIGNMENT_WEIGHT_MULTIPLIER = 1.0
    BOID_NEIGHBOUR_DISTANCE_THRESHOLD = 150

    PREDATOR_SEPARATION_WEIGHT = 30
    PREDATOR_NEIGHBOUR_DISTANCE_THRESHOLD = 90

    id_counter = 1

    SIZE = 16
    LINE_THICKNESS = int(0.4 * SIZE)
    LINE_LENGTH = int(1.6 * SIZE)

    def __init__(self):
        super(Predator, self).__init__()

    def update(self):
        nearby_boids = self.get_nearby_boids()
        if len(nearby_boids) > 0:
            # calculate forces
            cohesion_x, cohesion_y = self.calculate_cohesion_force(nearby_boids)
            alignment_x, alignment_y = self.calculate_alignment_force(nearby_boids)

            # apply forces
            self.dx += self.BOID_COHESION_WEIGHT * self.BOID_COHESION_WEIGHT_MULTIPLIER * cohesion_x
            self.dy += self.BOID_COHESION_WEIGHT * self.BOID_COHESION_WEIGHT_MULTIPLIER * cohesion_y
            self.dx += self.BOID_ALIGNMENT_WEIGHT * self.BOID_ALIGNMENT_WEIGHT_MULTIPLIER * alignment_x
            self.dy += self.BOID_ALIGNMENT_WEIGHT * self.BOID_ALIGNMENT_WEIGHT_MULTIPLIER * alignment_y

        nearby_predators = self.get_nearby_predators(self)
        if len(nearby_predators) > 0:
            separation_x, separation_y = self.calculate_separation_force(nearby_predators)

            self.dx += self.PREDATOR_SEPARATION_WEIGHT * separation_x
            self.dy += self.PREDATOR_SEPARATION_WEIGHT * separation_y

        nearby_obstacles = self.get_nearby_obstacles(self)
        if len(nearby_obstacles) > 0:
            separation_x, separation_y = self.calculate_separation_force(nearby_obstacles)

            self.dx += self.OBSTACLE_SEPARATION_WEIGHT * separation_x
            self.dy += self.OBSTACLE_SEPARATION_WEIGHT * separation_y

        # normalize and damp the speed
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        speed_deviation = speed - self.DEFAULT_SPEED
        target_speed = speed - 0.7 * speed_deviation
        self.dx = target_speed * self.dx / speed
        self.dy = target_speed * self.dy / speed

        # move
        self.x += self.dx
        self.y += self.dy
        # wrap around
        self.x = self.x % gfx.Gfx.width
        self.y = self.y % gfx.Gfx.height


def change_multiplier(self, attr_name, factor):
    current_weight_multiplier = getattr(Predator, attr_name, 1.0)
    new_weight_multiplier = min(max(current_weight_multiplier * factor, 0), 10)
    setattr(Predator, attr_name, new_weight_multiplier)
    print "Predator", attr_name, new_weight_multiplier

gfx.Gfx.change_predator_weight_multiplier = change_multiplier


def reset_multipliers(self):
    Predator.BOID_COHESION_WEIGHT_MULTIPLIER = 1.0
    Predator.BOID_ALIGNMENT_WEIGHT_MULTIPLIER = 1.0
    print "Predator multipliers reset"

gfx.Gfx.reset_predator_weight_multipliers = reset_multipliers


def add_predator(self):
    num_predators = int(0.1 * len(object_collection.ObjectCollection.all_predators)) + 1
    for i in range(num_predators):
        object_collection.ObjectCollection.all_predators.append(Predator())
    print '#predators:', len(object_collection.ObjectCollection.all_predators)

gfx.Gfx.add_predator = add_predator


def remove_predator(self):
    num_predators = int(0.1 * len(object_collection.ObjectCollection.all_predators)) + 1
    for i in range(num_predators):
        if len(object_collection.ObjectCollection.all_predators) > 0:
            object_collection.ObjectCollection.all_predators.pop()
    print '#predators:', len(object_collection.ObjectCollection.all_predators)

gfx.Gfx.remove_predator = remove_predator
