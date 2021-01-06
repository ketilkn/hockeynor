from datetime import datetime, date
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


def filter_datetime(matches: typing.List[typing.Dict], start: datetime=None, end: datetime = None, day: datetime=None) -> typing.List[typing.Dict]:
    first, last = datetime(1977, 4, 29, 0, 0), datetime(2100, 12, 31, 23, 59)
    if day:
        first, last = day.replace(hour=0, minute=0), day.replace(hour=23, minute=59)
    elif start:
        first = start
        last = end if end else datetime(2100, 12, 31)
        if first == last:
            last = first.replace(hour=23, minute=59)

    return [m for m in matches if first <= m['start_date'] <= last]


def today(matches: typing.List[typing.Dict]):
    return filter_datetime(matches, day=datetime.today())


def past(matches: typing.List[typing.Dict]):
    return filter_datetime(matches, start=datetime(1977, 4, 29), end=datetime.today().replace(hour=0, minute=0))


def future(matches: typing.List[typing.Dict]):
    return filter_datetime(matches, start=datetime.today().replace(hour=23, minute=59))


def main():
    import sys
    import argparse
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.INFO if "--debug" not in sys.argv else logging.DEBUG,
                        format=log_format)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true')
    arg_parser.add_argument('--pprint', action='store_true')
    arg_parser.add_argument('--past', action='store_true')
    arg_parser.add_argument('--today', action='store_true')
    arg_parser.add_argument('--future', action='store_true')

    #arg_parser.add_argument('--infile', nargs='?', type=argparse.FileType('r', encoding='utf8'), default=sys.stdin)

    arguments = arg_parser.parse_args()

    result = load()
    if any([arguments.future, arguments.past, arguments.today]):
        filtered = []
        if arguments.past:
            filtered = filtered + past(result)
        if arguments.today:
            filtered = filtered + today(result)
        if arguments.future:
            filtered = filtered + future(result)
        result = filtered

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