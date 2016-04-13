from beer_tracker import BeerTracker
import json
import argparse
import gfx
from rnn import Rnn
from ga import BeerTrackerGenotype, BeerTrackerPullGenotype, BeerTrackerWallGenotype


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--scenario',
        dest='scenario',
        type=str,
        choices=['standard', 'pull', 'wall'],
        required=False,
        default="standard"
    )
    arg_parser.add_argument(
        '--mode',
        dest='mode',
        type=str,
        choices=['static', 'dynamic'],
        required=False,
        default="static"
    )
    arg_parser.add_argument(
        '--num-scenarios',
        dest='num_scenarios',
        help='Number of scenarios per agent per generation',
        type=int,
        required=False,
        default=1
    )
    arg_parser.add_argument(
        '-g',
        '--generation',
        dest='generation',
        help='If dynamic mode, this specifies which generation to pick board(s) from',
        type=int,
        required=False,
        default=0
    )

    args = arg_parser.parse_args()
    with open('best_individual.json') as best_agent_weights:
        weights = json.load(best_agent_weights)

    if args.scenario == 'pull':
        genotype_class = BeerTrackerPullGenotype
    elif args.scenario == 'wall':
        genotype_class = BeerTrackerWallGenotype
    else:
        genotype_class = BeerTrackerGenotype

    nn = Rnn(
        num_input_nodes=genotype_class.num_input_nodes,
        num_hidden_nodes=genotype_class.num_hidden_nodes,
        num_output_nodes=genotype_class.num_output_nodes
    )
    nn.set_weights(weights)

    g = gfx.Gfx()
    g.fps = 8

    for i in range(args.num_scenarios):
        seed = i + ((997 * args.generation) if args.mode == 'dynamic' else 0)
        print '---', 'seed', seed, '---'
        bt = BeerTracker(
            nn=nn,
            seed=seed,
            scenario=args.scenario
        )
        bt.gfx = g
        bt.run()
        print bt.world.agent.num_small_misses, 'small miss(es)'
        print bt.world.agent.num_large_misses, 'large miss(es)'
        print bt.world.agent.num_partial_captures, 'partial capture(s)'
        print bt.world.agent.num_small_captures, 'small capture(s)'
        print bt.world.agent.num_large_captures, 'large capture(s)'
        if args.scenario == 'pull':
            print bt.world.agent.num_good_pulls, 'good pulls'
            print bt.world.agent.num_bad_pulls, 'bad pulls'
