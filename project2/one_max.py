from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse


class OneMaxGenotype(Genotype):
    GENOTYPE_SIZE = 20


class OneMaxProblem(Problem):
    @staticmethod
    def parse_args():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-s',
            '--genotype-size',
            dest='genotype_size',
            help='Number of bits in a genotype',
            type=int,
            required=False,
            default=OneMaxGenotype.GENOTYPE_SIZE
        )
        args, unknown_args = arg_parser.parse_known_args()
        OneMaxGenotype.GENOTYPE_SIZE = args.genotype_size

    @staticmethod
    def calculate_fitness(individual):
        return sum(individual.phenotype)


class OneMaxIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
