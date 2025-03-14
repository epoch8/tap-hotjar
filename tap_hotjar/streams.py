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
    return unidecode(text.replace(f'\n', '')).strip()


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
        th.Property(clean("Êtes-vous satisfaits de votre visite :"), th.NumberType),
    ).to_dict()

    @property
    def path(self): 
        return f"/ask/v3/sites/{self.site_id}/polls/{self.survey_id}/responses/export?survey_query=%7B%22sort_by%22:%22-index%22,%22clauses%22:[]%7D&format=csv&async_export=false"

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
        df = pd.read_csv(csv, dtype=object)
        unicode_mappings = {column: clean(column) for column in df.columns}
        df = df.rename(columns=unicode_mappings)
        data_str = df.to_json(None, orient='records')
        data = json.loads(data_str)
        yield from data

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("B2B Portalını ne kadar tavsiye edersiniz?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("How likely are you to recommend this portal to someone like you ?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("¿Qué tan probable es que recomiende este portal a otras personas?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("¿Qué probabilidad hay de que recomiende este portal a alguien como usted?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("¿Qué probabilidad hay que recomiende Motul a alguien como usted?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Quelle est la probabilité que vous recommandiez ce portail ?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Quelle est la probabilité que vous recommandiez ce portail ?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Qual é a probabilidade de você recomendar este portal a alguém como você?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Какова вероятность, что вы порекомендуете этот портал кому-то?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Quanto raccomandereste questo portale a qualcuno vome voi?"), th.NumberType),
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
        th.Property("User ID", th.StringType),
        th.Property("ICMCustomerID", th.StringType),
        th.Property("ICMUserID", th.StringType),
        th.Property(clean("Wie wahrscheinlich ist es, dass Sie dieses Bestellportal jemandem weiterempfehlen werden?"), th.NumberType),
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
        th.Property(clean("Appréciez-vous notre nouveau site internet et ses services ?"), th.NumberType),
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2CProdES(SurveysStream):
    name = "survey_b2c_prod_es"
    site_id = "3356229"
    survey_id = "904009"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
    ).to_dict()


class ShopEN(SurveysStream):
    name = "survey_b2c_shop_en"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
    ).to_dict()


class ShopFR(SurveysStream):
    name = "survey_b2c_shop_fr"
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
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
    ).to_dict()


class RentEN(SurveysStream):
    name = "survey_b2c_rent_en"
    site_id = "3387427"
    survey_id = "896529"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
    ).to_dict()


class ABO_NPC_DE(SurveysStream):
    name = "survey_abo_nps_de"
    site_id = "3581196"
    survey_id = "938394"
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
        th.Property(clean("Wie wahrscheinlich ist es, dass Sie uns an einen Freund oder Kollegen weiterempfehlen?"), th.NumberType),
        th.Property(clean("Was ist der Grund für Ihre Bewertung?"), th.StringType),
    ).to_dict()


