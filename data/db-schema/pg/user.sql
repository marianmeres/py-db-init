
-- ## require __extensions__
-- ## require __functions__

DROP TABLE IF EXISTS "TBLPREFIX____user" CASCADE;

CREATE TABLE "TBLPREFIX____user"(
    id              VARCHAR(128) PRIMARY KEY DEFAULT gen_random_uuid()
    , custom_id     VARCHAR(255)
    , type          VARCHAR(255) -- any label, e.g. bot | agent | guest | ...
    , email         VARCHAR(255)
    , first_name    VARCHAR(255)
    , last_name     VARCHAR(255)
    , meta          JSONB NOT NULL DEFAULT '{}'
    , created       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
    , updated       TIMESTAMP WITH TIME ZONE

    -- flag nice in theory, but more work in real life, never used
    -- , is_deleted    SMALLINT NOT NULL DEFAULT 0 CHECK (is_deleted = 1 OR is_deleted = 0)
);

CREATE UNIQUE INDEX TBLPREFIX____user__email     ON "TBLPREFIX____user"(email);
-- CREATE        INDEX TBLPREFIX____user__active    ON "TBLPREFIX____user"(id, is_deleted);
CREATE UNIQUE INDEX TBLPREFIX____user__custom_id ON "TBLPREFIX____user"(custom_id);

CREATE TRIGGER TBLPREFIX____user__lower_email_trigger BEFORE INSERT OR UPDATE ON "TBLPREFIX____user"
    FOR EACH ROW EXECUTE PROCEDURE trim_lower_email();
