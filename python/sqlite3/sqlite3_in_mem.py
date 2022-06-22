import sqlite3
import datetime

conn = sqlite3.connect(":memory:")


def create_objects():
    c = conn.cursor()
    c.execute(
        """
        create table product
        (name text, update_date textw)
        """
    )
    conn.commit()


def insert_product(name):
    c = conn.cursor()
    param = (name, datetime.datetime.now())
    c.execute("insert into product values (?,?)", param)
    conn.commit()


def list_products():
    c = conn.cursor()
    c.execute("select rowid, * from product")
    products = c.fetchall()
    print(products)


if __name__ == "__main__":
    create_objects()
    insert_product("monitor")
    list_products()
