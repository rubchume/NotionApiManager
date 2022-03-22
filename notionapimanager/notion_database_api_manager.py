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
        database_url = self.DATABASES_URL + database_id
        properties = requests.get(database_url, headers=self._headers).json()["properties"]
        return [
            PropertyDefinition(prop_name, PropertyType(prop_object["type"]))
            for prop_name, prop_object in properties.items()
        ]

    def _get_page_properties(self, page: dict) -> pd.Series:
        properties = {
            property_name: self._decoder.decode(property_data)
            for property_name, property_data in page["properties"].items()
        }

        return pd.Series(properties)

    def get_database(self, database_id):
        """
        Read Notion database and return a Pandas DataFrame

        :param database_id: id of database you want to retrieve
        :type database_id: str
        :return: dataframe of the database
        :rtype: pd.DataFrame
        """
        database_query_url = self.DATABASES_URL + database_id + "/query"
        response = requests.post(database_query_url, headers=self._headers)
        data = response.json()
        pages = [
            self._get_page_properties(page)
            for page in data["results"]
        ]

        return pd.concat(pages, axis="columns").T

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
        print(new_page_data)
        response = requests.post(self.CREATE_URL, headers=self._headers, data=data)

        print(response.json())
