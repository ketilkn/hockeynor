from datetime import datetime
import logging
import json
from pprint import pprint
import sys
import typing

import requests

LOG = logging.getLogger(__name__)


def build_url():
    return 'https://www.hockey.no/MatchResultSliderBlock/Load'


def transform(text: str) -> typing.Dict:
    live = json.loads(text)

    result = []
    for match in live['Matches']:
        d = match['StartDate'].replace('/Date(','').replace('000)/', '')
        result.append(
            {'match_id': match['MatchId'],
             'home': match['HomeTeamShortName'].strip(),
             'home_score': match['HomeTeamScore'],
             'away_score': match['AwayTeamScore'],
             'away': match['AwayTeamShortName'].strip(),

             'start_date': datetime.fromtimestamp(int(d))}
        )

    return result


def load():
    response = requests.get(url=build_url())

    if not response:
        LOG.error('Problem downloading matches {} {}'.format(response.status_code, response.reason))
        return

    matches = transform(response.text)

    return matches


def main():
    import sys
    import argparse
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.INFO if "--debug" not in sys.argv else logging.DEBUG,
                        format=log_format)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true')
    arg_parser.add_argument('--pprint', action='store_true')
    #arg_parser.add_argument('--infile', nargs='?', type=argparse.FileType('r', encoding='utf8'), default=sys.stdin)

    arguments = arg_parser.parse_args()

    result = load()

    if arguments.pprint:
        pprint(result, indent=2)
    else:
        print_scoreboard(result)
    return result


def print_scoreboard(result):
    prev = None
    for match in result:
        print(match['start_date'] if not prev or prev['start_date'] != match['start_date'] else '                   ',
              match['home'], '-', match['away'],
              '({}-{})'.format(match['home_score'], match['away_score']) if match['home_score'] else '')
        prev = match


r = None
if __name__ == '__main__':
    r = main()
    if bool(getattr(sys, 'ps1', sys.flags.interactive)):
        print('Result of main() stored in variable r')