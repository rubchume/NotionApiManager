from itertools import chain
import json
from typing import List

import pandas as pd
import requests

from notionapimanager.notion_property_encoder import NotionPropertyDecoder, NotionPropertyEncoder, PropertyDefinition, \
    PropertyType, PropertyValue


class NotionDatabaseApiManager:
    """Class for reading from (and writing to) Notion databases"""

    DATABASES_URL = 'https://api.notion.com/v1/databases/'
    CREATE_URL = 'https://api.notion.com/v1/pages'

    def __init__(self, integration_token, database_ids):
        self.integration_token = integration_token
        self.database_ids = database_ids

        self._headers = None
        self._decoder = None
        self._encoder = None
        self._property_types = None

    def connect(self):
        """Perform preparation operations before communicating with Notion API"""

        self._headers = {
            "Authorization": "Bearer " + self.integration_token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }
        self._decoder = NotionPropertyDecoder()
        self._encoder = NotionPropertyEncoder()

        self._property_types = {
            database_id: {
                property_definition.name: property_definition.property_type
                for property_definition in self._get_property_definitions(database_id)
            }
            for database_id in self.database_ids
        }

    def _get_property_definitions(self, database_id):
        def get_property_type(property_type_str):
            if PropertyType.has_value(property_type_str):
                return PropertyType(property_type_str)
            else:
                return PropertyType.UNKNOWN

        database_url = self.DATABASES_URL + database_id
        properties = requests.get(database_url, headers=self._headers).json()["properties"]
        return [
            PropertyDefinition(prop_name, get_property_type(prop_object["type"]))
            for prop_name, prop_object in properties.items()
        ]

    def _get_page_properties(self, page: dict) -> pd.Series:
        properties = {
            property_name: self._decoder.decode(property_data)
            for property_name, property_data in page["properties"].items()
        }

        return pd.Series(properties, name=page.get("id", None))

    def get_database(self, database_id):
        """
        Read Notion database and return a Pandas DataFrame

        :param database_id: id of database you want to retrieve
        :type database_id: str
        :return: dataframe of the database
        :rtype: pd.DataFrame
        """
        database_query_url = self.DATABASES_URL + database_id + "/query"
        pages_raw = self._get_all_pages(database_query_url)
        pages = [
            self._get_page_properties(page)
            for page in pages_raw
        ]

        if pages:
            return pd.concat(pages, axis="columns").T
        else:
            return pd.DataFrame(
                [],
                columns=self._property_types[database_id].keys()
            )

    def _get_all_pages(self, database_query_url):
        next_cursor = None
        has_more = True
        segments = []
        while has_more:
            print("Get segment")
            pages, has_more, next_cursor = self._get_results_segment(database_query_url, next_cursor)
            segments.append(pages)

        return chain.from_iterable(segments)

    def _get_results_segment(self, database_query_url, start_cursor):
        response = requests.post(
            database_query_url,
            headers=self._headers,
            json=dict(
                start_cursor=start_cursor
            ) if start_cursor else {}
        )
        data = response.json()
        pages = data["results"]
        next_cursor = data["next_cursor"]
        has_more = data["has_more"]

        return pages, has_more, next_cursor

    def _create_page_properties(self, database_id, page_properties: List[PropertyValue]):
        properties = {
            page_property.name: self._encoder.encode(
                page_property.value, self._property_types[database_id][page_property.name]
            )
            for page_property in page_properties
        }

        return {
            "parent": {"database_id": database_id},
            "properties": properties
        }

    def create_page(self, database_id, page_properties: List[PropertyValue]):
        """
        Add Notion page to database

        :param database_id: id of database you want to add a page to
        :type database_id: str
        :param page_properties: property values of new page
        :type page_properties: List[:class:`~.notion_property_encoder.PropertyValue`]
        """

        new_page_data = self._create_page_properties(database_id, page_properties)

        data = json.dumps(new_page_data)
        requests.post(self.CREATE_URL, headers=self._headers, data=data)
