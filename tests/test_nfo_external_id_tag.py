import pytest

from mdcx.config.enums import Website
from mdcx.core.nfo import get_external_id_tag_name


@pytest.mark.parametrize(
    "input_site, expected_tag_name",
    [
        (Website.JAVBUS, "javbusid"),
        (Website.JAVDB, "javdbid"),
        (Website.DMM, "dmmid"),
        (Website.MMTV, "mmtvid"),
        ("123SITE", "SITEid"),
        ("abc123Site", "Siteid"),
        ("ABC", "ABCid"),
        ("", "siteid"),
        (None, "siteid"),
    ],
)
def test_get_external_id_tag_name(input_site, expected_tag_name):
    """Test that get_external_id_tag_name correctly formats external id tags"""
    result = get_external_id_tag_name(input_site)
    assert result == expected_tag_name
