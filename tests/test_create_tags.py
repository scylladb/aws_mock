from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import Mock

    from tests.conftest import RunQueryFunc


def test_instance_tags(run_query: RunQueryFunc, mongo: Mock) -> None:
    mongo().aws_mock["i"].find_one.return_value = {"_id": "MOCKED_ID"}
    response = run_query({
        "Action": "CreateTags",
        "Version": "2016-11-15",
        "ResourceId.1": "i-12345",
        "Tag.1.Key": "tag1",
        "Tag.1.Value": "val1",
        "Tag.2.Key": "tag2",
        "Tag.2.Value": "val2",
    })
    assert b"CreateTagsResponse" in response.data
    assert b"<return>true</return>" in response.data
    mongo().aws_mock["i"].find_one.assert_called_once_with({"id": "i-12345"})
    mongo().aws_mock["i"].update_one.assert_called_once_with(
        filter={"_id": "MOCKED_ID"},
        update={"$set": {"tags": {
            "tag1": "val1",
            "tag2": "val2",
        }}},
    )
