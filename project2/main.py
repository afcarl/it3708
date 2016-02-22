from population import Population
import argparse


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--problem',
            dest='problem',
            type=str,
            choices=['onemax', 'lolz', 'ss'],
            required=False,
            default="onemax"
        )
        arg_parser.add_argument(
            '--adult-selection-method',
            dest='adult_selection_method',
            type=str,
            choices=['fgr', 'op', 'gm'],  # full generational replacement, over production or generational mixing
            required=False,
            default="gm"
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

        self.args, unknown_args = arg_parser.parse_known_args()

        if self.args.adult_pool_size < 1 or self.args.adult_pool_size > self.args.population_size:
            raise Exception('adult_pool_size must be a positive integer that is not greater than population_size')

        if self.args.problem == 'onemax':
            import one_max
            one_max.OneMaxProblem.parse_args()
            self.problem_class = one_max.OneMaxProblem
            self.individual_class = one_max.OneMaxIndividual
        elif self.args.problem == 'lolz':
            import lolz
            lolz.LolzProblem.parse_args()
            self.problem_class = lolz.LolzProblem
            self.individual_class = lolz.LolzIndividual
        elif self.args.problem == 'ss':  # surprising sequences
            pass  # TODO

        for i in range(self.args.num_runs):
            self.run()

    def run(self):
        population = Population(
            self.args.population_size,
            self.problem_class,
            self.individual_class,
            self.args.adult_selection_method,
            self.args.parent_selection_method,
            self.args.adult_pool_size
        )

        for generation in range(self.args.num_generations):
            print '---------'
            print 'generation', generation

            population.set_generation(generation)

            population.generate_phenotypes()

            population.evaluate_all()

            population.select_adults()

            population.print_stats()

            population.select_parents()

            population.reproduce()


if __name__ == '__main__':
    Main()
