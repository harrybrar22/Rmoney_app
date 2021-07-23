pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump:   hypertable
pg_dump: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: Consider using a full dump instead of a --data-only dump to avoid this problem.
pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump:   chunk
pg_dump: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: Consider using a full dump instead of a --data-only dump to avoid this problem.
--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7
-- Dumped by pg_dump version 12.7

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
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data';


--
-- Name: exchange_enum; Type: TYPE; Schema: public; Owner: rootuser
--

CREATE TYPE public.exchange_enum AS ENUM (
    'NSE',
    'BSE'
);


ALTER TYPE public.exchange_enum OWNER TO rootuser;

--
-- Name: instrument_type_enum; Type: TYPE; Schema: public; Owner: rootuser
--

CREATE TYPE public.instrument_type_enum AS ENUM (
    'EQ',
    'OPT',
    'IND',
    'FUT'
);


ALTER TYPE public.instrument_type_enum OWNER TO rootuser;

--
-- Name: option_typ_enum; Type: TYPE; Schema: public; Owner: rootuser
--

CREATE TYPE public.option_typ_enum AS ENUM (
    'CE',
    'PE',
    'null'
);


ALTER TYPE public.option_typ_enum OWNER TO rootuser;

--
-- Name: segment_enum; Type: TYPE; Schema: public; Owner: rootuser
--

CREATE TYPE public.segment_enum AS ENUM (
    'NSE',
    'NFO-OPT',
    'NFO-FUT'
);


ALTER TYPE public.segment_enum OWNER TO rootuser;

--
-- Name: get_fut_opt_symbol(); Type: FUNCTION; Schema: public; Owner: rootuser
--

CREATE FUNCTION public.get_fut_opt_symbol() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.trading_symbol IN (select trading_symbol FROM instrument WHERE instrument.type = 'FUT' OR instrument.type = 'OPT') 
THEN
RETURN NEW;
ELSE
RAISE EXCEPTION 'trading symbol doesnt exist';
END IF;
END;
$$;


ALTER FUNCTION public.get_fut_opt_symbol() OWNER TO rootuser;

--
-- Name: get_future_symbol(); Type: FUNCTION; Schema: public; Owner: rootuser
--

CREATE FUNCTION public.get_future_symbol() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.trading_symbol IN (select trading_symbol FROM instrument WHERE instrument.type = 'FUT') 
THEN
RETURN NEW;
ELSE
RAISE EXCEPTION 'trading symbol doesnt exist';
END IF;
END;
$$;


ALTER FUNCTION public.get_future_symbol() OWNER TO rootuser;

--
-- Name: get_index_symbol(); Type: FUNCTION; Schema: public; Owner: rootuser
--

CREATE FUNCTION public.get_index_symbol() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.trading_symbol IN (select trading_symbol FROM instrument WHERE instrument.type = 'IND') 
THEN
RETURN NEW;
ELSE
RAISE EXCEPTION 'trading symbol doesnt exist';
END IF;
END;
$$;


ALTER FUNCTION public.get_index_symbol() OWNER TO rootuser;

--
-- Name: get_option_symbol(); Type: FUNCTION; Schema: public; Owner: rootuser
--

CREATE FUNCTION public.get_option_symbol() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.trading_symbol IN (select trading_symbol FROM instrument WHERE instrument.type = 'OPT') 
THEN
RETURN NEW;
ELSE
RAISE EXCEPTION 'trading symbol doesnt exist';
END IF;
END;
$$;


ALTER FUNCTION public.get_option_symbol() OWNER TO rootuser;

--
-- Name: get_stock_symbol(); Type: FUNCTION; Schema: public; Owner: rootuser
--

CREATE FUNCTION public.get_stock_symbol() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF NEW.trading_symbol IN (select trading_symbol FROM instrument WHERE instrument.type = 'EQ') 
THEN
RETURN NEW;
ELSE
RAISE EXCEPTION 'trading symbol doesnt exist';
END IF;
END;
$$;


ALTER FUNCTION public.get_stock_symbol() OWNER TO rootuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: futures; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.futures (
    trading_symbol character varying(255) NOT NULL,
    underlying_symbol character varying,
    tick_size double precision DEFAULT 0.05,
    lot_size integer DEFAULT 1,
    segment public.segment_enum,
    exchange public.exchange_enum,
    listed_at timestamp without time zone,
    expiry_date date
);


