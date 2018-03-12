CREATE ROLE read_access NOINHERIT;
GRANT USAGE ON SCHEMA binance TO read_access;
GRANT USAGE ON SCHEMA cryptowatch TO read_access;
GRANT SELECT ON ALL TABLES IN SCHEMA binance TO read_access;
GRANT SELECT ON ALL TABLES IN SCHEMA cryptowatch TO read_access;
GRANT read_access TO dt_reader;