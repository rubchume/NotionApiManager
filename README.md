# Notion API Manager

This package implements a wrapper class around the official [Notion API](https://developers.notion.com/).

It makes it easier to read databases as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and to create new registries.

GitHub [repository](https://github.com/rubchume/NotionApiManager).

[Documentation](https://notionapimanager.readthedocs.io/en/latest/).

[PyPI](https://pypi.org/project/notionapimanager/).

# Steps

## Obtain a Notion integration token

You can do it following the instructions in this [PrettyStatic blog article](https://prettystatic.com/notion-api-python/).

## Install package

Install package from [PyPI](https://pypi.org/project/notionapimanager/).
```shell
pip install notionapimanager
```

## Basic usage of the NotionDatabaseApiManager class
Note: in Notion, a _database_ is what in SQL we would call a _table_.
Hence, a Notion _database_ will be returned as a Pandas DataFrame instance.

```python
from notionapimanager.notion_database_api_manager import NotionDatabaseApiManager
from notionapimanager.notion_property_encoder import PropertyValue

integration_token = "secret_example_integration_token_3147cefa7cd20d4s45677dfasd34"
database_id_1 = "cc147cefa7cd20d4841469ddbd4cd893"
database_id_2 = "cc147cef20d456461469ddbd4das4593"

manager = NotionDatabaseApiManager(integration_token, [database_id_1, database_id_2])
manager.connect()

# Get database 1
manager.get_database(database_id_1)

# Insert a new entry on the database 2
manager.create_page(
    database_id_2,
    [
        PropertyValue("Property Name", "Property value"),
    ]
)
```

