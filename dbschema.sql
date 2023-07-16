-- SEQUENCE: public.gebref_id_seq

-- DROP SEQUENCE public.gebref_id_seq;

CREATE SEQUENCE public.gebref_id_seq;

ALTER SEQUENCE public.gebref_id_seq
    OWNER TO postgres;

------------------------------------------------------------

-- Table: public.gebref

 DROP TABLE public.gebref;

CREATE TABLE public.gebref
(
    "NBA" character varying COLLATE pg_catalog."default",
    "OI" character varying COLLATE pg_catalog."default",
    qualitaet character varying COLLATE pg_catalog."default",
    land character varying COLLATE pg_catalog."default",
    regbez character varying COLLATE pg_catalog."default",
    kreis character varying COLLATE pg_catalog."default",
    gemeinde character varying COLLATE pg_catalog."default",
    gdeteil character varying COLLATE pg_catalog."default",
    strasse character varying COLLATE pg_catalog."default",
    hnr character varying COLLATE pg_catalog."default",
    zusatz character varying COLLATE pg_catalog."default",
    rechts character varying COLLATE pg_catalog."default",
    hoch character varying COLLATE pg_catalog."default",
    strassenname character varying COLLATE pg_catalog."default",
    adresse character varying COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('gebref_id_seq'::regclass),
    geom4647 geometry,
    geom25832 geometry,
    geom31466 geometry,
    gemeindename character varying COLLATE pg_catalog."default",
    CONSTRAINT gebref_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gebref
    OWNER to postgres;


---------------------------------------------------------------------

-- Table: public.gebref_schluessel

 DROP TABLE public.gebref_schluessel;

CREATE TABLE public.gebref_schluessel
(
    field_1 character varying COLLATE pg_catalog."default",
    field_2 character varying COLLATE pg_catalog."default",
    field_3 character varying COLLATE pg_catalog."default",
    field_4 character varying COLLATE pg_catalog."default",
    field_5 character varying COLLATE pg_catalog."default",
    field_6 character varying COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gebref_schluessel
    OWNER to postgres;

-------------------------------------------------------------------------

-- Table: public.gmadressen

 DROP TABLE public.gmadressen;

CREATE TABLE public.gmadressen
(
    gemeinde_stadt character varying COLLATE pg_catalog."default",
    ortsteil character varying COLLATE pg_catalog."default",
    strassenschluessel character varying COLLATE pg_catalog."default",
    strassenname character varying COLLATE pg_catalog."default",
    hsnr character varying COLLATE pg_catalog."default",
    ostwert character varying COLLATE pg_catalog."default",
    nordwert character varying COLLATE pg_catalog."default",
    geom25832 geometry,
    geom31466 geometry,
    nummernteil character varying COLLATE pg_catalog."default",
    buchstaben character varying COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gmadressen
    OWNER to postgres;


