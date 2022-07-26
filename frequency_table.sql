-- Як за допомогою SQL-запиту створити гістограму із розміром бінів N?
-- Гистограмму - никак, но можно сделать интервальную таблицу частот

-- MS SQL
DECLARE @N INT
SET @N = 10

SELECT x.interval, COUNT(x.user_id) as frequency
FROM
  (SELECT *,
  CONCAT(
         CAST(
            (SELECT MIN(metric_value) FROM table1) + 
            @N * (FLOOR((metric_value - (SELECT MIN(metric_value) FROM table1)) / @N) + 1) 
            as varchar), -- начало интервала
         ' - ',
         CAST(
            (SELECT MIN(metric_value) FROM table1) + 
            @N * (FLOOR((metric_value - (SELECT MIN(metric_value) FROM table1)) / @N) + 2) 
            as varchar) -- конец интервала == начало следующего интервала
  ) as interval -- 
  FROM table_) x
GROUP BY x.interval