ALTER TABLE public.futures OWNER TO rootuser;

--
-- Name: futures_minute; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.futures_minute (
    trading_symbol character varying(255) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume integer,
    open_interest integer
);


ALTER TABLE public.futures_minute OWNER TO rootuser;

--
-- Name: futures_opt_bhav; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.futures_opt_bhav (
    trading_symbol character varying(255) NOT NULL,
    expiry_date date,
    strike_pr integer,
    option_typ public.option_typ_enum,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    settle_pr double precision,
    contracts integer,
    val_inlakh double precision,
    open_int integer,
    chg_in_oi integer,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.futures_opt_bhav OWNER TO rootuser;

--
-- Name: index; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.index (
    trading_symbol character varying NOT NULL,
    tick_size double precision,
    exchange public.exchange_enum
);


ALTER TABLE public.index OWNER TO rootuser;

--
-- Name: index_minute; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.index_minute (
    trading_symbol character varying NOT NULL,
    datetime timestamp without time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision
);


ALTER TABLE public.index_minute OWNER TO rootuser;

--
-- Name: instrument; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.instrument (
    trading_symbol character varying(255) NOT NULL,
    type public.instrument_type_enum NOT NULL
);


ALTER TABLE public.instrument OWNER TO rootuser;

--
-- Name: options; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.options (
    trading_symbol character varying(255) NOT NULL,
    underlying_symbol character varying(255),
    strike double precision,
    "right" public.option_typ_enum,
    tick_size double precision DEFAULT 0.05,
    lot_size integer DEFAULT 1,
    segment public.segment_enum,
    exchange public.exchange_enum,
    listed_at timestamp without time zone,
    expiry_date date
);


ALTER TABLE public.options OWNER TO rootuser;

--
-- Name: options_minute; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.options_minute (
    trading_symbol character varying(255) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume integer,
    open_interest integer
);


ALTER TABLE public.options_minute OWNER TO rootuser;

--
-- Name: stocks; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.stocks (
    trading_symbol character varying(255) NOT NULL,
    company_name character varying(255),
    tick_size double precision DEFAULT 0.05,
    lot_size integer DEFAULT 1,
    exchange public.exchange_enum,
    listed_at timestamp without time zone
);


ALTER TABLE public.stocks OWNER TO rootuser;

--
-- Name: stocks_bhav; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.stocks_bhav (
    trading_symbol character varying(255) NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    last double precision,
    prev_close double precision,
    total_trade_qty bigint,
    total_trade_val double precision,
    "timestamp" timestamp without time zone NOT NULL,
    total_trades integer,
    isin character varying(255)
);


ALTER TABLE public.stocks_bhav OWNER TO rootuser;

--
-- Name: stocks_minute; Type: TABLE; Schema: public; Owner: rootuser
--

CREATE TABLE public.stocks_minute (
    trading_symbol character varying(255) NOT NULL,
    datetime timestamp without time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume integer
);


ALTER TABLE public.stocks_minute OWNER TO rootuser;

--
-- Name: futures_minute futures_minute_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures_minute
    ADD CONSTRAINT futures_minute_pkey PRIMARY KEY (trading_symbol, datetime);


--
-- Name: futures_opt_bhav futures_opt_bhav_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures_opt_bhav
    ADD CONSTRAINT futures_opt_bhav_pkey PRIMARY KEY (trading_symbol, "timestamp");


--
-- Name: futures futures_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures
    ADD CONSTRAINT futures_pkey PRIMARY KEY (trading_symbol);


--
-- Name: index_minute index_minute_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.index_minute
    ADD CONSTRAINT index_minute_pkey PRIMARY KEY (trading_symbol, datetime);


--
-- Name: index index_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.index
    ADD CONSTRAINT index_pkey PRIMARY KEY (trading_symbol);


--
-- Name: instrument instrument_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.instrument
    ADD CONSTRAINT instrument_pkey PRIMARY KEY (trading_symbol);


--
-- Name: options_minute options_minute_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.options_minute
    ADD CONSTRAINT options_minute_pkey PRIMARY KEY (trading_symbol, datetime);


--
-- Name: options options_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (trading_symbol);


--
-- Name: stocks_bhav stocks_bhav_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks_bhav
    ADD CONSTRAINT stocks_bhav_pkey PRIMARY KEY (trading_symbol, "timestamp");


--
-- Name: stocks_minute stocks_minute_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks_minute
    ADD CONSTRAINT stocks_minute_pkey PRIMARY KEY (trading_symbol, datetime);


--
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (trading_symbol);


--
-- Name: futures_minute_datetime_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX futures_minute_datetime_idx ON public.futures_minute USING btree (datetime DESC);


--
-- Name: futures_opt_bhav_timestamp_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX futures_opt_bhav_timestamp_idx ON public.futures_opt_bhav USING btree ("timestamp" DESC);


--
-- Name: index_minute_datetime_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX index_minute_datetime_idx ON public.index_minute USING btree (datetime DESC);


--
-- Name: options_minute_datetime_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX options_minute_datetime_idx ON public.options_minute USING btree (datetime DESC);


--
-- Name: stocks_bhav_timestamp_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX stocks_bhav_timestamp_idx ON public.stocks_bhav USING btree ("timestamp" DESC);


--
-- Name: stocks_minute_datetime_idx; Type: INDEX; Schema: public; Owner: rootuser
--

CREATE INDEX stocks_minute_datetime_idx ON public.stocks_minute USING btree (datetime DESC);


--
-- Name: futures futures; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER futures BEFORE INSERT ON public.futures FOR EACH ROW EXECUTE FUNCTION public.get_future_symbol();


--
-- Name: futures_minute futures_minute; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER futures_minute BEFORE INSERT ON public.futures_minute FOR EACH ROW EXECUTE FUNCTION public.get_future_symbol();


--
-- Name: futures_opt_bhav futures_opt_bhav; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER futures_opt_bhav BEFORE INSERT ON public.futures_opt_bhav FOR EACH ROW EXECUTE FUNCTION public.get_fut_opt_symbol();


--
-- Name: index index; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER index BEFORE INSERT ON public.index FOR EACH ROW EXECUTE FUNCTION public.get_index_symbol();


--
-- Name: index_minute index_minute; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER index_minute BEFORE INSERT ON public.index_minute FOR EACH ROW EXECUTE FUNCTION public.get_index_symbol();


--
-- Name: options options; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER options BEFORE INSERT ON public.options FOR EACH ROW EXECUTE FUNCTION public.get_option_symbol();


--
-- Name: options_minute options_minute; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER options_minute BEFORE INSERT ON public.options_minute FOR EACH ROW EXECUTE FUNCTION public.get_option_symbol();


--
-- Name: stocks stocks; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER stocks BEFORE INSERT ON public.stocks FOR EACH ROW EXECUTE FUNCTION public.get_stock_symbol();


--
-- Name: stocks_bhav stocks_bhav; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER stocks_bhav BEFORE INSERT ON public.stocks_bhav FOR EACH ROW EXECUTE FUNCTION public.get_stock_symbol();


--
-- Name: stocks_minute stocks_minute; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER stocks_minute BEFORE INSERT ON public.stocks_minute FOR EACH ROW EXECUTE FUNCTION public.get_stock_symbol();


--
-- Name: futures_minute ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.futures_minute FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: futures_opt_bhav ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.futures_opt_bhav FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: index_minute ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.index_minute FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: options_minute ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.options_minute FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: stocks_bhav ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.stocks_bhav FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: stocks_minute ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: rootuser
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.stocks_minute FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: futures_minute futures_minute_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures_minute
    ADD CONSTRAINT futures_minute_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: futures_opt_bhav futures_opt_bhav_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures_opt_bhav
    ADD CONSTRAINT futures_opt_bhav_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: futures futures_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.futures
    ADD CONSTRAINT futures_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: index_minute index_minute_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.index_minute
    ADD CONSTRAINT index_minute_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: index index_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.index
    ADD CONSTRAINT index_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: options_minute options_minute_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.options_minute
    ADD CONSTRAINT options_minute_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: options options_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: stocks_bhav stocks_bhav_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks_bhav
    ADD CONSTRAINT stocks_bhav_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: stocks_minute stocks_minute_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks_minute
    ADD CONSTRAINT stocks_minute_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- Name: stocks stocks_trading_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rootuser
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_trading_symbol_fkey FOREIGN KEY (trading_symbol) REFERENCES public.instrument(trading_symbol);


--
-- PostgreSQL database dump complete
--

