"""Stream type classes for tap-hotjar."""
import requests
import io
import zipfile
import pandas as pd
import json
from unidecode import unidecode
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hotjar.client import HotJarStream

class HotJarApiError(Exception):
    ...

def clean(text: str) -> str:
    return unidecode(text).strip()

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
        th.Property(clean("Bonjour, êtes-vous :"), th.StringType),
        th.Property(clean("Votre visite concerne :"), th.StringType),
        th.Property(clean("Que cherchez vous sur le site :"), th.StringType),
        th.Property(clean("Êtes-vous satisfaits de votre visite :"), th.StringType),
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
        unicode_mappings = {column: clean(column) for column in df.columns}
        df = df.rename(columns=unicode_mappings)
        data_str = df.to_json(None, orient='records')
        data = json.loads(data_str)
        yield from data

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        for key in row:
            if isinstance(row[key], str):
                row[key] = clean(row[key])
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
        th.Property(clean("B2B Portalını ne kadar tavsiye edersiniz?"), th.StringType),
        th.Property(clean("Bu puanınınız nedenini kısaca yazar mısınız?"), th.StringType),
        th.Property(clean("Sizi şaşırmak için B2B'de ne yapmalıyız?"), th.StringType),
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
        th.Property(clean("How likely are you to recommend this portal to someone like you ?"), th.StringType),
        th.Property(clean("What is the reason for your score?"), th.StringType),
        th.Property(clean("What should we do to WOW you?"), th.StringType),
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
        th.Property(clean("¿Qué tan probable es que recomiende este portal a otras personas?"), th.StringType),
        th.Property(clean("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(clean("¿Qué debemos hacer para mejorar su experiencia en la plataforma?"), th.StringType),
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
        th.Property(clean("¿Qué probabilidad hay de que recomiende este portal a alguien como usted?"), th.StringType),
        th.Property(clean("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(clean("¿Qué debemos hacer para que te sorprendas?"), th.StringType),
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
        th.Property(clean("¿Qué probabilidad hay que recomiende este portal a alguien como usted?"), th.StringType),
        th.Property(clean("¿Cuál es la razón de su puntuación?"), th.StringType),
        th.Property(clean("¿Qué debemos hacer para que le sorprenda?"), th.StringType),
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
        th.Property(clean("Quelle est la probabilité que vous recommandiez ce portail ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Que pouvons-nous faire pour l'améliorer"), th.StringType),
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
        th.Property(clean("Quelle est la probabilité que vous recommandiez ce portail ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Que pouvons-nous faire pour l'améliorer"), th.StringType),
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
        th.Property(clean("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.StringType),
        th.Property(clean("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(clean("Was sollten wir tun, um Sie zu begeistern?"), th.StringType),
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
        th.Property(clean("Qual é a probabilidade de você recomendar este portal a alguém como você?"), th.StringType),
        th.Property(clean("Qual é a razão de sua pontuação?"), th.StringType),
        th.Property(clean("O que devemos fazer para COMO você?"), th.StringType),
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
        th.Property(clean("Какова вероятность, что вы порекомендуете этот портал кому-то?"), th.StringType),
        th.Property(clean("Чем вы руководствовались при выборе вашей оценки?"), th.StringType),
        th.Property(clean("Что мы должны сделать, чтобы повысить вашу оценку?"), th.StringType),
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
        th.Property(clean("Quanto raccomandereste questo portale a qualcuno vome voi?"), th.StringType),
        th.Property(clean("Qual è il motivo del vostro punteggio?"), th.StringType),
        th.Property(clean("Che cosa dovremmo fare per migliorare?"), th.StringType),
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
        th.Property(clean("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.StringType),
        th.Property(clean("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(clean("Was sollten wir tun, um Sie zu begeistern?"), th.StringType),
    ).to_dict()


class B2CProdFR(SurveysStream):
    name = "survey_b2c_prod_fr"
    site_id = "3356229"
    survey_id = "880360"
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
        th.Property(clean("Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()


class B2CProdEN(SurveysStream):
    name = "survey_b2c_prod_en"
    site_id = "3356229"
    survey_id = "880355"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.StringType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2CRentFR(SurveysStream):
    name = "survey_b2c_rent_fr"
    site_id = "3387427"
    survey_id = "885645"
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
    ).to_dict()

class B2CRideFR(SurveysStream):
    name = "survey_b2c_ride_fr"
    site_id = "3387423"
    survey_id = "885537"
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
    ).to_dict()

class ShopEN(SurveysStream):
    name = "survey_shop_en"
    site_id = "3387435"
    survey_id = "887070"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.StringType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
    ).to_dict()

class ShopFR(SurveysStream):
    name = "survey_shop_fr"
    site_id = "3387435"
    survey_id = "887066"
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.StringType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
    ).to_dict()

class RentEN(SurveysStream):
    name = "survey_rent_en"
    site_id = "3387435"
    survey_id = "887066"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.StringType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
    ).to_dict()


