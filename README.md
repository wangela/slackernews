# slackernews
Slacker News is a reporting tool to analyze the logs of a fictional news website.

## Setup and Usage
1. Install VirtualBox, which you can
[download from here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

1. Install Vagrant, which you can [download from here](https://www.vagrantup.com/downloads.html)

1. Start and log in to the virtual machine with `vagrant up` followed by
  `vagrant ssh`.

1. Once logged in to the virtual machine, `cd /vagrant` to get to the directory
shared with your regular laptop.

1. Clone this repository to get all the necessary files you'll need.

1. [Download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
and unzip it to reveal `newsdata.sql`, then move it to /vagrant

1. From the directory where your data is stored, load the data with the psql command.
```
$ psql -d news -f newsdata.sql
```

8. Create the necessary views of the database.
```
$ psql -d news -f views.sql
```

9. Run the Python script to generate the output
```
$ python3 all_time_popular.py
```

## Output
This tool produces three reports in plain text:

### Top 3 most popular articles
- Presents the top 3 articles as a sorted list with the most popular article at top
- Popularity defined by number of page views over all time

### Most popular article authors
- Presents the authors in a sorted list with the most popular authors at top
- Popularity defined by sum of author's articles page views over all time

### Buggy Days
- Presents all the days where more than 1% of requests led to HTTP status errors

## Database Structure
The logs are stored in a SQL database with the following structure:

### Table "Articles"

Column |           Type           |                       Modifiers                       
--------|--------------------------|-------------------------------------------------------
author | integer                  | not null
title  | text                     | not null
slug   | text                     | not null
lead   | text                     |
body   | text                     |
time   | timestamp with time zone | default now()
id     | integer                  | not null default nextval('articles_id_seq'::regclass)

Indexes:
   "articles_pkey" PRIMARY KEY, btree (id)
   "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
   "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

### Table "Authors"

Column |  Type   |                      Modifiers                       
--------|--------|------------------------------------------------------
name   | text    | not null
bio    | text    |
id     | integer | not null default nextval('authors_id_seq'::regclass)

Indexes:
   "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
   TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

### Table "Log"

Column |           Type           |                    Modifiers                     
--------|--------------------------|--------------------------------------------------
path   | text                     |
ip     | inet                     |
method | text                     |
status | text                     |
time   | timestamp with time zone | default now()
id     | integer                  | not null default nextval('log_id_seq'::regclass)

Indexes:
   "log_pkey" PRIMARY KEY, btree (id)

## Custom Views
You must create the custom views below before running the Python script.

### View "titles_log"
Path format is /article/title so we need to extract the title (substring
  starting at character 10).

```
CREATE VIEW titles_log AS
  SELECT SUBSTRING(path, 10) AS title, time, status
  FROM log;
```

### View "articles_log"
Create a view associating the article ID with each log entry.

```
CREATE VIEW articles_log AS
  SELECT articles.id, authors.name, articles.title, titles_log.time,
  titles_log.status
  FROM titles_log
  LEFT JOIN articles
  ON (titles_log.title = articles.slug)
  LEFT JOIN authors
  ON (articles.author = authors.id)
  WHERE length(titles_log.title) > 0;
```

### View "dates"
Create a view of the log separating out the date from the timestamp.

```
CREATE VIEW dates AS
  SELECT to_char(DATE_TRUNC('day', time), 'YYYY-MM-DD') AS date, status
  FROM log;
```

### View "requests"
Create a view of the log counting all requests.

```
CREATE VIEW requests AS
  SELECT date, count(*) AS requests
  FROM dates
  GROUP BY date
  ORDER BY requests DESC;
```

### View "errors"
Create a view of the log filtering for just the errors.

```
CREATE VIEW errors AS
  SELECT date, count(*) AS errors
  FROM dates
  WHERE status != '200 OK'
  GROUP BY date
  ORDER BY errors DESC;
```
