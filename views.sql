CREATE VIEW titles_log AS
  SELECT SUBSTRING(path, 10) AS title, time, status
  FROM log;

CREATE VIEW articles_log AS
  SELECT articles.id, authors.name, articles.title, titles_log.time,
  titles_log.status
  FROM titles_log
  LEFT JOIN articles
  ON (titles_log.title = articles.slug)
  LEFT JOIN authors
  ON (articles.author = authors.id)
  WHERE length(titles_log.title) > 0;

CREATE VIEW dates AS
  SELECT to_char(DATE_TRUNC('day', time), 'YYYY-MM-DD') AS date, status
  FROM log;

CREATE VIEW requests AS
  SELECT date, count(*) AS requests
  FROM dates
  GROUP BY date
  ORDER BY requests DESC;

CREATE VIEW errors AS
  SELECT date, count(*) AS errors
  FROM dates
  WHERE status != '200 OK'
  GROUP BY date
  ORDER BY errors DESC;
