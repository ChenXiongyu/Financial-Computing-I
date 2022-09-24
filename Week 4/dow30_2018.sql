create table dow30_2018 (
    Date         date,
    Ticker       varchar(8),
    Open         real,
    High         real,
    Low          real,
    Close        real,
    Volume       int,
    AdjClose     real,
    primary key  (Date, Ticker)
);

