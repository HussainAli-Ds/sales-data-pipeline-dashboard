from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from config import DB_URI

engine = create_engine(DB_URI)

def insert_data(df):
    meta = MetaData()
    table = Table("store", meta, autoload_with=engine)

    data = df.to_dict(orient="records")

    stmt = insert(table).values(data)
    stmt = stmt.on_conflict_do_nothing()

    with engine.begin() as conn:
        conn.execute(stmt)