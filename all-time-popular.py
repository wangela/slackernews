import psycopg2

DBNAME = "news"
# Check Python code quality using pep8 command line tool
# Refer to PEP8 style guide at https://www.python.org/dev/peps/pep-0008/
# Document SQL views in the README

# Top 3 most popular articles
# Presents the top 3 articles with the most popular article at top
# Popularity defined by number of page views over all time
def top_articles():
    db = psycopg2.connect("dbname=DBNAME")
    curr = db.cursor()
    curr.execute("SELECT title, count(*) AS views FROM articles_log
        WHERE status != '404 NOT FOUND'
        GROUP BY title
        ORDER BY views DESC LIMIT 3;")
    print ("TOP ARTICLES:")
    return curr.fetchall()
    curr.close()
    db.close()

# Most popular article authors
# Presents the authors with the most popular authors at top
# Popularity defined by sum of author's articles page views over all time
def top_authors():
    db = psycopg2.connect("dbname=DBNAME")
    curr = db.cursor()
    curr.execute("SELECT name, count(*) AS views FROM articles_log
        WHERE status != '404 NOT FOUND'
        GROUP BY name ORDER BY views DESC;")
    print ("TOP AUTHORS:")
    return curr.fetchall()
    curr.close()
    db.close()

# Buggy Days
# Presents all the days where more than 1% of requests
#   led to HTTP status errors
def buggy_days():
    db = psycopg2.connect("dbname=DBNAME")
    curr = db.cursor()
    curr.execute("SELECT date, requests, errors, percentage
        FROM (SELECT date, requests, errors,
            trunc(100.0*errors / requests, 2) AS percentage
            FROM requests LEFT JOIN errors
            USING (date)) AS subq
        WHERE percentage > 1.00
        ORDER BY percentage DESC;")
    print ("HIGH ERROR DAYS")
    return curr.fetchall()
    curr.close()
    db.close()


top_articles()
top_authors()
buggy_days()
