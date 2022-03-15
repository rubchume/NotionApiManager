#!/bin/bash
source PyPI_credentials

echo "Publish package"
poetry build
poetry publish -u $USER -p $PASSWORD
