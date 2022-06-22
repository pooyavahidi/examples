import sqlite3
import datetime

conn = sqlite3.connect("example.db")


def add_row():
    c = conn.cursor()
    # Create table
    c.execute(
        """CREATE TABLE IF NOT EXISTS Product
                (LastUpdatedDate text,
                CreatedDate text,
                Name text,
                Status text
                )"""
    )

    # Insert a' row of data
    c.execute(
        "INSERT INTO Product VALUES (?,?,?,?)",
        (
            datetime.datetime.now(),
            datetime.datetime.now(),
            "iPhone",
            "InStock",
        ),
    )

    # Save (commit) the changes
    conn.commit()


def read_rows():
    c = conn.cursor()
    res = c.execute("SELECT * FROM Product")
    for row in res:
        print(row)


if __name__ == "__main__":
    add_row()
    read_rows()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
