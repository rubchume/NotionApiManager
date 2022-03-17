Data Types
==========

In Notion, each element of a *database* is called a *page*.
Each page can have multiple *properties*, and each property has a *type*.

These are the property types that this package can handle:

- text
- rich_text (partially covered)
- select
- title (partially covered)
- date (partially covered)
- checkbox
- number

Different Notion property types match with sensible Pandas DataFrame column types.

See the main class :py:class:`notionapimanager.notion_database_api_manager.NotionDatabaseApiManager`.
