# Introduction

This package implements a wrapper class around the official [Notion API](https://developers.notion.com/).

[Notion](https://www.notion.so/) app has changed forever the way millions of users take notes.

At the moment of writing these lines, even if there are strong competitors like Obsidian or LogSeq that out-compete Notion in the task of creating a *second brain*, Notion still has the edge as the most balanced note-taking app. It might not be the best in anything, but it is excellent in everything, and that balance is what makes it my preferred option when it comes taking notes, manage projects and organizing knowledge.

One of the great things of Notion is that its API is simple and easy to use. However, for most common operations it could be even simpler.

This project is a small Python wrapper around the existing Notion API so creating new pages and consuming existing information becomes a matter of writing a few lines.

It makes it easier to read databases as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and to create new registries.

This package published in **PyPI** ([PyPI](https://pypi.org/project/notionapimanager/)) and documented in ReadTheDocs ([Documentation](https://notionapimanager.readthedocs.io/en/latest/)).

It has been developed using Continuous Integration and Continuous Development pipeline (CI/CD).

# Approach

There has been a strong intention of using the least amount of third party packages. The only one on which I relied is Pandas. The rest is implemented using the built-in packages available in Python 3.

The documentation has been generated automatically with **Sphinx** and published in ReadTheDocs.

The CI/CD pipeline (the whole process testing and deploying the new versions of the package) is done by running a **Gitlab CI Pipeline**.

# How to use

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

