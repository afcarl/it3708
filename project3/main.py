import argparse
import agent
import grid
import gfx


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        self.args, unknown_args = arg_parser.parse_known_args()
        self.agent = agent.Agent()
        self.grid = grid.Grid()
        self.gfx = gfx.Gfx()

        self.run()

    def run(self):
        self.gfx.draw(self.grid)


if __name__ == '__main__':
    Main()
