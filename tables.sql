create table if not exists instrument_masters
(
    exchange_segment         varchar(255),
    exchange_instrument_id   bigint,
    instrument_type          int,
    name                     varchar(255),
    description              varchar(255),
    series                   varchar(255),
    name_with_series         varchar(255),
    instrument_id            bigint unique,
    price_band_high          decimal(12, 2),
    price_band_low           decimal(12, 2),
    freeze_qty               bigint,
    tick_size                decimal(12, 2),
    lot_size                 int,
    underlying_instrument_id bigint,
    underlying_index_name    varchar(255),
    contract_expiration      date,
    strike_price             decimal(12, 2),
    option_type              int,
    primary key (exchange_instrument_id, instrument_type, name, description, series, instrument_id)
);

create table if not exists index_constituents
(
    index        varchar(255),
    symbol       varchar(255),
    company_name varchar(255),
    sector       varchar(255),
    weightage    decimal(5, 2),
    primary key (index, symbol, company_name, sector)
);
