# 🔎™️ Trademark Search

*Created by **Jan Pokorný** for a Vacuumlabs interview assignment*

## 📜 High-level overview

This is a simple application that allows you to search for trademarks through a HTTP endpoint. It consists of three main parts: the database server (PostgreSQL), the import service, and the API.

### 💾 Database server

The database server is a simple PostgreSQL container, with some initialization logic to crate the tables and matching functions. The fuzzy matching is implemented using the `pg_trgm` extension, which implements trigram matching and indexing. I also considered using Elasticsearch, but it turned out that PostgreSQL's performance for this specific task is very satisfactory.

### 📥 Import service

The import service downloads the opendata dump from EUIPO, parses it, and imports the data into the database. It uses `aria2c` to download the dump, `xq` to parse the XML files and convert to a CSV file, and `psql` to import the CSV file into the database. Currently, the import service only imports the application number, wordmark text, and important dates. It would be possible to import the full dataset as a JSON column (since PostgreSQL has JSON support), but I didn't want to wait that long for the import.

### 🔗 API

The API (built on `fastapi`) consists of a single HTTP endpoint, `GET /trademarks`, which allows to search for trademarks by either exact or fuzzy match. It accepts query parameters `text` (str, the search text), `fuzzy` (bool, default false, whether to perform a non-exact match), and `limit` (int, default 10, the maximum number of results to return). When fuzzy matching, the results are ordered from the most similar to the least similar.

## 📦 Installation

The project will start downloading and importing the data when you run `docker compose up`. If you want to skip the download and parsing stage (recommended, even though I tried to make it fast), download [the prepared file](https://gist.github.com/JanPokorny/fb4f611d351ee110a87269a46d1b7167) and save it to `import/data/items.csv`. By intention, the import service will not import the data if some data already exists in the database, so if the import fails you may need to drop the database volumes and restart the application.


## 🔎 Example

Run the server (`docker compose up`) and then use HTTPie to test:

```bash
$ xh GET :/trademarks text==puf fuzzy==true limit==5

HTTP/1.1 200 OK
Content-Length: 717
Content-Type: application/json
Date: Wed, 17 Aug 2022 10:19:49 GMT
Server: uvicorn

[
    {
        "application_number": "018319502",
        "word_mark_text": "PUFF",
        "application_date": "2020-10-12",
        "registration_date": null,
        "expiry_date": null
    },
    {
        "application_number": "018203300",
        "word_mark_text": "Pufei",
        "application_date": "2020-02-28",
        "registration_date": "2020-06-13",
        "expiry_date": "2030-02-28"
    },
    {
        "application_number": "018187181",
        "word_mark_text": "PUFFY",
        "application_date": "2020-01-24",
        "registration_date": "2020-05-22",
        "expiry_date": "2030-01-24"
    },
    {
        "application_number": "018321417",
        "word_mark_text": "Pup Pup",
        "application_date": "2020-10-14",
        "registration_date": null,
        "expiry_date": null
    },
    {
        "application_number": "018335091",
        "word_mark_text": "PUFF XXL",
        "application_date": "2020-11-10",
        "registration_date": null,
        "expiry_date": null
    }
]
```
