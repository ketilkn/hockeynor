from datetime import datetime
from hockeynor import upcoming



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


def test_transform():
    result = upcoming.transform(TEST_DATA)
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
    assert upcoming.build_url() == 'https://www.hockey.no/MatchResultSliderBlock/Load'