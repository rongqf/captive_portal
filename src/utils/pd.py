
import pandas as pd
from utils.common import engine

from sqlalchemy.dialects.postgresql import insert
def gen_upsert(elements):
    def postgres_upsert(table, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        insert_statement = insert(table.table).values(data)
        if elements:
            upsert_statement = insert_statement.on_conflict_do_update(
                index_elements = elements,
                set_={c.key: c for c in insert_statement.excluded},
            )
            conn.execute(upsert_statement)
        else:
            conn.execute(insert_statement)
    return postgres_upsert
def df_to_sql(df, tablename, elements=None, index=False):
    df.to_sql(
        tablename,
        engine, 
        if_exists='append', 
        index=index, 
        method=gen_upsert(elements)
    )

def df_upsert(df1: pd.DataFrame, df2: pd.DataFrame, on=None, copy=False):
    if on:
        x1 = df1.set_index(on)
        x2 = df2.set_index(on)
    else:
        x1 = df1
        x2 = df2
    y1, y2 = x1.align(x2, join='outer',  copy=copy)
    y1.update(x2, overwrite=True)
    if on:
        return y1.reset_index()
    else:
        return y1