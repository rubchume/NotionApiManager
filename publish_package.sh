#!/bin/bash
source PyPI_credentials

echo "Publish package"
./prepare_documentation.sh
poetry build
poetry publish -u $USER -p $PASSWORD
