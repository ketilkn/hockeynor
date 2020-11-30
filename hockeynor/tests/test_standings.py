from datetime import datetime

import pytest

from hockeynor import standings


TEST_DATA = """
<html>
<body>
<div> 
  <h1>Standings</h1>
  <table></table>
<script type="text/javascript">
    $(document).ready(function() {
        hockey.live.StandingsViewModel = hockey.live.createStandingsViewModel({"PublicTable":true,"Rows":[{"Id":695546,"Name":"Frisk Asker Elite   ","Number":"1","Results":[{"Name":"GP","Result":"14"},{"Name":"W","Result":"12"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"2"},{"Name":"PTS","Result":"36"},{"Name":"GF","Result":"59"},{"Name":"GA","Result":"27"},{"Name":"PIM","Result":"153"},{"Name":"PCT","Result":"85"}],"TeamUrl":"/live/Statistics/Players?teamid=695546"},{"Id":708311,"Name":"Storhamar Elite     ","Number":"2","Results":[{"Name":"GP","Result":"14"},{"Name":"W","Result":"10"},{"Name":"OTW","Result":"1"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"3"},{"Name":"PTS","Result":"32"},{"Name":"GF","Result":"55"},{"Name":"GA","Result":"31"},{"Name":"PIM","Result":"245"},{"Name":"PCT","Result":"76"}],"TeamUrl":"/live/Statistics/Players?teamid=708311"},{"Id":527810,"Name":"Vålerenga Elite","Number":"3","Results":[{"Name":"GP","Result":"15"},{"Name":"W","Result":"10"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"5"},{"Name":"PTS","Result":"30"},{"Name":"GF","Result":"48"},{"Name":"GA","Result":"34"},{"Name":"PIM","Result":"324"},{"Name":"PCT","Result":"66"}],"TeamUrl":"/live/Statistics/Players?teamid=527810"},{"Id":852911,"Name":"Lillehammer Elite","Number":"4","Results":[{"Name":"GP","Result":"14"},{"Name":"W","Result":"8"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"1"},{"Name":"SOL","Result":"1"},{"Name":"L","Result":"4"},{"Name":"PTS","Result":"26"},{"Name":"GF","Result":"43"},{"Name":"GA","Result":"43"},{"Name":"PIM","Result":"323"},{"Name":"PCT","Result":"61"}],"TeamUrl":"/live/Statistics/Players?teamid=852911"},{"Id":220882,"Name":"Stavanger Ishockeyklubb","Number":"5","Results":[{"Name":"GP","Result":"14"},{"Name":"W","Result":"8"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"6"},{"Name":"PTS","Result":"24"},{"Name":"GF","Result":"53"},{"Name":"GA","Result":"37"},{"Name":"PIM","Result":"164"},{"Name":"PCT","Result":"57"}],"TeamUrl":"/live/Statistics/Players?teamid=220882"},{"Id":695363,"Name":"Stjernen Elite      ","Number":"6","Results":[{"Name":"GP","Result":"15"},{"Name":"W","Result":"6"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"1"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"8"},{"Name":"PTS","Result":"20"},{"Name":"GF","Result":"58"},{"Name":"GA","Result":"57"},{"Name":"PIM","Result":"184"},{"Name":"PCT","Result":"44"}],"TeamUrl":"/live/Statistics/Players?teamid=695363"},{"Id":678819,"Name":"Sparta Elite   ","Number":"7","Results":[{"Name":"GP","Result":"12"},{"Name":"W","Result":"4"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"2"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"6"},{"Name":"PTS","Result":"16"},{"Name":"GF","Result":"36"},{"Name":"GA","Result":"33"},{"Name":"PIM","Result":"114"},{"Name":"PCT","Result":"44"}],"TeamUrl":"/live/Statistics/Players?teamid=678819"},{"Id":720730,"Name":"Manglerud Star Elite","Number":"8","Results":[{"Name":"GP","Result":"12"},{"Name":"W","Result":"4"},{"Name":"OTW","Result":"1"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"2"},{"Name":"L","Result":"5"},{"Name":"PTS","Result":"16"},{"Name":"GF","Result":"42"},{"Name":"GA","Result":"48"},{"Name":"PIM","Result":"240"},{"Name":"PCT","Result":"44"}],"TeamUrl":"/live/Statistics/Players?teamid=720730"},{"Id":600620,"Name":"Grüner              ","Number":"9","Results":[{"Name":"GP","Result":"14"},{"Name":"W","Result":"2"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"1"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"11"},{"Name":"PTS","Result":"7"},{"Name":"GF","Result":"28"},{"Name":"GA","Result":"71"},{"Name":"PIM","Result":"188"},{"Name":"PCT","Result":"16"}],"TeamUrl":"/live/Statistics/Players?teamid=600620"},{"Id":708282,"Name":"Narvik","Number":"10","Results":[{"Name":"GP","Result":"16"},{"Name":"W","Result":"1"},{"Name":"OTW","Result":"0"},{"Name":"SOW","Result":"0"},{"Name":"OTL","Result":"0"},{"Name":"SOL","Result":"0"},{"Name":"L","Result":"15"},{"Name":"PTS","Result":"3"},{"Name":"GF","Result":"31"},{"Name":"GA","Result":"72"},{"Name":"PIM","Result":"221"},{"Name":"PCT","Result":"6"}],"TeamUrl":"/live/Statistics/Players?teamid=708282"}]});
        ko.applyBindings(hockey.live.StandingsViewModel, document.getElementById("standings-page"));

        hockey.tablesort.init();
    });
</script>
</div>
</body>
</html>
"""


def test__find_model_index():
    assert standings._find_model_index('  = hockey.live.createStandingsViewModel({});')[0] == 41
    assert standings._find_model_index('  = hockey.live.createStandingsViewModel({});')[1] == 43


def test__find_model_index_raise_value_error_on_missing_model():
    with pytest.raises(ValueError) as err:
        assert standings._find_model_index('  = hockey.live.createStangsViewModel({});')[0] == 41
    with pytest.raises(ValueError) as err:
        assert standings._find_model_index('  = hockey.live.createStandingsViewModel({;')
    with pytest.raises(ValueError) as err:
        standings._find_model_index(None)


def test_find_model():
    result = standings.find_model(TEST_DATA)
    assert '"Id":695546,"Name":"Frisk Asker Elite   "' in result
    assert result[0] == '{'
    assert result[-1] == '}'


def test_transform_model_to_json():
    result = standings.transform_model_to_json(TEST_DATA)

    assert isinstance(result, dict)
    assert 'Rows' in result
    assert len(result['Rows']) == 10


def test_transform_model_to_json_raise_value_error():
    with pytest.raises(ValueError) as none_is_illegal:
        standings.transform_model_to_json(None)
    with pytest.raises(ValueError) as object_expected:
        standings.transform_model_to_json('<html><script>hockey.live.createStandingsViewModel("eh");')


def test_build_url():
    assert standings.build_url() == 'https://www.hockey.no/live/Standings?date=01.11.2020&tournamentid=397960&teamid=0'