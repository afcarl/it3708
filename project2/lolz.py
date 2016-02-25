from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse


class LolzGenotype(Genotype):
    GENOTYPE_SIZE = 6


class LolzProblem(Problem):
    ZERO_CAP = 4

    @staticmethod
    def parse_args():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--genotype-size',
            dest='genotype_size',
            help='Number of bits in a genotype',
            type=int,
            required=False,
            default=LolzGenotype.GENOTYPE_SIZE
        )
        arg_parser.add_argument(
            '-z',
            '--zero-cap',
            dest='zero_cap',
            help='The variable referred to as \'z\' in the project description',
            type=int,
            required=False,
            default=LolzProblem.ZERO_CAP
        )
        args, unknown_args = arg_parser.parse_known_args()
        LolzGenotype.GENOTYPE_SIZE = args.genotype_size
        LolzProblem.ZERO_CAP = args.zero_cap

    @staticmethod
    def calculate_fitness(individual):
        zero_score = 0
        one_score = 0
        zero_streak = True
        one_streak = True

        for x in individual.phenotype:
            if x == 0 and zero_streak:
                zero_score += 1
                one_streak = False
            elif x == 1 and one_streak:
                one_score += 1
                zero_streak = False
            else:
                break

        if zero_score > LolzProblem.ZERO_CAP:
            zero_score = LolzProblem.ZERO_CAP

        raw_fitness = max(zero_score, one_score)
        is_solution = raw_fitness == LolzGenotype.GENOTYPE_SIZE
        scaled_fitness = float(raw_fitness) / LolzGenotype.GENOTYPE_SIZE
        return scaled_fitness, is_solution


class LolzIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
