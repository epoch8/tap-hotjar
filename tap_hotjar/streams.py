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
