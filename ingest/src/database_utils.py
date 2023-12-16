from sqlalchemy import inspect, text
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def exist_table(database_url, table_name):
    try:
        return inspect(create_engine(database_url)).has_table(table_name)
    except Exception as ex:
        logger.error(ex)
    return False


def create_pk(database_url, table_name, pk_column="id"):
    try:
        with create_engine(database_url).connect() as conn:
            query = text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column});")
            conn.execute(query)
    except Exception as ex:
        logger.error(ex)


def dataframe_to_db(df, table_name, database_url, chunksize=1000):
    engine = create_engine(database_url)
    conn = engine.connect()
    has_table = exist_table(database_url, table_name)
    with conn.begin() as transaction:
        try:
            df.to_sql(
                name=table_name,
                con=engine,
                index=False,
                if_exists="replace",
                chunksize=chunksize,
                method="multi",
            )
            transaction.commit()
        except Exception as e:
            logger.error(e)
            transaction.rollback()
    if not has_table:
        create_pk(database_url, table_name)
