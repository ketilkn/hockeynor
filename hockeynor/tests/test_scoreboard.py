from datetime import datetime, date
from hockeynor import scoreboard



TEST_DATA = """{"Matches": [ 
{ "MatchId": 7267686,
  "HomeTeamShortName": "  Stavanger Ishockeyklubb  ",
  "AwayTeamShortName": "Sparta Elite   ",
  "HomeTeamScore": 5,
  "AwayTeamScore": 4,
  "FetchScoreFromRaven": false,
  "StartDate": "/Date(1603382400000)/",
  "FormattedDate": "22.10.2020",
  "FormattedShortDate": "22.10",
  "FormattedStartTime": "18:00"},
{   "MatchId": 7267685,
    "HomeTeamShortName": "Narvik",
    "AwayTeamShortName": "Manglerud Star Elite",
    "HomeTeamScore": 1,
    "AwayTeamScore": 3,
    "FetchScoreFromRaven": false,
    "StartDate": "/Date(1603384200000)/",
    "FormattedDate": "22.10.2020",
    "FormattedShortDate": "22.10",
    "FormattedStartTime": "18:30" },
{
            "MatchId": 7267710,
            "HomeTeamShortName": "Frisk Asker Elite   ",
            "AwayTeamShortName": "Manglerud Star Elite",
            "HomeTeamScore": null,
            "AwayTeamScore": null,
            "FetchScoreFromRaven": false,
            "StartDate": "/Date(1605456000000)/",
            "FormattedDate": "15.11.2020",
            "FormattedShortDate": "15.11",
            "FormattedStartTime": "17:00"
        }

]}
"""

TEST_MATCHES = [
    {'away': 'SIL', 'away_score': 3, 'home': 'NH', 'home_score': 0, 'match_id': 7267711,
     'start_date': datetime(2020, 11, 14, 16, 0)},
    {'away': 'Grüner', 'away_score': 1, 'home': 'Stjernen Elite', 'home_score': 7, 'match_id': 7267712,
     'start_date': datetime(2020, 11, 14, 16, 0)},
    {'away': 'Oilers', 'away_score': 6, 'home': 'L.I.K', 'home_score': 1, 'match_id': 7267709,
     'start_date': datetime(2020, 11, 14, 18, 0)},
    {'away': 'M/S', 'away_score': 4, 'home': 'F/A', 'home_score': 5, 'match_id': 7267710,
     'start_date': datetime(2020, 11, 15, 17, 0)},
    {'away': 'L.I.K', 'away_score': 4, 'home': 'NH', 'home_score': 1, 'match_id': 7267855,
     'start_date': datetime(2020, 11, 17, 18, 30)},
    {'away': 'L.I.K', 'away_score': 4, 'home': 'NH', 'home_score': None, 'match_id': 7267856,
     'start_date': datetime(2020, 11, 18, 18, 30)},
    {'away': 'Oilers', 'away_score': None, 'home': 'SIL', 'home_score': None, 'match_id': 7267747,
     'start_date': datetime(2020, 12, 8, 19, 0)}]


def test_filter_date():
    result = scoreboard.filter_datetime(TEST_MATCHES, start=datetime(1977, 4, 29))
    assert isinstance(result, list)
    assert len(result) == 7


def test_filter_datetime_for_future():
    future = scoreboard.filter_datetime(TEST_MATCHES, start=datetime(2020, 12, 8))
    assert len(future) == 1
    assert future[0] == TEST_MATCHES[-1]


def test_filter_datetime_for_yesterday():
    yesterday = scoreboard.filter_datetime(TEST_MATCHES, start=datetime(2020, 11, 18, 0, 0), end=datetime(2020, 11, 18, 23, 59))
    assert len(yesterday) == 1
    assert yesterday[0] == TEST_MATCHES[-2]


def test_filter_datetime_for_yesterday_with_no_time_set():
    yesterday = scoreboard.filter_datetime(TEST_MATCHES,
                                           start=datetime(2020, 11, 18),
                                           end=datetime(2020, 11, 18))
    assert len(yesterday) == 1
    assert yesterday[0] == TEST_MATCHES[-2]


def test_filter_datetime_day_in_past():
    october14 = scoreboard.filter_datetime(TEST_MATCHES, day=datetime(2020, 11, 14))
    assert len(october14) == 3
    assert TEST_MATCHES[0] in october14
    assert TEST_MATCHES[1] in october14
    assert TEST_MATCHES[2] in october14


def test_filter_today():
    matches = [
        {'away': 'SIL', 'away_score': 3, 'home': 'NH', 'home_score': 0, 'match_id': 7267711,
         'start_date': datetime(2020, 11, 14, 16, 0)},
        {'away': 'Grüner', 'away_score': 1, 'home': 'Stjernen Elite', 'home_score': 7, 'match_id': 42,
         'start_date': datetime.now()}]

    result = scoreboard.today(matches)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['match_id'] == 42


def test_filter_past():
    matches = [
        {'away': 'SIL', 'away_score': 3, 'home': 'NH', 'home_score': 0, 'match_id': 1,
         'start_date': datetime(2020, 11, 14, 16, 0)},
        {'away': 'Grüner', 'away_score': 1, 'home': 'Stjernen Elite', 'home_score': 7, 'match_id': 42,
         'start_date': datetime.now()}]

    result = scoreboard.past(matches)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['match_id'] == 1


def test_filter_future():
    matches = [
        {'away': 'SIL', 'away_score': 3, 'home': 'NH', 'home_score': 0, 'match_id': 1,
         'start_date': datetime(2099, 11, 14, 16, 0)},
        {'away': 'Grüner', 'away_score': 1, 'home': 'Stjernen Elite', 'home_score': 7, 'match_id': 42,
         'start_date': datetime.now()}]

    result = scoreboard.future(matches)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['match_id'] == 1


def test_transform():
    result = scoreboard.transform(TEST_DATA)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]['home'] == 'Stavanger Ishockeyklubb'
    assert result[0]['away'] == 'Sparta Elite'
    assert result[0]['home_score'] == 5
    assert result[0]['away_score'] == 4
    assert isinstance(result[0]['start_date'], datetime)
    assert result[1]['start_date'] == datetime(year=2020, month=10, day=22, hour=18, minute=30)
    assert result[2]['match_id'] == 7267710




def test_build_url():
    assert scoreboard.build_url() == 'https://www.hockey.no/MatchResultSliderBlock/Load'