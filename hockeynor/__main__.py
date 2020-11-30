import logging
from pprint import pprint
import sys

import hockeynor.scoreboard

LOG = logging.getLogger(__name__)


def main():
    import sys
    import argparse
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.INFO if "--debug" not in sys.argv else logging.DEBUG,
                        format=log_format)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true')

    arguments = arg_parser.parse_args()

    score = hockeynor.scoreboard.load()

    hockeynor.scoreboard.print_scoreboard(score)

    return score


r = None
if __name__ == '__main__':
    r = main()
    if bool(getattr(sys, 'ps1', sys.flags.interactive)):
        print('Result of main() stored in variable r')