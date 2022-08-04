Usage
=====

.. _NotionDevelopers: https://developers.notion.com/
.. _PandasDataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _PyPI: https://pypi.org/project/notionapimanager/
.. _GitHubRepository: https://github.com/rubchume/NotionApiManager
.. _NotionIntegrationTutorial: https://prettystatic.com/notion-api-python/

Overview
--------

This package implements a wrapper class around the official `Notions Developers page <NotionDevelopers_>`_.

It makes it easier to read databases as `Pandas DataFrames <PandasDataFrame_>`_ and to create new registries.

GitHub `repository <GitHubRepository_>`_.


Steps
-----

Obtain a Notion integration token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can do it following the instructions in this `PrettyStatic blog article <NotionIntegrationTutorial_>`_.

Install package
^^^^^^^^^^^^^^^

Install package from `PyPI <PyPI_>`_:

.. code-block:: console

   (.venv) $ pip install notionapimanager

Basic usage of the NotionDatabaseApiManager class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note: in Notion, a *database* is what in SQL we would call a *table*.
Hence, a Notion *database* will be returned as a `Pandas DataFrame <Pandas DataFrames_>`_ instance.

.. code-block:: python

   from notionapimanager.notion_database_api_manager import NotionDatabaseApiManager
   from notionapimanager.notion_property_encoder import PropertyValue

   integration_token = "secret_example_integration_token_3147cefa7cd20d4s45677dfasd34"
   database_id_1 = "cc147cefa7cd20d4841469ddbd4cd893"
   database_id_2 = "cc147cef20d456461469ddbd4das4593"

   manager = NotionDatabaseApiManager(
       integration_token,
       [database_id_1, database_id_2]
   )
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

   # Get blocks of page
   page_id = "a0259665-56b4-4567-a773-9cd369kg2d6f945"
   manager.get_page_blocks(page_id)
