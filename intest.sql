--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 15.3

-- Started on 2024-04-30 23:42:53 +05

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 17691)
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying,
    status integer
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17696)
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO postgres;

--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 222
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- TOC entry 3318 (class 2604 OID 17765)
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- TOC entry 3462 (class 0 OID 17691)
-- Dependencies: 221
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.groups VALUES (2, 'Менеджер', 1);
INSERT INTO public.groups VALUES (1, 'Бригадир', 1);
INSERT INTO public.groups VALUES (4, 'Менеджер 2', 1);
INSERT INTO public.groups VALUES (6, 'Администратор Маркетинг', 1);
INSERT INTO public.groups VALUES (7, 'Локальный Маркетинг', 1);
INSERT INTO public.groups VALUES (8, 'Креативные Разработки', 1);
INSERT INTO public.groups VALUES (9, 'Мастер', 1);
INSERT INTO public.groups VALUES (10, 'test', 1);
INSERT INTO public.groups VALUES (11, 'Тестовый', 1);
INSERT INTO public.groups VALUES (3, 'Администратор АРС Розница', 1);
INSERT INTO public.groups VALUES (12, 'cypress', 1);
INSERT INTO public.groups VALUES (13, 'Администратор АРС Фабрика ', 1);
INSERT INTO public.groups VALUES (5, 'some role', 1);
INSERT INTO public.groups VALUES (14, 'Менеджер по работе с подрядчиками', 1);
INSERT INTO public.groups VALUES (15, 'Логистика', 1);
INSERT INTO public.groups VALUES (16, 'Стафф Кухня', 1);
INSERT INTO public.groups VALUES (17, 'Территориальный менеджер', 1);
INSERT INTO public.groups VALUES (18, 'outsource master', 1);
INSERT INTO public.groups VALUES (19, 'HR Department', 1);
INSERT INTO public.groups VALUES (20, 'It Department ', 1);
INSERT INTO public.groups VALUES (21, 'Руководитель отдела инвентарь', 1);
INSERT INTO public.groups VALUES (22, 'Ит Специалист', 1);
INSERT INTO public.groups VALUES (23, 'Руководитель IT отдела', 1);
INSERT INTO public.groups VALUES (24, 'Safia Office', 1);
INSERT INTO public.groups VALUES (25, 'Отдел Видеонаблюдения', 1);
INSERT INTO public.groups VALUES (26, 'Contact center', 1);
INSERT INTO public.groups VALUES (27, 'Менеджер ИТ', 1);
INSERT INTO public.groups VALUES (28, 'Супер админ', 1);


--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 222
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.groups_id_seq', 28, true);


--
-- TOC entry 3320 (class 2606 OID 17790)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3321 (class 1259 OID 17824)
-- Name: ix_groups_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_groups_id ON public.groups USING btree (id);


--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE groups; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.groups TO analytics;


-- Completed on 2024-04-30 23:42:53 +05

--
-- PostgreSQL database dump complete
--

