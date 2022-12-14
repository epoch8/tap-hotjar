"""HotJar tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_hotjar.streams import (
    HotJarStream,
    SurveysStream,
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    SurveysStream,
]


class TapHotJar(Tap):
    """HotJar tap class."""
    name = "tap-hotjar"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "email",
            th.StringType,
            required=True,
            description="User email"
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="Project IDs to replicate"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapHotJar.cli()
