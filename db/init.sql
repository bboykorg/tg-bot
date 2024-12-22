

CREATE TABLE public.score (
    score integer DEFAULT 0 NOT NULL,
    "ID" integer NOT NULL,
    "ID_user" bigint NOT NULL
);

ALTER TABLE public.score ALTER COLUMN "ID" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."score_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000
    CACHE 1
);

SELECT pg_catalog.setval('public."score_ID_seq"', 1, true);

ALTER TABLE ONLY public.score
    ADD CONSTRAINT score_pkey PRIMARY KEY ("ID");
