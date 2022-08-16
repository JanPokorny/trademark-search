CREATE EXTENSION pg_trgm;

CREATE FUNCTION matchable(s VARCHAR) RETURNS VARCHAR
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT
    RETURN lower(normalize(s, nfkd));

CREATE TABLE trademarks (
    application_number CHAR(9) NOT NULL,
    word_mark_text VARCHAR(255) NOT NULL,
    application_date DATE,
    registration_date DATE,
    expiry_date DATE,
    word_mark_text_matchable VARCHAR(255) NOT NULL GENERATED ALWAYS AS (matchable(word_mark_text)) STORED,
    PRIMARY KEY (application_number)
);

CREATE INDEX trademarks_word_mark_text_matchable_idx ON trademarks USING gin(word_mark_text_matchable gin_trgm_ops);
