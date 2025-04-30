import sqlite3


def loading_maps():
    con = sqlite3.connect("data\\database.db")
    cur = con.cursor()
    column_names = [i[1] for i in cur.execute('PRAGMA table_info("levels")').fetchall()]
    result = cur.execute("""SELECT * FROM levels
                    """).fetchall()
    con.close()
    result = [dict(zip(column_names, res)) for res in result]  # преобразуем данные из базы в словари
    return result


def save_results(id):
    con = sqlite3.connect("data\\database.db")
    cur = con.cursor()
    cur.execute("""UPDATE levels
                SET status = 1
                WHERE id = ?
                """, (id,))

    con.commit()
    con.close()