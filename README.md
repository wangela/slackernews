# slackernews
Slacker News is a reporting tool to analyze the logs of a fictional news website.

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
--------+--------------------------+-------------------------------------------------------
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
--------+---------+------------------------------------------------------
name   | text    | not null
bio    | text    |
id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
   "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
   TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

### Table "Log"

Column |           Type           |                    Modifiers                     
--------+--------------------------+--------------------------------------------------
path   | text                     |
ip     | inet                     |
method | text                     |
status | text                     |
time   | timestamp with time zone | default now()
id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
   "log_pkey" PRIMARY KEY, btree (id)

### View "titles-log"
Path format is /article/title so we need to convert the title to its associated id

create view titles-log as
  select path, ip, method, status, time, id

create view articles-log as
  select articles.id, log.ip, log.time, log.status, log.id
  from log join articles
  using
