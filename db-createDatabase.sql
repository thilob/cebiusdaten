DROP DATABASE IF EXISTS cebiusdaten;

CREATE DATABASE cebiusdaten
    WITH
    OWNER = cebiusdaten
    ENCODING = 'UTF8'
    LC_COLLATE = 'German_Germany.1252'
    LC_CTYPE = 'German_Germany.1252'
    BUILTIN_LOCALE = 'C.UTF-8'
    LOCALE_PROVIDER = 'builtin'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT CREATE, CONNECT ON DATABASE cebiusdaten TO cebiusdaten;
GRANT TEMPORARY ON DATABASE cebiusdaten TO cebiusdaten WITH GRANT OPTION;


CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';

CREATE TABLE public.gebref (
    nba "char",
    oid character varying(16),
    qua "char",
    landschl character varying(2),
    land character varying,
    regbezschl "char",
    regbez character varying,
    kreisschl character varying(2),
    kreis character varying,
    gmdschl character varying(3),
    gmd character varying,
    ottschl character varying(4),
    ott character varying,
    strschl character varying(5),
    str character varying,
    hnr character varying,
    adz character varying,
    zone integer,
    ostwert numeric(9,3),
    nordwert numeric(10,3),
    datum character varying,
    id uuid DEFAULT public.uuid_generate_v4(),
    geom25832 public.geometry(Point,25832),
    geom31466 public.geometry(Point,31466)
);

ALTER TABLE public.gebref OWNER TO cebiusdaten;

CREATE INDEX idx_gemeinde ON public.gebref USING btree (landschl, land, regbezschl, regbez, kreisschl, kreis, gmdschl, gmd);

REVOKE CONNECT,TEMPORARY ON DATABASE cebiusdaten FROM PUBLIC;
REVOKE ALL ON DATABASE cebiusdaten FROM cebiusdaten;
GRANT CREATE,CONNECT ON DATABASE cebiusdaten TO cebiusdaten;
GRANT TEMPORARY ON DATABASE cebiusdaten TO cebiusdaten WITH GRANT OPTION;
