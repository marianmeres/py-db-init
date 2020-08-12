
CREATE OR REPLACE FUNCTION trim_lower_email() RETURNS trigger AS
$BODY$
BEGIN
  NEW.email = TRIM(LOWER(NEW.email));
  RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;