import psycopg2

conn = psycopg2.connect(database='Hotel_V2', user='postgres', password='20332035')
cur = conn.cursor()


