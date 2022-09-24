-- c
select count(*) from dow30_2018;
-- d
select count(*) from dow30_2018 where ticker = 'CAT';
-- e
select ticker, count(*) from dow30_2018 
	group by ticker;
-- f
select ticker, count(*) 
	from dow30_2018 
	group by ticker
	order by ticker
;
-- g
select ticker, open, date from dow30_2018;
-- h
select ticker, max(close) from dow30_2018
	group by ticker;
-- i
select ticker, max(close) as max_close into dow30_max_close_2018
	from dow30_2018
	group by ticker;
-- j
select * from dow30_max_close_2018;
-- k
select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018
	join dow30_max_close_2018 on dow30_2018.close = dow30_max_close_2018.max_close;

select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018, dow30_max_close_2018
    where dow30_2018.ticker = dow30_max_close_2018.ticker and dow30_2018.close = dow30_max_close_2018.max_close;

-- l
select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018
	join dow30_max_close_2018 on dow30_2018.close = dow30_max_close_2018.max_close
	order by ticker;

select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018, dow30_max_close_2018
    where dow30_2018.ticker = dow30_max_close_2018.ticker and dow30_2018.close = dow30_max_close_2018.max_close
	order by ticker;

-- m
select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018
	join dow30_max_close_2018 on dow30_2018.close = dow30_max_close_2018.max_close
	order by close desc;

select dow30_2018.ticker, dow30_2018.close, dow30_2018.date from dow30_2018, dow30_max_close_2018
    where dow30_2018.ticker = dow30_max_close_2018.ticker and dow30_2018.close = dow30_max_close_2018.max_close
	order by close desc;

-- n
with start_ as (
	select ticker, open as start_open
		from dow30_2018
		where date = '2018-01-02'
		order by ticker
)
, end_ as (
	select ticker, adjclose as end_close
		from dow30_2018
		where date = '2018-12-31'
		order by ticker
)
select 
	start_.ticker, start_.start_open, end_.end_close,
	100*(end_.end_close - start_.start_open)/start_.start_open as annual_returns
	from start_
	join end_ on start_.ticker = end_.ticker
	where 100*(end_.end_close - start_.start_open)/start_.start_open >= 0
	order by annual_returns desc

;







