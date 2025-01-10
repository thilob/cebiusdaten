--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS cebiusdaten;
--
-- Name: cebiusdaten; Type: DATABASE; Schema: -; Owner: cebiusdaten
--

CREATE DATABASE cebiusdaten WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';


ALTER DATABASE cebiusdaten OWNER TO cebiusdaten;

\connect cebiusdaten

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: gebref; Type: TABLE; Schema: public; Owner: cebiusdaten
--

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

--
-- Name: idx_gemeinde; Type: INDEX; Schema: public; Owner: cebiusdaten
--

CREATE INDEX idx_gemeinde ON public.gebref USING btree (landschl, land, regbezschl, regbez, kreisschl, kreis, gmdschl, gmd);


--
-- Name: DATABASE cebiusdaten; Type: ACL; Schema: -; Owner: cebiusdaten
--

REVOKE CONNECT,TEMPORARY ON DATABASE cebiusdaten FROM PUBLIC;
REVOKE ALL ON DATABASE cebiusdaten FROM cebiusdaten;
GRANT CREATE,CONNECT ON DATABASE cebiusdaten TO cebiusdaten;
GRANT TEMPORARY ON DATABASE cebiusdaten TO cebiusdaten WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

