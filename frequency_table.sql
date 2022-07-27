-- MS SQL

DECLARE @N INT
SET @N = 10

SELECT x.start_interval, x.end_interval, COUNT(x.user_id) as frequency
FROM
	(SELECT *,
		(SELECT MIN(metric_value) FROM table) + @N * (FLOOR((metric_value - (SELECT MIN(metric_value) FROM table)) / @N)) as start_interval,
		(SELECT MIN(metric_value) FROM table) + @N * (FLOOR((metric_value - (SELECT MIN(metric_value) FROM table)) / @N) + 1) as end_interval
	FROM table) x
GROUP BY x.start_interval, x.end_interval
ORDER BY x.start_interval

-- Будут пропущены интервалы без значений, но это не испортит гистограмму (при отрисовке на числовой оси Х)
