-- Table: public.sign

-- DROP TABLE public.sign;

CREATE TABLE public.sign
(
    id integer NOT NULL DEFAULT nextval('sign_id_seq'::regclass),
    name character varying(300) COLLATE pg_catalog."default" NOT NULL,
    email character varying(300) COLLATE pg_catalog."default" NOT NULL,
    profession character varying(500) COLLATE pg_catalog."default",
    comments text COLLATE pg_catalog."default",
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    secret_key character(32) COLLATE pg_catalog."default" NOT NULL,
    published timestamp with time zone,
    serial integer,
    CONSTRAINT sign_pkey PRIMARY KEY (id),
    CONSTRAINT sign_email_unique UNIQUE (email)

)

TABLESPACE pg_default;

ALTER TABLE public.sign
    OWNER to postgres;

-- Index: index_sign_published

-- DROP INDEX public.index_sign_published;

CREATE INDEX index_sign_published
    ON public.sign USING btree
    (published)
    TABLESPACE pg_default;

-- Index: index_sign_secret_key

-- DROP INDEX public.index_sign_secret_key;

CREATE UNIQUE INDEX index_sign_secret_key
    ON public.sign USING btree
    (secret_key COLLATE pg_catalog."default")
    TABLESPACE pg_default;