class B2CProd_FR_CA_NPS(SurveysStream):
    name = "survey_b2c_prod_fr_ca_nps"
    site_id = "3356229"
    survey_id = "937605"
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
        th.Property(clean("Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()


class B2CProd_EN_CA_NPS(SurveysStream):
    name = "survey_b2c_prod_en_ca_nps"
    site_id = "3356229"
    survey_id = "937603"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2CProd_IT_NPS(SurveysStream):
    name = "survey_b2c_prod_it_nps"
    site_id = "3356229"
    survey_id = "916470"
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
        th.Property(clean("Quanto è probabile che tu ci raccomandi a un amico o a un collega?"), th.NumberType),
        th.Property(clean("Qual è il motivo della tua risposta?"), th.StringType),
        th.Property(clean("Aiutaci a migliorare la tua esperienza! Sei un operatore del settore o un consumatore finale?"), th.StringType),
    ).to_dict()


class B2CProd_DE_DE_NPS(SurveysStream):
    name = "survey_b2c_prod_de_de_nps"
    site_id = "3356229"
    survey_id = "916468"
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
        th.Property(clean("Wie gefällt Ihnen unsere neue Webseite?"), th.NumberType),
        th.Property(clean("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(clean("Helfen Sie uns, unsere Inhalte zu verbessern! Sind Sie ein Händler oder ein Endverbraucher?"), th.StringType),
    ).to_dict()


class B2CProd_EN_DE_NPS(SurveysStream):
    name = "survey_b2c_prod_en_de_nps"
    site_id = "3356229"
    survey_id = "916466"
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
        th.Property(clean("How do you rate our new web appearance?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2CProd_USA_NPS(SurveysStream):
    name = "survey_b2c_prod_usa_nps"
    site_id = "3356229"
    survey_id = "916464"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_en_GB_NPS(SurveysStream):
    name = "survey_b2c_prod_en_gb_nps"
    site_id = "3356229"
    survey_id = "960940"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_B2C_PROD_PL_NPS(SurveysStream):
    name = "survey_b2c_prod_pl_nps"
    site_id = "3356229"
    survey_id = "954014"
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
        th.Property(clean("Jak prawdopodobne jest, że polecisz nas znajomemu lub współpracownikowi?"), th.NumberType),
        th.Property(clean("Jaki jest powód Twojej oceny?"), th.StringType),
        th.Property(clean("Pomóż nam ulepszyć Twoje doświadczenia! Jesteś profesjonalistą czy osobą prywatną?"), th.StringType),
    ).to_dict()


class B2C_B2C_PROD_PT_NPS(SurveysStream):
    name = "survey_b2c_prod_pt_nps"
    site_id = "3356229"
    survey_id = "938790"
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
        th.Property(clean("Qual a probabilidade de você nos recomendar a um amigo ou colega?"), th.NumberType),
        th.Property(clean("Qual é o motivo da sua pontuação?"), th.StringType),
        th.Property(clean("Ajude-nos a tornar sua experiência melhor! Você é um profissional ou consumidor?"), th.StringType),
    ).to_dict()


class B2C_PROD_ID_ID_NPS(SurveysStream):
    name = "survey_b2c_prod_id_id_nps"
    site_id = "3356229"
    survey_id = "933192"
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
        th.Property(clean("Seberapa besar kemungkinan Anda merekomendasikan kami kepada teman atau rekan kerja Anda?"), th.NumberType),
        th.Property(clean("Apa alasan di balik penilaian Anda?"), th.StringType),
        th.Property(clean("Bantu kami untuk meningkatkan pengalaman Anda! Apakah Anda seorang profesional atau konsumen?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_ID_NPS(SurveysStream):
    name = "survey_b2c_prod_en_id_nps"
    site_id = "3356229"
    survey_id = "933191"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_TR_NPS(SurveysStream):
    name = "survey_b2c_prod_tr_nps"
    site_id = "3356229"
    survey_id = "960938"
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
        th.Property(clean("Bizi bir arkadaşınıza veya meslektaşınıza tavsiye eder misiniz?"), th.NumberType),
        th.Property(clean("Cevabınızın nedeni nedir?"), th.StringType),
        th.Property(clean(f"Deneyiminizi daha iyi hale getirmemize yardımcı olun! \nSatıcı mısınız yoksa son kullanıcı mısınız?"), th.StringType),
    ).to_dict()

    # def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
    #     for key in row:
    #         if isinstance(row[key], str):
    #             row[key] = clean(row[key])
    #     return row


class Shop_NPS_IT(SurveysStream):
    name = "survey_shop_nps_it"
    site_id = "3387435"
    survey_id = "923534"
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
        th.Property(clean("Quanto è probabile che tu ci raccomandi a un amico o a un collega?"), th.NumberType),
        th.Property(clean("Qual è il motivo della tua risposta ?"), th.StringType),
    ).to_dict()


class Shop_NPS_ES(SurveysStream):
    name = "survey_shop_nps_es"
    site_id = "3387435"
    survey_id = "923507"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
    ).to_dict()


class Ride_NPS_IT(SurveysStream):
    name = "survey_ride_nps_it"
    site_id = "3387423"
    survey_id = "965898"
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
        th.Property(clean("Quanto è probabile che tu ci raccomandi a un amico o a un collega?"), th.NumberType),
        th.Property(clean("Qual è il motivo della tua risposta ?"), th.StringType),
    ).to_dict()


class Ride_NPS_ES(SurveysStream):
    name = "survey_ride_nps_es"
    site_id = "3387423"
    survey_id = "906684"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
    ).to_dict()


class Rent_NPS_EN(SurveysStream):
    name = "survey_rent_nps_en"
    site_id = "3387427"
    survey_id = "896529"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
    ).to_dict()


