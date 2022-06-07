import unittest

import pandas as pd
from pandas._testing import assert_frame_equal
import requests_mock

from notionapimanager import NotionDatabaseApiManager
from notionapimanager.notion_database_api_manager import NotionPropertyDecoder, NotionPropertyEncoder, PropertyType
from notionapimanager.notion_property_encoder import PropertyValue


class NotionDatabaseApiManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = NotionDatabaseApiManager("integration_token_1234", ["database_id_12345678"])
        self.manager._property_types = {
            "database_id_12345678": {
                "property1": PropertyType.CHECKBOX,
                "property2": PropertyType.TEXT,
                "property3": PropertyType.SELECT
            }
        }
        self.manager._decoder = NotionPropertyDecoder()
        self.manager._encoder = NotionPropertyEncoder()

    @requests_mock.Mocker(kw="requests_mocker")
    def test_connect(self, requests_mocker):
        # Given
        manager = NotionDatabaseApiManager("integration_token_1234", ["database_id_12345678"])
        requests_mocker.get(
            "https://api.notion.com/v1/databases/database_id_12345678",
            json={
                "properties": {
                    "property1": {"type": "checkbox"},
                    "property2": {"type": "text"}
                }
            }
        )
        expected_property_types = {
            "database_id_12345678": {
                "property1": PropertyType.CHECKBOX,
                "property2": PropertyType.TEXT,
            }
        }
        # When
        manager.connect()
        # Then
        self.assertEqual(
            manager._property_types,
            expected_property_types
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_connect_and_read_unknown_property_type(self, requests_mocker):
        # Given
        manager = NotionDatabaseApiManager("integration_token_1234", ["database_id_12345678"])
        requests_mocker.get(
            "https://api.notion.com/v1/databases/database_id_12345678",
            json={
                "properties": {
                    "property1": {"type": "checkbox"},
                    "property2": {"type": "unknown_type"}
                }
            }
        )
        expected_property_types = {
            "database_id_12345678": {
                "property1": PropertyType.CHECKBOX,
                "property2": PropertyType.UNKNOWN,
            }
        }
        # When
        manager.connect()
        # Then
        self.assertEqual(
            manager._property_types,
            expected_property_types
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_no_rows_returns_empty_dataframe_with_right_columns(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [],
                columns=["property1", "property2", "property3"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_id(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "id": "abcdefg",
                        "properties": {
                            "column1": {
                                "type": "text",
                                "text": "This is the title"
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    ["This is the title"]
                ],
                columns=["column1"],
                index=["abcdefg"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_text_field(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "column1": {
                                "type": "text",
                                "text": "This is the title"
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    ["This is the title"]
                ],
                columns=["column1"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_select_field(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "someProperty": {
                                "type": "select",
                                "select": {"name": "Option1"}
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    ["Option1"]
                ],
                columns=["someProperty"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_rich_text_field(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "someProperty": {
                                "type": "rich_text",
                                "rich_text": [{"plain_text": "This is the text"}]
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    ["This is the text"]
                ],
                columns=["someProperty"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_empty_rich_text_field_does_not_fail(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "someProperty": {
                                "type": "rich_text",
                                "rich_text": []
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    [None]
                ],
                columns=["someProperty"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_database_with_date_field(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "someProperty": {
                                "type": "date",
                                "date": {"start": "2022/3/4"}
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    [pd.to_datetime("2022/3/4")]
                ],
                columns=["someProperty"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_unknown_property_type_returns_the_value_as_it_is(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/databases/database_id_12345678/query",
            json={
                "results": [
                    {
                        "properties": {
                            "someProperty": {
                                "type": "unknownwhatever",
                                "unknownwhatever": {"somefield": "somevalue"}
                            }
                        }
                    },
                ],
                "next_cursor": None,
                "has_more": False
            }
        )
        # When
        response = self.manager.get_database("database_id_12345678")
        # Then
        assert_frame_equal(
            response,
            pd.DataFrame(
                [
                    [{"somefield": "somevalue"}]
                ],
                columns=["someProperty"]
            )
        )

    @requests_mock.Mocker(kw="requests_mocker")
    def test_create_page(self, requests_mocker):
        # Given
        requests_mocker.post(
            "https://api.notion.com/v1/pages",
            json={
                "results": "whatever"
            }
        )
        expected_json = {
            "parent": {"database_id": "database_id_12345678"},
            "properties": {
                "property1": {"checkbox": False},
                "property2": {"text": {"content": "This is some text"}},
                "property3": {"select": {"name": "Option 3 of select"}}
            }
        }
        # When
        self.manager.create_page(
            "database_id_12345678",
            [
                PropertyValue("property1", False),
                PropertyValue("property2", "This is some text"),
                PropertyValue("property3", "Option 3 of select"),
            ]
        )
        # Then
        self.assertEqual(1, requests_mocker.call_count)
        self.assertEqual("POST", requests_mocker.request_history[0].method)
        self.assertEqual("https://api.notion.com/v1/pages", requests_mocker.request_history[0].url)
        self.assertEqual(expected_json, requests_mocker.request_history[0].json())

    @requests_mock.Mocker(kw="requests_mocker")
    def test_get_page_blocks(self, requests_mocker):
        # Given
        requests_mocker.get(
            "https://api.notion.com/v1/blocks/page_id/children",
            json={'object': 'list',
                  'results': [{'object': 'block',
                               'id': '2dcba05b-611a-48b4-a27d-705baca48284',
                               'created_time': '2022-06-06T22:52:00.000Z',
                               'last_edited_time': '2022-06-06T23:09:00.000Z',
                               'created_by': {'object': 'user',
                                              'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
                               'last_edited_by': {'object': 'user',
                                                  'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
                               'has_children': False,
                               'archived': False,
                               'type': 'child_database',
                               'child_database': {'title': 'Ingredientes receta'}},
                              {'object': 'block',
                               'id': 'ad3dd600-2a4e-4169-a499-c7196244ac89',
                               'created_time': '2022-06-04T16:34:00.000Z',
                               'last_edited_time': '2022-06-04T16:34:00.000Z',
                               'created_by': {'object': 'user',
                                              'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
                               'last_edited_by': {'object': 'user',
                                                  'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
                               'has_children': False,
                               'archived': False,
                               'type': 'paragraph',
                               'paragraph': {'color': 'default', 'text': []}}],
                  'next_cursor': None,
                  'has_more': False}
        )
        # When
        blocks = self.manager.get_page_blocks("page_id")
        # Then
        self.assertEqual(
            blocks,
            [{'object': 'block',
              'id': '2dcba05b-611a-48b4-a27d-705baca48284',
              'created_time': '2022-06-06T22:52:00.000Z',
              'last_edited_time': '2022-06-06T23:09:00.000Z',
              'created_by': {'object': 'user',
                             'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
              'last_edited_by': {'object': 'user',
                                 'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
              'has_children': False,
              'archived': False,
              'type': 'child_database',
              'child_database': {'title': 'Ingredientes receta'}},
             {'object': 'block',
              'id': 'ad3dd600-2a4e-4169-a499-c7196244ac89',
              'created_time': '2022-06-04T16:34:00.000Z',
              'last_edited_time': '2022-06-04T16:34:00.000Z',
              'created_by': {'object': 'user',
                             'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
              'last_edited_by': {'object': 'user',
                                 'id': '477cd72a-ba43-4857-aeed-1331957a950d'},
              'has_children': False,
              'archived': False,
              'type': 'paragraph',
              'paragraph': {'color': 'default', 'text': []}}]
        )
