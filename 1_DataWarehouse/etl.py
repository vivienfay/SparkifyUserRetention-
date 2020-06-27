import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    load the staging tables from S3
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    insert the tables from staging tables to dimension data model
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """running"""
    """
    read the configuration document and connect to the S3 and redshift
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    """
    load staging table
    """
    load_staging_tables(cur, conn)
    """
    insert data from staging tables
    """
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()