from enum import Enum, unique
from typing import Any, NamedTuple

import pandas as pd


class EnrichedEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in cls)


@unique
class PropertyType(EnrichedEnum):
    TEXT = "text"
    RICH_TEXT = "rich_text"
    SELECT = "select"
    TITLE = "title"
    DATE = "date"
    CHECKBOX = "checkbox"
    NUMBER = "number"
    URL = "url"
    UNKNOWN = "unknown"


class PropertyDefinition(NamedTuple):
    name: str
    property_type: PropertyType


class PropertyValue(NamedTuple):
    name: str
    value: Any


class NotionPropertyDecoder:
    """Transforms Notion page property encoded values (as returned by Notion API in JSON format) into domain object values

    Use the method :func:`~NotionPropertyDecoder.decode`
    """

    def __init__(self):
        self.PROPERTY_TYPE_TO_PROPERTY_DECODER_MAP = {
            "select": self._select_decoder,
            "rich_text": self._rich_text_decoder,
            "title": self._rich_text_decoder,
            "date": self._date_decoder
        }

    def _get_decoder_for_type(self, property_type):
        return self.PROPERTY_TYPE_TO_PROPERTY_DECODER_MAP.get(
            property_type,
            self._default_decoder
        )

    @classmethod
    def _default_decoder(cls, property_value):
        return property_value

    @classmethod
    def _select_decoder(cls, property_value):
        return property_value["name"]

    @classmethod
    def _rich_text_decoder(cls, property_value):
        if not property_value:
            return None

        return property_value[0]["plain_text"]

    @classmethod
    def _date_decoder(cls, property_value):
        return pd.to_datetime(property_value["start"])

    @classmethod
    def _get_property_type(cls, property_data):
        return property_data["type"]

    @classmethod
    def _get_encoded_property_value(cls, property_data):
        return property_data[cls._get_property_type(property_data)]

    def decode(self, property_data):
        """This function is the entry point for the class"""
        property_type = self._get_property_type(property_data)
        encoded_property_value = self._get_encoded_property_value(property_data)

        return self._get_decoder_for_type(property_type)(encoded_property_value)


class NotionPropertyEncoder:
    """Transforms list of domain object values into page property encoded values (as required by Notion API in JSON format)

    Use the method :func:`~NotionPropertyEncoder.encode`
    """

    def __init__(self):
        self.property_type_to_property_encoder_map = {
            PropertyType.TEXT: self._text_encode,
            PropertyType.RICH_TEXT: self._rich_text_encode,
            PropertyType.TITLE: self._title_encode,
            PropertyType.SELECT: self._select_encode,
            PropertyType.DATE: self._date_encode,
            PropertyType.CHECKBOX: self._checkbox_encode,
            PropertyType.NUMBER: self._number_encode,
        }

    @staticmethod
    def _text_encode(value: str):
        return {
            PropertyType.TEXT.value: {
                "content": value
            }
        }

    @staticmethod
    def _rich_text_encode(value: str):
        return {
            "rich_text": [
                {
                    "text": {
                        "content": value
                    }
                }
            ]
        }

    @staticmethod
    def _title_encode(value: str):
        return {
            "title": [
                {
                    "text": {
                        "content": value
                    }
                }
            ]
        }

    @staticmethod
    def _select_encode(value: str):
        return {
            "select": {
                "name": value
            }
        }

    @staticmethod
    def _date_encode(value: pd.Timestamp):
        return {
            "date": {"start": value.strftime("%Y-%m-%d"), "end": None, "time_zone": None}
        }

    @staticmethod
    def _checkbox_encode(value: bool):
        return {"checkbox": value}

    @staticmethod
    def _number_encode(value):
        return {"number": value}

    def encode(self, value, property_type: PropertyType):
        """This function is the entry point for the class"""
        encoder = self.property_type_to_property_encoder_map[property_type]
        return encoder(value)
