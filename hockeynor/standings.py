import json
import logging
from pprint import pprint
import sys
import typing

import requests

LOG = logging.getLogger(__name__)


def _find_model_index(html: str) -> typing.Tuple[int, int]:
    """Find start and end index of model in html
          :raises ValueError on missing model start
          :raises ValueError on missing model end
          :raises ValueError no None model"""
    if html is None:
        raise ValueError('html is None')
    start = html.find('hockey.live.createStandingsViewModel(')
    if start == -1:
        raise ValueError(f'Model not found in html ({len(html)=})')
    end = html[start + 37:].find(');')
    if end == -1:
        raise ValueError(f'Model without an end found in html ({len(html)=})')

    return start + 37, end + start + 37


def find_model(html: str) -> str:
    start, end = _find_model_index(html)
    return html[start: end]


def transform_model_to_json(html: str) -> typing.Dict:
    if html is None:
        raise ValueError('html cannot be None')
    model = find_model(html)
    standings = json.loads(model)

    if not isinstance(standings, dict):
        ValueError('Unexpected {} in html'.format(type(standings)))
    return standings


def build_url() -> str:
    """Build url for standings source"""
    return 'https://www.hockey.no/live/Standings?date=01.11.2020&tournamentid=397960&teamid=0'


def load():
    url = build_url()
    response = requests.get(url)

    if not response:
        LOG.error('Problem downloading standings {} {}'.format(response.status_code, response.reason))
        return []

    standing = transform_model_to_json(response.text)

    return standing


def print_standings(standings):
    print("NO Team                    GP W  OW SW OL SL  L PTS  GF  GA  PIM  PCT")
    for team in standings['Rows']:
        print('{Number:>2} {Name:23} {GP:>2} {W:>2} {OTW:>2} {SOW:>2} {OTL:>2} {SOL:>2} {L:>2} {PTS:>3} {GF:>3} {GA:>3} {PIM:>4} {PCT:>3}'.format(
                **{**{'Number': team['Number'], 'Name': team['Name']},
                **{el['Name']: int(el['Result']) for el in team['Results']}}))



def main():
    import sys
    import argparse
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.INFO if "--debug" not in sys.argv else logging.DEBUG,
                        format=log_format)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true')
    arg_parser.add_argument('--pprint', action='store_true')

    arguments = arg_parser.parse_args()

    result = load()

    if arguments.pprint:
        pprint(result, indent=4)
    else:
        print_standings(result)
    return result


r = None
if __name__ == '__main__':
    r = main()
    if bool(getattr(sys, 'ps1', sys.flags.interactive)):
        print('Result of main() stored in variable r')