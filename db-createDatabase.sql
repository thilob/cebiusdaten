-- Schritt 1: Benutzer erstellen
-- Notwendig: Account mit Superuser-Eigenschaften, z.B. user: postgres
-- Role: cebiusdaten
DROP DATABASE IF EXISTS cebiusdaten;
DROP ROLE IF EXISTS cebiusdaten;

CREATE ROLE cebiusdaten WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:5Mq5l+WK6btSCYz5Y/oiAQ==$RAzWRLbYWb/LqRo03UN6uTbUbfbX4YBYVZIIkgPLc4w=:TqRN/9cLf9yhZVfTJkfhBtKczgsvLInVolXKEn8NoQ4=';

  -- Schritt 2: Datenbank erstellen
  -- Database: cebiusdaten

CREATE DATABASE cebiusdaten
    WITH
    OWNER = cebiusdaten
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT CREATE, CONNECT ON DATABASE cebiusdaten TO cebiusdaten;
GRANT TEMPORARY ON DATABASE cebiusdaten TO cebiusdaten WITH GRANT OPTION;
\connect cebiusdaten
--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--
CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


-- Schritt 3: Tabellen und andere Objekte anlegen


CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
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
-- Name: gebref.geom25832; Type: TABLE; Schema: public; Owner: cebiusdaten
--

CREATE TABLE public."gebref.geom25832" (
    id_0 integer NOT NULL,
    geom25832 public.geometry(Point,25832)
);


ALTER TABLE public."gebref.geom25832" OWNER TO cebiusdaten;

--
-- Name: gebref.geom25832_id_0_seq; Type: SEQUENCE; Schema: public; Owner: cebiusdaten
--

CREATE SEQUENCE public."gebref.geom25832_id_0_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."gebref.geom25832_id_0_seq" OWNER TO cebiusdaten;

--
-- Name: gebref.geom25832_id_0_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cebiusdaten
--

ALTER SEQUENCE public."gebref.geom25832_id_0_seq" OWNED BY public."gebref.geom25832".id_0;


--
-- Name: gmadressen; Type: TABLE; Schema: public; Owner: cebiusdaten
--

CREATE TABLE public.gmadressen (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    gemeinde_stadt character varying,
    ortsteil character varying,
    strassenschluessel character varying,
    strassenname character varying,
    hsnr character varying,
    ostwert character varying,
    nordwert character varying,
    nummernteil character varying,
    buchstaben character varying,
    geom25832 public.geometry(Point,25832),
    geom31466 public.geometry(Point,31466)
);


ALTER TABLE public.gmadressen OWNER TO cebiusdaten;

--
-- Name: gebref.geom25832 id_0; Type: DEFAULT; Schema: public; Owner: cebiusdaten
--

ALTER TABLE ONLY public."gebref.geom25832" ALTER COLUMN id_0 SET DEFAULT nextval('public."gebref.geom25832_id_0_seq"'::regclass);


--
-- Name: gebref.geom25832 gebref.geom25832_pkey; Type: CONSTRAINT; Schema: public; Owner: cebiusdaten
--

ALTER TABLE ONLY public."gebref.geom25832"
    ADD CONSTRAINT "gebref.geom25832_pkey" PRIMARY KEY (id_0);


--
-- Name: gmadressen gmadressem_pkey; Type: CONSTRAINT; Schema: public; Owner: cebiusdaten
--

ALTER TABLE ONLY public.gmadressen
    ADD CONSTRAINT gmadressem_pkey PRIMARY KEY (id);


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
