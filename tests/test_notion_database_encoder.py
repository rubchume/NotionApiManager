import unittest

import pandas as pd

from notionapimanager.notion_property_encoder import NotionPropertyEncoder, PropertyType


class NotionPropertyEncoderTests(unittest.TestCase):
    def test_encode_text(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode("some random text", PropertyType.TEXT)
        # Then
        self.assertEqual(
            result,
            {
                "text": {"content": "some random text"}
            }
        )

    def test_encode_rich_text(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode("some random text", PropertyType.RICH_TEXT)
        # Then
        self.assertEqual(
            result,
            {
                "rich_text": [
                    {
                        "text": {"content": "some random text"}
                    }
                ]
            }
        )

    def test_encode_title(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode("some random text", PropertyType.TITLE)
        # Then
        self.assertEqual(
            result,
            {
                "title": [
                    {
                        "text": {"content": "some random text"}
                    }
                ]
            }
        )

    def test_encode_select(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode("option 1", PropertyType.SELECT)
        # Then
        self.assertEqual(
            result,
            {
                "select": {"name": "option 1"}
            }
        )

    def test_encode_date(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode(pd.to_datetime("2022/3/4"), PropertyType.DATE)
        # Then
        self.assertEqual(
            {
                "date": {"start": "2022-03-04", "end": None, "time_zone": None}
            },
            result
        )

    def test_encode_checkbox(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode(True, PropertyType.CHECKBOX)
        # Then
        self.assertEqual(
            {
                "checkbox": True
            },
            result
        )

    def test_encode_number(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode(45, PropertyType.NUMBER)
        # Then
        self.assertEqual(
            {
                "number": 45
            },
            result
        )

    def test_encode_relation(self):
        # Given
        encoder = NotionPropertyEncoder()
        # When
        result = encoder.encode(45, PropertyType.NUMBER)
        # Then
        self.assertEqual(
            {
                "number": 45
            },
            result
        )
