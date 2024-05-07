"""HotJar tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_hotjar.streams import (
    HotJarStream,
    SurveysStream,
    B2BUsStream,
    B2BTrStream,
    B2BMexStream,
    B2BCentralAmericaStream,
    B2BIbericaStream,
    B2BFranceExportStream,
    B2BFranceStream,
    B2BGermanExportStream,
    B2BBrasilStream,
    B2BRussiaStream,
    B2BItalyStream,
    B2BGermanStream,
    B2CProdFR,
    B2CProdEN,
    B2CProdES,
    B2CRentFR,
    B2CRideFR,
    ShopEN,
    ShopFR,
    RentEN,
    ABO_NPC_DE,
    B2CProd_FR_CA_NPS,
    B2CProd_EN_CA_NPS,
    B2CProd_IT_NPS,
    B2CProd_DE_DE_NPS,
    B2CProd_EN_DE_NPS,
    B2CProd_USA_NPS,
    B2C_PROD_en_GB_NPS,
    B2C_B2C_PROD_PL_NPS,
    B2C_B2C_PROD_PT_NPS,
    B2C_PROD_ID_ID_NPS,
    B2C_PROD_EN_ID_NPS,
    B2C_PROD_TR_NPS,
    Shop_NPS_IT,
    Shop_NPS_ES,
    Ride_NPS_IT,
    Ride_NPS_ES,
    Rent_NPS_EN,
    B2C_PROD_FR_MA,
    B2C_PROD_FR_TN,
    B2C_PROD_ES_NI,
    B2C_PROD_ES_MX,
    B2C_PROD_PT_BR_NPS,
    B2C_PROD_PT_UK_UA,
    B2C_PROD_ES_SV,
    B2C_PROD_ROMANIAN,
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    SurveysStream,
    B2BUsStream,
    B2BTrStream,
    B2BMexStream,
    B2BCentralAmericaStream,
    B2BIbericaStream,
    B2BFranceExportStream,
    B2BFranceStream,
    B2BGermanExportStream,
    B2BBrasilStream,
    B2BRussiaStream,
    B2BItalyStream,
    B2BGermanStream,
    B2CProdFR,
    B2CProdEN,
    B2CProdES,
    B2CRentFR,
    B2CRideFR,
    ShopEN,
    ShopFR,
    RentEN,
    ABO_NPC_DE,
    B2CProd_FR_CA_NPS,
    B2CProd_EN_CA_NPS,
    B2CProd_IT_NPS,
    B2CProd_DE_DE_NPS,
    B2CProd_EN_DE_NPS,
    B2CProd_USA_NPS,
    B2C_PROD_en_GB_NPS,
    B2C_B2C_PROD_PL_NPS,
    B2C_B2C_PROD_PT_NPS,
    B2C_PROD_ID_ID_NPS,
    B2C_PROD_EN_ID_NPS,
    B2C_PROD_TR_NPS,
    Shop_NPS_IT,
    Shop_NPS_ES,
    Ride_NPS_IT,
    Ride_NPS_ES,
    Rent_NPS_EN,
    B2C_PROD_FR_MA,
    B2C_PROD_FR_TN,
    B2C_PROD_ES_NI,
    B2C_PROD_ES_MX,
    B2C_PROD_PT_BR_NPS,
    B2C_PROD_PT_UK_UA,
    B2C_PROD_ES_SV,
    B2C_PROD_ROMANIAN,
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
