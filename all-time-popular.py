import psycopg2

# Check Python code quality using pep8 command line tool
# Refer to PEP8 style guide at https://www.python.org/dev/peps/pep-0008/
# Document SQL views in the README

# Top 3 most popular articles
# Presents the top 3 articles as a sorted list with the most popular article at top
# Popularity defined by number of page views over all time

# Most popular article authors
# Presents the authors in a sorted list with the most popular authors at top
# Popularity defined by sum of author's articles page views over all time

# Buggy Days
# Presents all the days where more than 1% of requests led to HTTP status errors
