import unittest
import surprising_sequences


class TestSurprisingSequencesProblem(unittest.TestCase):
    def assert_fitness(self, mode, dna, should_be_surprising):
        surprising_sequences.SurprisingSequencesProblem.MODE = mode
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet_by_size(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = dna
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        if should_be_surprising:
            self.assertAlmostEqual(fitness, 1.0)
        else:
            self.assertLess(fitness, 1.0)

    def test_fitness_global1(self):
        self.assert_fitness('global', [0, 1, 2], should_be_surprising=True)

    def test_fitness_global2(self):
        self.assert_fitness('global', [0, 1, 2, 2, 1, 0], should_be_surprising=True)

    def test_fitness_global3(self):
        self.assert_fitness('global', [0, 0, 1, 2, 2], should_be_surprising=False)

    def test_fitness_global4(self):
        self.assert_fitness('global', [0, 1, 1, 0, 2, 2, 0], should_be_surprising=False)

    def test_fitness_local1(self):
        self.assert_fitness('local', [0, 0, 1, 2, 2], should_be_surprising=True)

    def test_fitness_local2(self):
        self.assert_fitness('local', [0, 1, 1, 0, 2, 2, 0], should_be_surprising=True)

    def test_fitness_local3(self):
        self.assert_fitness('local', [0, 1, 2, 1, 2], should_be_surprising=False)

    def test_phenotype(self):
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = [0, 1, 2]
        individual = surprising_sequences.SurprisingSequencesIndividual(g1)
        self.assertEqual(individual.phenotype, [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
