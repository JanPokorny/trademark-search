#!/usr/bin/env ash

set -e

if [ ! -f ./data/items.csv ]; then
  echo '# Downloading archives...'
  aria2c \
    --auto-file-renaming=false \
    --continue=true \
    --check-integrity \
    --metalink-file=./sources.meta4 \
    --dir=./data/archives

  echo '# Unpacking items...'
  find ./data/archives -type f -name '*.zip' \
    | parallel 'unzip -n -j -d ./data/items'

  echo '# Converting items to CSV...'
  find ./data/items -type f -name '*.xml' \
    | parallel 'xq --raw-output -f ./filter.jq' > ./data/items.csv    
else
  echo '# File items.csv already exists, skipping download...'
fi

echo '# Importing CSV to PostgreSQL...'
CONNECTION_STRING="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"
echo $CONNECTION_STRING
while ! pg_isready -d $CONNECTION_STRING; do sleep 1; done
psql -d $CONNECTION_STRING -c '\COPY trademarks FROM STDIN WITH CSV HEADER;' < ./data/items.csv || true  # ignore errors -- data may already be imported
