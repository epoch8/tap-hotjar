"""Stream type classes for tap-hotjar."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hotjar.client import HotJarStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.



class GroupsStream(HotJarStream):
    """Define custom stream."""
    name = "groups"
    path = "/v2/users/me"
    schema = th.PropertiesList(
        th.Property("access_key", th.StringType),
        th.Property("user_id", th.StringType),
    ).to_dict()
