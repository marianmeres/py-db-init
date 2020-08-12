

DROP TABLE IF EXISTS "TBLPREFIX____setting" CASCADE;

CREATE TABLE "TBLPREFIX____setting" (
    id                  VARCHAR(128) PRIMARY KEY
    , value             JSONB
    , meta              JSONB NOT NULL DEFAULT '{}'
    , created           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
    , updated           TIMESTAMP WITH TIME ZONE
);

