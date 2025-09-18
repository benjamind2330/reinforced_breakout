from learning.agent import train
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train the Breakout agent.")
    parser.add_argument('--gui', action='store_true', help='Enable GUI display during training')
    args = parser.parse_args()

    train(args.gui)