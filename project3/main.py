import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project2.population import Population
import argparse
import json
import ga


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--adult-selection-method',
            dest='adult_selection_method',
            type=str,
            choices=['full_generational_replacement', 'over_production', 'generational_mixing'],
            required=False,
            default="generational_mixing"
        )
        arg_parser.add_argument(
            '--parent-selection-method',
            dest='parent_selection_method',
            type=str,
            choices=['fitness_proportionate', 'sigma_scaling', 'boltzmann_selection', 'tournament_selection'],
            required=False,
            default="fitness_proportionate"
        )
        arg_parser.add_argument(
            '--adult-pool-size',
            dest='adult_pool_size',
            help='Max number of adults in the adult pool',
            type=int,
            required=False,
            default=10
        )
        arg_parser.add_argument(
            '-p',
            '--population-size',
            dest='population_size',
            help='Number of genotypes in a population',
            type=int,
            required=False,
            default=20
        )
        arg_parser.add_argument(
            '-g',
            '--num-generations',
            dest='num_generations',
            help='Number of generations',
            type=int,
            required=False,
            default=20
        )
        arg_parser.add_argument(
            '--num-runs',
            dest='num_runs',
            help='Number of runs',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--crossover-rate',
            dest='crossover_rate',
            help='Probability of sexual reproduction (two parents) instead of asexual reproduction (one parent)',
            type=float,
            required=False,
            default=0.5
        )
        arg_parser.add_argument(
            '--mutation-rate',
            dest='mutation_rate',
            help='Probability of gene mutation in new genotypes',
            type=float,
            required=False,
            default=0.5
        )
        arg_parser.add_argument(
            '--stop-early',
            nargs='?',
            dest='stop_early',
            help='Stop when (if) a solution is found, and output a representation of the solution',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--silent',
            nargs='?',
            dest='silent',
            help='Add this flag for the program to be less verbose',
            const=True,
            required=False,
            default=False
        )

        self.args, unknown_args = arg_parser.parse_known_args()

        if self.args.adult_pool_size < 1 or self.args.adult_pool_size > self.args.population_size:
            raise Exception('adult_pool_size must be a positive integer that is not greater than population_size')
        if self.args.crossover_rate < 0.0 or self.args.crossover_rate > 1.0:
            raise Exception('crossover_rate must be between 0.0 and 1.0')
        if self.args.mutation_rate < 0.0 or self.args.mutation_rate > 1.0:
            raise Exception('mutation_rate must be between 0.0 and 1.0')

        ga.FlatLandProblem.parse_args()
        self.problem_class = ga.FlatLandProblem
        self.genotype_class = ga.FlatLandGenotype
        self.individual_class = ga.FlatLandIndividual

        logs = []
        for i in range(self.args.num_runs):
            population = self.run()
            logs.append(population.log)

        with open('logs.json', 'w') as log_file:
            json.dump(logs, log_file)

    def run(self):
        self.problem_class.pre_run_hook()

        population = Population(
            self.args.population_size,
            self.problem_class,
            self.genotype_class,
            self.individual_class,
            self.args.adult_selection_method,
            self.args.parent_selection_method,
            self.args.adult_pool_size,
            self.args.crossover_rate,
            self.args.mutation_rate
        )
        self.problem_class.population = population

        for generation in range(self.args.num_generations):
            if not self.args.silent:
                print '---------'
                print 'generation', generation

            population.set_generation(generation)
            population.generate_phenotypes()
            population.evaluate_all()
            if self.args.stop_early and population.is_solution_found:
                print 'A solution has been found in generation {}:'.format(generation)
                print population.solution
                break
            population.adult_selection_handler.select_adults()
            population.log_stats(self.args.silent)
            population.parent_selection_handler.select_parents()
            population.reproduce()

        self.problem_class.post_run_hook(population)

        return population


if __name__ == '__main__':
    Main()
