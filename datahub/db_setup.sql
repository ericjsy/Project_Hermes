CREATE SCHEMA IF NOT EXISTS binance;

CREATE TABLE binance.raw_data
(ID serial PRIMARY KEY
,symbol varchar(7) NOT NULL
,price_change double precision NOT NULL
,price_change_percent double precision NOT NULL
,prev_close_price double precision NOT NULL
,last_price double precision NOT NULL
,last_qty double precision NOT NULL
,bid_price double precision NOT NULL
,ask_price double precision NOT NULL
,open_price double precision NOT NULL
,high_price double precision NOT NULL
,low_price double precision NOT NULL
,volume double precision NOT NULL
,quote_volume double precision NOT NULL
,last_updated timestamp NOT NULL
) WITH (OIDS = FALSE);

CREATE OR REPLACE FUNCTION binance.create_partition_and_insert() RETURNS trigger AS
  $BODY$
    DECLARE
      partition_date TEXT;
      partition_date_offset TEXT;
      partition_schema TEXT;
      partition TEXT;
      partition_offset TEXT;
      partition_table TEXT;
      partition_table_offset TEXT;
    BEGIN
      partition_date := to_char(NEW.last_updated,'YYYY_MM');
      partition_date_offset := to_char(NEW.last_updated + interval '-1 year','YYYY_MM');
      partition_schema := TG_TABLE_SCHEMA || '.' || TG_RELNAME;
      partition := partition_schema || '_' || partition_date;
      partition_offset := partition_schema || '_' || partition_date_offset;
      partition_table := TG_RELNAME || '_' || partition_date;
      partition_table_offset := TG_RELNAME || '_' || partition_date_offset;
      IF EXISTS (SELECT relname FROM pg_class WHERE relname = partition_table_offset) THEN
        RAISE NOTICE 'Inheritence revoked from table patition in previous year: %.', partition_table_offset;
        EXECUTE 'ALTER TABLE ' || partition_offset || ' NO INHERIT ' || partition_schema || ';';
      END IF;
      IF NOT EXISTS (SELECT relname FROM pg_class WHERE relname = partition_table) THEN
        RAISE NOTICE 'A partition has been created: %', partition;
        EXECUTE 'CREATE TABLE ' || partition || ' (check ((date_trunc(''day'', last_updated)::DATE >= date_trunc(''month'', timestamp ''' || NEW.last_updated || ''')::DATE) AND (date_trunc(''day'', last_updated)::DATE < date_trunc(''month'', timestamp ''' || NEW.last_updated + interval '1 month' || ''')::DATE))) INHERITS (' || partition_schema || ');';
        EXECUTE 'CREATE INDEX ' || partition_table || '_idx ON ' || partition || '(last_updated);';
      END IF;
      EXECUTE 'INSERT INTO ' || partition || ' SELECT(' || partition_schema || ' ' || quote_literal(NEW) || ').* RETURNING ID;';
      RETURN NULL;
    END;
  $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER partition_insert_trigger
BEFORE INSERT ON binance.raw_data
FOR EACH ROW EXECUTE PROCEDURE binance.create_partition_and_insert();
