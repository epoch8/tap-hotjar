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
    site_id = "2975966"
    survey_id = "810747"
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

    @property
    def path(self): 
        return f"/v3/sites/{self.site_id}/polls/{self.survey_id}/responses/export?survey_query=%7B%22sort_by%22:%22-index%22,%22clauses%22:[]%7D&format=csv&async_export=false"


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
        unicode_mappings = {column:_(column) for column in df.columns}
        df = df.rename(columns=unicode_mappings)
        data_str = df.to_json(None, orient='records')
        data = json.loads(data_str)
        yield from data

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        for key in row:
            if isinstance(row[key], str):
                row[key] = _(row[key])
        return row


class B2BTrStream(SurveysStream):
    name = "survey_b2b_tr"
    site_id = "3046251"
    survey_id = "868818"
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
        th.Property(_("B2B Portalını ne kadar tavsiye edersiniz?"), th.StringType),
        th.Property(_("Bu puanınınız nedenini kısaca yazar mısınız?"), th.StringType),
        th.Property(_("Sizi şaşırmak için B2B'de ne yapmalıyız?"), th.StringType),
    ).to_dict()

class B2BUsStream(SurveysStream):
    name = "survey_b2b_us"
    site_id = "3046251"
    survey_id = "868826"
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
        th.Property(_("How likely are you to recommend this portal to someone like you ?"), th.StringType),
        th.Property(_("What is the reason for your score?"), th.StringType),
        th.Property(_("What should we do to WOW you?"), th.StringType),
    ).to_dict()

class B2BCentralAmericaStream(SurveysStream):
    name = "survey_b2b_central_america"
    site_id = "3046251"
    survey_id = "879136"
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
        th.Property(_("¿Qué tan probable es que recomiende este portal a otras personas?"), th.StringType),
        th.Property(_("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(_("¿Qué debemos hacer para mejorar su experiencia en la plataforma?"), th.StringType),
    ).to_dict()


class B2BMexStream(SurveysStream):
    name = "survey_b2b_mex"
    site_id = "3046251"
    survey_id = "838209"
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
        th.Property(_("¿Qué tan probable es que recomiende este portal a otras personas?"), th.StringType),
        th.Property(_("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(_("¿Qué debemos hacer para mejorar su experiencia en la plataforma?"), th.StringType),
    ).to_dict()

class B2BIbericaStream(SurveysStream):
    name = "survey_b2b_iberica"
    site_id = "3046251"
    survey_id = "879133"
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
        th.Property(_("¿Qué probabilidad hay que recomiende este portal a alguien como usted?"), th.StringType),
        th.Property(_("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(_("¿Qué debemos hacer para que le sorprenda?"), th.StringType),
    ).to_dict()

class B2BFranceExportStream(SurveysStream):
    name = "survey_b2b_france_export"
    site_id = "3046251"
    survey_id = "879131"
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
        th.Property(_("Quelle est la probabilité que vous recommandiez ce portail ?"), th.StringType),
        th.Property(_("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(_("Que pouvons-nous faire pour l'améliorer "), th.StringType),
    ).to_dict()

class B2BFranceStream(SurveysStream):
    name = "survey_b2b_france"
    site_id = "3046251"
    survey_id = "879128"
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
        th.Property(_("Quelle est la probabilité que vous recommandiez ce portail ?"), th.StringType),
        th.Property(_("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(_("Que pouvons-nous faire pour l'améliorer "), th.StringType),
    ).to_dict()

class B2BGermanExportStream(SurveysStream):
    name = "survey_b2b_german_export"
    site_id = "3046251"
    survey_id = "879125"
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
        th.Property(_("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.StringType),
        th.Property(_("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(_("Was sollten wir tun, um Sie zu begeistern?"), th.StringType),
    ).to_dict()

class B2BBrasilStream(SurveysStream):
    name = "survey_b2b_brasil"
    site_id = "3046251"
    survey_id = "879115"
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
        th.Property(_("Qual é a probabilidade de você recomendar este portal a alguém como você?"), th.StringType),
        th.Property(_("Qual é a razão de sua pontuação?"), th.StringType),
        th.Property(_("O que devemos fazer para COMO você?"), th.StringType),
    ).to_dict()

class B2BRussiaStream(SurveysStream):
    name = "survey_b2b_russia"
    site_id = "3046251"
    survey_id = "879110"
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
        th.Property(_("Какова вероятность, что вы порекомендуете этот портал кому-то?"), th.StringType),
        th.Property(_("Чем вы руководствовались при выборе вашей оценки?"), th.StringType),
        th.Property(_("Что мы должны сделать, чтобы повысить вашу оценку?"), th.StringType),
    ).to_dict()


class B2BItalyStream(SurveysStream):
    name = "survey_b2b_italy"
    site_id = "3046251"
    survey_id = "879106"
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
        th.Property(_("Quanto raccomandereste questo portale a qualcuno vome voi?"), th.StringType),
        th.Property(_("Qual è il motivo del vostro punteggio?"), th.StringType),
        th.Property(_("Che cosa dovremmo fare per migliorare?"), th.StringType),
    ).to_dict()


class B2BGermanStream(SurveysStream):
    name = "survey_b2b_german"
    site_id = "3046251"
    survey_id = "879094"
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
        th.Property(_("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.StringType),
        th.Property(_("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(_("Was sollten wir tun, um Sie zu begeistern?"), th.StringType),
    ).to_dict()


