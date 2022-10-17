"""Stream type classes for tap-hotjar."""
import requests
import io
import zipfile
import pandas as pd
import json
from unidecode import unidecode as _
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hotjar.client import HotJarStream

class HotJarApiError(Exception):
    ...

class SurveysStream(HotJarStream):
    """Define custom stream."""
    name = "survey_personae_website"
    path = "/v3/sites/2975966/polls/810747/responses/export?survey_query=%7B%22sort_by%22:%22-index%22,%22clauses%22:[]%7D&format=csv&async_export=false"
    schema = th.PropertiesList(
        th.Property("Number", th.IntegerType),
        th.Property("User", th.StringType),
        th.Property("Date Submitted", th.StringType),
        th.Property("Country", th.StringType),
        th.Property("Source URL", th.StringType),
        th.Property("Device", th.StringType),
        th.Property("Browser", th.StringType),
        th.Property("OS", th.StringType),
        th.Property("Hotjar User ID", th.StringType),
        th.Property(_("Bonjour, êtes-vous :"), th.StringType),
        th.Property(_("Votre visite concerne :"), th.StringType),
        th.Property(_("Que cherchez vous sur le site : "), th.StringType),
        th.Property(_("Êtes-vous satisfaits de votre visite : "), th.StringType),
    ).to_dict()


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        zip_download_url = response.json().get("download_url")
        if not zip_download_url:
            raise HotJarApiError()
        surveys_zip_bin = requests.get(zip_download_url).content
        with zipfile.ZipFile(io.BytesIO(surveys_zip_bin)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    csv = io.StringIO(thefile.read().decode("utf-8"))
        df = pd.read_csv(csv)
        french_unicode_mappings = {column:_(column) for column in df.columns}
        df = df.rename(columns=french_unicode_mappings)
        data_str = df.to_json(None, orient='records')
        data = json.loads(data_str)
        yield from data

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        for key in row:
            if isinstance(row[key], str):
                row[key] = _(row[key])
        return row