class B2C_PROD_FR_MA(SurveysStream):
    name = "survey_b2c_prod_fr_ma"
    site_id = "3356229"
    survey_id = "987223"
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
        th.Property(clean("Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()


class B2C_PROD_FR_TN(SurveysStream):
    name = "survey_b2c_prod_fr_tn"
    site_id = "3356229"
    survey_id = "987597"
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
        th.Property(clean("Quelle est la probabilité que vous nous recommandiez à un ami ou à un collègue ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_NI(SurveysStream):
    name = "survey_b2c_prod_es_ni"
    site_id = "3356229"
    survey_id = "988590"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_MX(SurveysStream):
    name = "survey_b2c_prod_es_mx"
    site_id = "3356229"
    survey_id = "992136"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_PT_BR_NPS(SurveysStream):
    name = "survey_b2c_prod_pt_br_nps"
    site_id = "3356229"
    survey_id = "987494"
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
        th.Property(clean("Qual a probabilidade de você nos recomendar a um amigo ou colega?"), th.NumberType),
        th.Property(clean("Qual é o motivo da sua pontuação?"), th.StringType),
        th.Property(clean("Ajude-nos a tornar sua experiência melhor! Você é um profissional ou consumidor?"), th.StringType),
    ).to_dict()


class B2C_PROD_PT_UK_UA(SurveysStream):
    name = "survey_b2c_prod_uk_ua"
    site_id = "3356229"
    survey_id = "987491"
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
        th.Property(clean("Наскільки ймовірно, що порадите нас друзям чи колегам?"), th.NumberType),
        th.Property(clean("На чому грунтується Ваша оцінка?"), th.StringType),
        th.Property(clean("Допоможіть нам стати кращими для Вас! Ви спеціаліст чи приватна особа?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_SV(SurveysStream):
    name = "survey_b2c_prod_es_sv"
    site_id = "3356229"
    survey_id = "1016406"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ROMANIAN(SurveysStream):
    name = "survey_b2c_prod_romanian"
    site_id = "3356229"
    survey_id = "992131"
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
        th.Property(clean("Cât de probabil este să ne recomanzi unui prieten sau coleg?"), th.NumberType),
        th.Property(clean("Care este motivul evaluării tale?"), th.StringType),
        th.Property(clean("Ajută-ne să ne îmbunătățim experiența! Ești profesionist sau consumator?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_FI(SurveysStream):
    name = "survey_b2c_prod_en_fi"
    site_id = "3356229"
    survey_id = "1016414"
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
        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_PE(SurveysStream):
    name = "survey_b2c_prod_es_pe"
    site_id = "3356229"
    survey_id = "1016410"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_CR(SurveysStream):
    name = "survey_b2c_prod_es_cr"
    site_id = "3356229"
    survey_id = "1016409"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_HN(SurveysStream):
    name = "survey_b2c_prod_es_hn"
    site_id = "3356229"
    survey_id = "1016408"
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
        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class SHOP_NPS_DE(SurveysStream):
    name = "survey_shop_nps_de"
    site_id = "3901562"
    survey_id = "1014897"
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
        th.Property(clean("Warum möchtest du schon gehen?"), th.StringType),
        th.Property(clean("Was hat dich gestört?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_DK(SurveysStream):
    name = "survey_b2c_prod_en_dk"
    site_id = "3356229"
    survey_id = "1021393"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_LV(SurveysStream):
    name = "survey_b2c_prod_en_lv"
    site_id = "3356229"
    survey_id = "1021387"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_SE(SurveysStream):
    name = "survey_b2c_prod_en_se"
    site_id = "3356229"
    survey_id = "1021386"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_VI_VN(SurveysStream):
    name = "survey_b2c_prod_vi_vn"
    site_id = "3356229"
    survey_id = "992207"
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

        th.Property(clean("Khả năng bạn giới thiệu chúng tôi với bạn bè hoặc đồng nghiệp là bao nhiêu?"), th.NumberType),
        th.Property(clean("Lý do cho điểm số của bạn là gì?"), th.StringType),
        th.Property(clean("Hãy giúp chúng tôi làm cho trải nghiệm của bạn tốt hơn! Bạn là người chuyên nghiệp hay người tiêu dùng?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_CO(SurveysStream):
    name = "survey_b2c_prod_es_co"
    site_id = "3356229"
    survey_id = "987505"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_NZ_NPS(SurveysStream):
    name = "survey_b2c_prod_en_nz_nps"
    site_id = "3356229"
    survey_id = "1064337"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_SG_NPS(SurveysStream):
    name = "survey_b2c_prod_en_sg_nps"
    site_id = "3356229"
    survey_id = "1064336"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_PH_NPS(SurveysStream):
    name = "survey_b2c_prod_en_ph_nps"
    site_id = "3356229"
    survey_id = "1064333"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_MY_NPS(SurveysStream):
    name = "survey_b2c_prod_en_my_nps"
    site_id = "3356229"
    survey_id = "1064331"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_ZA_NPS(SurveysStream):
    name = "survey_b2c_prod_en_za_nps"
    site_id = "3356229"
    survey_id = "1057594"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_GT(SurveysStream):
    name = "survey_b2c_prod_es_gt"
    site_id = "3356229"
    survey_id = "1054742"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_DO(SurveysStream):
    name = "survey_b2c_prod_es_do"
    site_id = "3356229"
    survey_id = "1054741"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_VE(SurveysStream):
    name = "survey_b2c_prod_es_ve"
    site_id = "3356229"
    survey_id = "1054739"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_ES_AR(SurveysStream):
    name = "survey_b2c_prod_es_ar"
    site_id = "3356229"
    survey_id = "1043104"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()


class B2C_PROD_IT_CH_NPS(SurveysStream):
    name = "survey_b2c_prod_it_ch_nps"
    site_id = "3356229"
    survey_id = "1077355"
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

        th.Property(clean("Quanto è probabile che tu ci raccomandi a un amico o a un collega?"), th.NumberType),
        th.Property(clean("Qual è il motivo della tua risposta?"), th.StringType),
        th.Property(clean("Aiutaci a migliorare la tua esperienza! Sei un operatore del settore o un consumatore finale?"), th.StringType),
    ).to_dict()


class B2C_PROD_FR_CH_NPS(SurveysStream):
    name = "survey_b2c_prod_fr_ch_nps"
    site_id = "3356229"
    survey_id = "1077350"
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

        th.Property(clean("Appréciez-vous notre nouveau site internet et ses services ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()


class B2C_PROD_DE_CH_NPS(SurveysStream):
    name = "survey_b2c_prod_de_ch_nps"
    site_id = "3356229"
    survey_id = "1077234"
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

        th.Property(clean("Wie gefällt Ihnen unsere neue Webseite?"), th.NumberType),
        th.Property(clean("Was ist der Grund für Ihre Bewertung?"), th.StringType),
        th.Property(clean("Helfen Sie uns, unsere Inhalte zu verbessern! Sind Sie ein Händler oder ein Endverbraucher?"), th.StringType),
    ).to_dict()


class B2C_PROD_AUSTRALIAN_EN_AU(SurveysStream):
    name = "survey_b2c_prod_australian_en_au"
    site_id = "3356229"
    survey_id = "992211"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_LT(SurveysStream):
    name = "survey_b2c_prod_en_lt"
    site_id = "3356229"
    survey_id = "1021388"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()


class B2C_PROD_EN_NO(SurveysStream):
    name = "survey_b2c_prod_en_no"
    site_id = "3356229"
    survey_id = "1021392"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# нужно прописать названия классов и переменной name по аналогии с этими примерами
# # исходное название опроса Motul B2C PROD de-DE NPS
# class B2CProd_DE_DE_NPS(SurveysStream): 
#     name = "survey_b2c_prod_de_de_nps"
# # исходное название опроса Motul B2C PROD en-NO
# class B2C_PROD_EN_NO(SurveysStream): 
#     name = "survey_b2c_prod_en_no"
# # исходное название опроса Motul B2C PROD en-LT
# class B2C_PROD_EN_LT(SurveysStream): 
#     name = "survey_b2c_prod_en_lt"

# теперь я даю тебе список исходных названий опросов. для каждого напиши в таком же формате 
# исходное название опроса Motul B2C PROD fr-YT Mayotte NPS
# class B2C_PROD_FR_YT_MAYOTTE_NPS(SurveysStream):
#     name = "survey_b2c_prod_fr_yt_mayotte_nps"

# # исходное название опроса Motul B2C PROD fr-MV Maldives NPS
# class B2C_PROD_FR_MV_MALDIVES_NPS(SurveysStream):
#     name = "survey_b2c_prod_fr_mv_maldives_nps"

# # исходное название опроса Motul B2C PROD fr-MG Madagascar NPS
# class B2C_PROD_FR_MG_MADAGASCAR_NPS(SurveysStream):
#     name = "survey_b2c_prod_fr_mg_madagascar_nps"

# # исходное название опроса Motul B2C PROD pt-MZ Mozambique NPS
# class B2C_PROD_PT_MZ_MOZAMBIQUE_NPS(SurveysStream):
#     name = "survey_b2c_prod_pt_mz_mozambique_nps"

# # исходное название опроса Motul B2C PROD pt-AO Angola NPS
# class B2C_PROD_PT_AO_ANGOLA_NPS(SurveysStream):
#     name = "survey_b2c_prod_pt_ao_angola_nps"

# # исходное название опроса Motul B2C PROD en-ZW Zimbabwe NPS
# class B2C_PROD_EN_ZW_ZIMBABWE_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_zw_zimbabwe_nps"

# # исходное название опроса Motul B2C PROD en-ZM Zambia NPS
# class B2C_PROD_EN_ZM_ZAMBIA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_zm_zambia_nps"

# # исходное название опроса Motul B2C PROD en-TZ Tanzania NPS
# class B2C_PROD_EN_TZ_TANZANIA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_tz_tanzania_nps"

# # исходное название опроса Motul B2C PROD en-SZ Swaziland NPS
# class B2C_PROD_EN_SZ_SWAZILAND_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_sz_swaziland_nps"

# # исходное название опроса Motul B2C PROD en-NA Namibia NPS
# class B2C_PROD_EN_NA_NAMIBIA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_na_namibia_nps"

# # исходное название опроса Motul B2C PROD en-YT Mayotte NPS
# class B2C_PROD_EN_YT_MAYOTTE_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_yt_mayotte_nps"

# # исходное название опроса Motul B2C PROD en-MV Maldives NPS
# class B2C_PROD_EN_MV_MALDIVES_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_mv_maldives_nps"

# # исходное название опроса Motul B2C PROD en-MG Madagascar NPS
# class B2C_PROD_EN_MG_MADAGASCAR_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_mg_madagascar_nps"

# # исходное название опроса Motul B2C PROD en-KE Kenya NPS
# class B2C_PROD_EN_KE_KENYA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_ke_kenya_nps"

# # исходное название опроса Motul B2C PROD en-BW Botswana NPS
# class B2C_PROD_EN_BW_BOTSWANA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_bw_botswana_nps"

# # исходное название опроса Motul B2C PROD en-AO Angola NPS
# class B2C_PROD_EN_AO_ANGOLA_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_ao_angola_nps"

# # исходное название опроса Motul B2C PROD en-MZ Mozambique NPS
# class B2C_PROD_EN_MZ_MOZAMBIQUE_NPS(SurveysStream):
#     name = "survey_b2c_prod_en_mz_mozambique_nps"

# # исходное название опроса Motul B2C PROD en-NG Nigeria
# class B2C_PROD_EN_NG_NIGERIA(SurveysStream):
#     name = "survey_b2c_prod_en_ng_nigeria"

# # исходное название опроса Motul B2C PROD Netherlands nl-NL
# class B2C_PROD_NETHERLANDS_NL_NL(SurveysStream):
#     name = "survey_b2c_prod_netherlands_nl_nl"

# # исходное название опроса Motul B2C PROD Luxembourg en-LU
# class B2C_PROD_LUXEMBOURG_EN_LU(SurveysStream):
#     name = "survey_b2c_prod_luxembourg_en_lu"

# # исходное название опроса Motul B2C PROD Belgium en-BE
# class B2C_PROD_BELGIUM_EN_BE(SurveysStream):
#     name = "survey_b2c_prod_belgium_en_be"

# # исходное название опроса Motul B2C PROD Netherlands en-NL
# class B2C_PROD_NETHERLANDS_EN_NL(SurveysStream):
#     name = "survey_b2c_prod_netherlands_en_nl"

# # исходное название опроса Motul B2C PROD es-UY
# class B2C_PROD_ES_UY(SurveysStream):
#     name = "survey_b2c_prod_es_uy"

# # исходное название опроса Motul B2C PROD es-PY
# class B2C_PROD_ES_PY(SurveysStream):
#     name = "survey_b2c_prod_es_py"

# # исходное название опроса Motul B2C PROD es-PA
# class B2C_PROD_ES_PA(SurveysStream):
#     name = "survey_b2c_prod_es_pa"

# # исходное название опроса Motul B2C PROD es-EC
# class B2C_PROD_ES_EC(SurveysStream):
#     name = "survey_b2c_prod_es_ec"

# # исходное название опроса Motul B2C PROD es-CL
# class B2C_PROD_ES_CL(SurveysStream):
#     name = "survey_b2c_prod_es_cl"

# # исходное название опроса Motul B2C PROD es-BO
# class B2C_PROD_ES_BO(SurveysStream):
#     name = "survey_b2c_prod_es_bo"

# # исходное название опроса Motul B2C PROD Montenegro en-ME
# class B2C_PROD_MONTENEGRO_EN_ME(SurveysStream):
#     name = "survey_b2c_prod_montenegro_en_me"

# # исходное название опроса Motul B2C PROD Slovenia en-SI
# class B2C_PROD_SLOVENIA_EN_SI(SurveysStream):
#     name = "survey_b2c_prod_slovenia_en_si"

# # исходное название опроса Motul B2C PROD Croatia en-HR
# class B2C_PROD_CROATIA_EN_HR(SurveysStream):
#     name = "survey_b2c_prod_croatia_en_hr"

# # исходное название опроса Motul B2C PROD Bosnia and Herzegovina en-BA
# class B2C_PROD_BOSNIA_AND_HERZEGOVINA_EN_BA(SurveysStream):
#     name = "survey_b2c_prod_bosnia_and_herzegovina_en_ba"

# # исходное название опроса Motul B2C PROD North Macedonia en-MK
# class B2C_PROD_NORTH_MACEDONIA_EN_MK(SurveysStream):
#     name = "survey_b2c_prod_north_macedonia_en_mk"

# # исходное название опроса Motul B2C PROD Albania en-AL
# class B2C_PROD_ALBANIA_EN_AL(SurveysStream):
#     name = "survey_b2c_prod_albania_en_al"

# # исходное название опроса Motul B2C PROD Moldova en-MD
# class B2C_PROD_MOLDOVA_EN_MD(SurveysStream):
#     name = "survey_b2c_prod_moldova_en_md"

# # исходное название опроса Motul B2C PROD Bulgaria en-BG
# class B2C_PROD_BULGARIA_EN_BG(SurveysStream):
#     name = "survey_b2c_prod_bulgaria_en_bg"

# # исходное название опроса Motul B2C PROD Serbia en-RS
# class B2C_PROD_SERBIA_EN_RS(SurveysStream):
#     name = "survey_b2c_prod_serbia_en_rs"

# # исходное название опроса Motul B2C PROD Saudi Arabia en-SA
# class B2C_PROD_SAUDI_ARABIA_EN_SA(SurveysStream):
#     name = "survey_b2c_prod_saudi_arabia_en_sa"

# # исходное название опроса Motul B2C PROD Qatar en-QA
# class B2C_PROD_QATAR_EN_QA(SurveysStream):
#     name = "survey_b2c_prod_qatar_en_qa"

# # исходное название опроса Motul B2C PROD Pakistan en-PK
# class B2C_PROD_PAKISTAN_EN_PK(SurveysStream):
#     name = "survey_b2c_prod_pakistan_en_pk"

# # исходное название опроса Motul B2C PROD Oman en-OM
# class B2C_PROD_OMAN_EN_OM(SurveysStream):
#     name = "survey_b2c_prod_oman_en_om"

# # исходное название опроса Motul B2C PROD Lebanon en-LB
# class B2C_PROD_LEBANON_EN_LB(SurveysStream):
#     name = "survey_b2c_prod_lebanon_en_lb"

# # исходное название опроса Motul B2C PROD Kuwait en-KW
# class B2C_PROD_KUWAIT_EN_KW(SurveysStream):
#     name = "survey_b2c_prod_kuwait_en_kw"

# # исходное название опроса Motul B2C PROD Jordan en-JO
# class B2C_PROD_JORDAN_EN_JO(SurveysStream):
#     name = "survey_b2c_prod_jordan_en_jo"

# # исходное название опроса Motul B2C PROD Iraq en-IQ
# class B2C_PROD_IRAQ_EN_IQ(SurveysStream):
#     name = "survey_b2c_prod_iraq_en_iq"

# # исходное название опроса Motul B2C PROD Bahrain en-BH
# class B2C_PROD_BAHRAIN_EN_BH(SurveysStream):
#     name = "survey_b2c_prod_bahrain_en_bh"

# # исходное название опроса Motul B2C PROD U.A.E. en-AE
# class B2C_PROD_UAE_EN_AE(SurveysStream):
#     name = "survey_b2c_prod_uae_en_ae"


# Motul B2C PROD fr-YT Mayotte NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1578435
class B2CProd_FR_YT(SurveysStream):
    name = "survey_b2c_prod_fr_yt"
    site_id = "3356229"
    survey_id = "1578435"
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

        th.Property(clean("Appréciez-vous notre nouveau site internet et ses services ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()

# Motul B2C PROD fr-MV Maldives NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1578434
class B2CProd_FR_MV(SurveysStream):
    name = "survey_b2c_prod_fr_mv"
    site_id = "3356229"
    survey_id = "1578434"
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

        th.Property(clean("Appréciez-vous notre nouveau site internet et ses services ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()

# Motul B2C PROD fr-MG Madagascar NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1578431
class B2CProd_FR_MG(SurveysStream):
    name = "survey_b2c_prod_fr_mg"
    site_id = "3356229"
    survey_id = "1578431"
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

        th.Property(clean("Appréciez-vous notre nouveau site internet et ses services ?"), th.NumberType),
        th.Property(clean("Quelle est la raison de votre score ?"), th.StringType),
        th.Property(clean("Aidez-nous à améliorer votre expérience ! Etes-vous un professionnel ou un particulier ?"), th.StringType),
    ).to_dict()

# Motul B2C PROD pt-MZ Mozambique NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1578428
class B2CProd_PT_MZ(SurveysStream):
    name = "survey_b2c_prod_pt_mz"
    site_id = "3356229"
    survey_id = "1578428"
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

        th.Property(clean("Qual a probabilidade de você nos recomendar a um amigo ou colega?"), th.NumberType),
        th.Property(clean("Qual é o motivo da sua pontuação?"), th.StringType),
        th.Property(clean("Ajude-nos a tornar sua experiência melhor! Você é um profissional ou consumidor?"), th.StringType),
    ).to_dict()

# Motul B2C PROD pt-AO Angola NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1578427
class B2CProd_PT_AO(SurveysStream):
    name = "survey_b2c_prod_pt_ao"
    site_id = "3356229"
    survey_id = "1578427"
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

        th.Property(clean("Qual a probabilidade de você nos recomendar a um amigo ou colega?"), th.NumberType),
        th.Property(clean("Qual é o motivo da sua pontuação?"), th.StringType),
        th.Property(clean("Ajude-nos a tornar sua experiência melhor! Você é um profissional ou consumidor?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-ZW Zimbabwe NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576374
class B2CProd_EN_ZW(SurveysStream):
    name = "survey_b2c_prod_en_zw"
    site_id = "3356229"
    survey_id = "1576374"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-ZM Zambia NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576370
class B2CProd_EN_ZM(SurveysStream):
    name = "survey_b2c_prod_en_zm"
    site_id = "3356229"
    survey_id = "1576370"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-TZ Tanzania NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576369
class B2CProd_EN_TZ(SurveysStream):
    name = "survey_b2c_prod_en_tz"
    site_id = "3356229"
    survey_id = "1576369"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-SZ Swaziland NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576364
class B2CProd_EN_SZ(SurveysStream):
    name = "survey_b2c_prod_en_sz"
    site_id = "3356229"
    survey_id = "1576364"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-NA Namibia NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576338
class B2CProd_EN_NA(SurveysStream):
    name = "survey_b2c_prod_en_na"
    site_id = "3356229"
    survey_id = "1576338"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-YT Mayotte NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576335
class B2CProd_EN_YT(SurveysStream):
    name = "survey_b2c_prod_en_yt"
    site_id = "3356229"
    survey_id = "1576335"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-MV Maldives NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576332
class B2CProd_EN_MV(SurveysStream):
    name = "survey_b2c_prod_en_mv"
    site_id = "3356229"
    survey_id = "1576332"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-MG Madagascar NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576330
class B2CProd_EN_MG(SurveysStream):
    name = "survey_b2c_prod_en_mg"
    site_id = "3356229"
    survey_id = "1576330"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-KE Kenya NPS
# https://insights.hotjar.com/sites/3356229/surveys/overview/1576328
class B2CProd_EN_KE(SurveysStream):
    name = "survey_b2c_prod_en_ke"
    site_id = "3356229"
    survey_id = "1576328"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-BW Botswana NPS
class B2CProd_EN_BW(SurveysStream):
    name = "survey_b2c_prod_en_bw"
    site_id = "3356229"
    survey_id = "1576322"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-AO Angola NPS
class B2CProd_EN_AO(SurveysStream):
    name = "survey_b2c_prod_en_ao"
    site_id = "3356229"
    survey_id = "1576315"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-MZ Mozambique NPS
class B2CProd_EN_MZ(SurveysStream):
    name = "survey_b2c_prod_en_mz"
    site_id = "3356229"
    survey_id = "1576073"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD en-NG Nigeria
class B2C_PROD_EN_NG(SurveysStream):
    name = "survey_b2c_prod_en_ng"
    site_id = "3356229"
    survey_id = "1575283"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Netherlands nl-NL
class B2C_PROD_NL_NL(SurveysStream):
    name = "survey_b2c_prod_nl_nl"
    site_id = "3356229"
    survey_id = "1566591"
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

        th.Property(clean("Hoe groot is de kans dat je ons zou aanbevelen bij een vriend of collega?"), th.NumberType),
        th.Property(clean("Wat is de reden voor je antwoord?"), th.StringType),
        th.Property(clean("Help ons je ervaring efficienter te maken! Ben je een zakelijke of particuliere klant?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Luxembourg en-LU
class B2C_PROD_EN_LU(SurveysStream):
    name = "survey_b2c_prod_en_lu"
    site_id = "3356229"
    survey_id = "1548837"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Belgium en-BE
class B2C_PROD_EN_BE(SurveysStream):
    name = "survey_b2c_prod_en_be"
    site_id = "3356229"
    survey_id = "1548835"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Netherlands en-NL
class B2C_PROD_EN_NL(SurveysStream):
    name = "survey_b2c_prod_en_nl"
    site_id = "3356229"
    survey_id = "1548755"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-UY
class B2C_PROD_ES_UY(SurveysStream):
    name = "survey_b2c_prod_es_uy"
    site_id = "3356229"
    survey_id = "1541808"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-PY
class B2C_PROD_ES_PY(SurveysStream):
    name = "survey_b2c_prod_es_py"
    site_id = "3356229"
    survey_id = "1541806"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-PA
class B2C_PROD_ES_PA(SurveysStream):
    name = "survey_b2c_prod_es_pa"
    site_id = "3356229"
    survey_id = "1541802"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-EC
class B2C_PROD_ES_EC(SurveysStream):
    name = "survey_b2c_prod_es_ec"
    site_id = "3356229"
    survey_id = "1541800"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-CL
class B2C_PROD_ES_CL(SurveysStream):
    name = "survey_b2c_prod_es_cl"
    site_id = "3356229"
    survey_id = "1541798"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD es-BO
class B2C_PROD_ES_BO(SurveysStream):
    name = "survey_b2c_prod_es_bo"
    site_id = "3356229"
    survey_id = "1541796"
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

        th.Property(clean("¿Qué probabilidad hay que nos recomiendes a un amigo?"), th.NumberType),
        th.Property(clean("¿Cuál es la razón de tu respuesta?"), th.StringType),
        th.Property(clean("¡Ayúdanos a mejorar tu experiencia! ¿Eres profesional o particular?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Montenegro en-ME
class B2C_PROD_EN_ME(SurveysStream):
    name = "survey_b2c_prod_en_me"
    site_id = "3356229"
    survey_id = "1521810"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Slovenia en-SI
class B2C_PROD_EN_SI(SurveysStream):
    name = "survey_b2c_prod_en_si"
    site_id = "3356229"
    survey_id = "1521807"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Croatia en-HR
class B2C_PROD_EN_HR(SurveysStream):
    name = "survey_b2c_prod_en_hr"
    site_id = "3356229"
    survey_id = "1521802"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Bosnia and Herzegovina en-BA
class B2C_PROD_EN_BA(SurveysStream):
    name = "survey_b2c_prod_en_ba"
    site_id = "3356229"
    survey_id = "1521800"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD North Macedonia en-MK
class B2C_PROD_EN_MK(SurveysStream):
    name = "survey_b2c_prod_en_mk"
    site_id = "3356229"
    survey_id = "1521799"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Albania en-AL
class B2C_PROD_EN_AL(SurveysStream):
    name = "survey_b2c_prod_en_al"
    site_id = "3356229"
    survey_id = "1521714"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Moldova en-MD
class B2C_PROD_EN_MD(SurveysStream):
    name = "survey_b2c_prod_en_md"
    site_id = "3356229"
    survey_id = "1521701"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Bulgaria en-BG
class B2C_PROD_EN_BG(SurveysStream):
    name = "survey_b2c_prod_en_bg"
    site_id = "3356229"
    survey_id = "1521678"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Serbia en-RS
class B2C_PROD_EN_RS(SurveysStream):
    name = "survey_b2c_prod_en_rs"
    site_id = "3356229"
    survey_id = "1521567"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Saudi Arabia en-SA
class B2C_PROD_EN_SA(SurveysStream):
    name = "survey_b2c_prod_en_sa"
    site_id = "3356229"
    survey_id = "1367169"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Qatar en-QA
class B2C_PROD_EN_QA(SurveysStream):
    name = "survey_b2c_prod_en_qa"
    site_id = "3356229"
    survey_id = "1367163"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Pakistan en-PK
class B2C_PROD_EN_PK(SurveysStream):
    name = "survey_b2c_prod_en_pk"
    site_id = "3356229"
    survey_id = "1367162"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Oman en-OM
class B2C_PROD_EN_OM(SurveysStream):
    name = "survey_b2c_prod_en_om"
    site_id = "3356229"
    survey_id = "1367159"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Lebanon en-LB
class B2C_PROD_EN_LB(SurveysStream):
    name = "survey_b2c_prod_en_lb"
    site_id = "3356229"
    survey_id = "1367157"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Kuwait en-KW
class B2C_PROD_EN_KW(SurveysStream):
    name = "survey_b2c_prod_en_kw"
    site_id = "3356229"
    survey_id = "1367154"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Jordan en-JO
class B2C_PROD_EN_JO(SurveysStream):
    name = "survey_b2c_prod_en_jo"
    site_id = "3356229"
    survey_id = "1367152"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Iraq en-IQ
class B2C_PROD_EN_IQ(SurveysStream):
    name = "survey_b2c_prod_en_iq"
    site_id = "3356229"
    survey_id = "1367151"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD Bahrain en-BH
class B2C_PROD_EN_BH(SurveysStream):
    name = "survey_b2c_prod_en_bh"
    site_id = "3356229"
    survey_id = "1367150"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()

# Motul B2C PROD U.A.E. en-AE
class B2C_PROD_EN_AE(SurveysStream):
    name = "survey_b2c_prod_en_ae"
    site_id = "3356229"
    survey_id = "1361692"
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

        th.Property(clean("How likely are you to recommend us to a friend or colleague?"), th.NumberType),
        th.Property(clean("What's the reason for your score?"), th.StringType),
        th.Property(clean("Help us make your experience better! Are you professional or consumer?"), th.StringType),
    ).to_dict()