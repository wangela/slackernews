#! /usr/bin/env python3
import psycopg2


def connect(database_name="news"):
    """
    Connects to the News database

    Args:
        database_name(str): The name of the SQL database

    Returns:
        db: A database connection
        cursor: The connection's cursor in that database

    Raises:
        Prints an error message if the connection fails
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not connect to database {}".format(database_name))


def top_articles():
    """
    Top Articles: Presents the top 3 articles defined by number of page views

    Args:
        none

    Returns:
        A sorted list with the titles of the top 3 articles in decreasing order
        of popularity.
    """
    db, cursor = connect()

    query = """SELECT title, count(*) AS views FROM articles_log
        WHERE status != '404 NOT FOUND'
        GROUP BY title
        ORDER BY views DESC LIMIT 3;"""
    cursor.execute(query)

    print("TOP ARTICLES:")
    return curr.fetchall()
    curr.close()
    db.close()


def top_authors():
    """
    Top Authors: Presents the authors with the most page views across all their
    articles over all time

    Args:
        none

    Returns:
        A sorted list with the names of all authors in decreasing order of
        popularity.
    """
    db, cursor = connect()

    query = """SELECT name, count(*) AS views FROM articles_log
        WHERE status != '404 NOT FOUND'
        GROUP BY name ORDER BY views DESC;"""
    cursor.execute(query)

    print("TOP AUTHORS:")
    return curr.fetchall()
    curr.close()
    db.close()


def buggy_days():
        """
        Buggy Days: Presents all the days where more than 1% of requests led to
        HTTP status errors

        Args:
            none

        Returns:
            A list with the dates, number of requests, number of requests that
            generated errors, and the percentage of requests that led to an
            error. Only dates with more than 1% error rate a included.
        """
    db, cursor = connect()

    query = """SELECT date, requests, errors, percentage
        FROM (SELECT date, requests, errors,
            trunc(100.0*errors / requests, 2) AS percentage
            FROM requests LEFT JOIN errors
            USING (date)) AS subq
        WHERE percentage > 1.00
        ORDER BY percentage DESC;"""

    print("HIGH ERROR DAYS:")
    return curr.fetchall()
    curr.close()
    db.close()


if __name__ == "__main__":
    print(top_articles())
    print(top_authors())
    print(buggy_days())
