import sys
import os
from beer_tracker import BeerTracker
import json
from rnn import Rnn
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project2.individual import Individual
from project2.genotype import Genotype
from project2.problem import Problem


class BeerTrackerGenotype(Genotype):
    num_input_nodes = 5
    num_hidden_nodes = 5
    num_output_nodes = 2
    bits_per_weight = 8
    rnn = Rnn(num_input_nodes, num_hidden_nodes, num_output_nodes)
    GENOTYPE_SIZE = rnn.num_edges * bits_per_weight


class BeerTrackerProblem(Problem):
    population = None
    dynamic_mode = False
    num_scenarios = 1

    @staticmethod
    def calculate_fitness(individual):
        punishment = 3.0  # punishment for partial captures, small misses and large captures
        fitness_sum = 0
        for i in range(BeerTrackerProblem.num_scenarios):
            seed = i + (997 * BeerTrackerProblem.population.generation if BeerTrackerProblem.dynamic_mode else 0)

            beer_tracker = BeerTracker(
                nn=individual.phenotype,
                seed=seed
            )
            beer_tracker.run()
            fitness = (
                1 * beer_tracker.world.agent.num_small_captures +
                (-punishment) * beer_tracker.world.agent.num_partial_captures +
                (-punishment) * beer_tracker.world.agent.num_small_misses +
                (-punishment) * beer_tracker.world.agent.num_large_captures
            )

            if fitness < 0:
                fitness = math.exp(0.1 * fitness)
            else:
                fitness += 1

            fitness_sum += fitness

        fitness = fitness_sum / BeerTrackerProblem.num_scenarios
        is_solution = False  # I could implement this, but it seems I don't need it

        return fitness, is_solution

    @staticmethod
    def post_run_hook(population):
        fittest_individual = population.get_fittest_individual()
        with open('best_individual.json', 'w') as individual_file:
            json.dump(fittest_individual.phenotype.weights, individual_file)


class BeerTrackerIndividual(Individual):
    range_map = {
        'weight': (-5.0, 5.0),
        'bias_weight': (-10.0, 0.0),
        'gain': (1.0, 5.0),
        'time_constant': (1.0, 2.0)
    }

    def calculate_summed_weight(self, i, range_key):
        j = i * BeerTrackerGenotype.bits_per_weight
        weight = sum(self.genotype.dna[j:j + BeerTrackerGenotype.bits_per_weight])
        weight = self.range_map[range_key][0] + \
                 (self.range_map[range_key][1] - self.range_map[range_key][0]) * \
                 float(weight) / BeerTrackerGenotype.bits_per_weight
        return weight

    def calculate_bitshifted_weight(self, i, range_key):
        j = i * BeerTrackerGenotype.bits_per_weight
        bits = self.genotype.dna[j:j + BeerTrackerGenotype.bits_per_weight]
        weight = 0
        for bit in bits:
            weight = (weight << 1) | bit
        weight = self.range_map[range_key][0] + \
                 (self.range_map[range_key][1] - self.range_map[range_key][0]) * \
                 float(weight) / (2 ** BeerTrackerGenotype.bits_per_weight)
        return weight

    def calculate_phenotype(self):
        self.phenotype = Rnn(
            BeerTrackerGenotype.num_input_nodes,
            BeerTrackerGenotype.num_hidden_nodes,
            BeerTrackerGenotype.num_output_nodes
        )

        weights = []

        for i in range(BeerTrackerGenotype.rnn.edge_chunks['input_hidden']):
            weight = self.calculate_bitshifted_weight(i, 'weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['hidden_hidden']):
            weight = self.calculate_bitshifted_weight(i, 'weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['bias_hidden']):
            weight = self.calculate_bitshifted_weight(i, 'bias_weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['hidden_output']):
            weight = self.calculate_bitshifted_weight(i, 'weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['bias_output']):
            weight = self.calculate_bitshifted_weight(i, 'bias_weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['output_output']):
            weight = self.calculate_bitshifted_weight(i, 'weight')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['hidden_gains']):
            weight = self.calculate_bitshifted_weight(i, 'gain')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['output_gains']):
            weight = self.calculate_bitshifted_weight(i, 'gain')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['hidden_time_constants']):
            weight = self.calculate_bitshifted_weight(i, 'time_constant')
            weights.append(weight)
        for i in range(BeerTrackerGenotype.rnn.edge_chunks['output_time_constants']):
            weight = self.calculate_bitshifted_weight(i, 'time_constant')
            weights.append(weight)

        self.phenotype.set_weights(weights)
