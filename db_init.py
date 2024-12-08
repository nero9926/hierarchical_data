import json

import psycopg2


# Подключение к базе данных PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5433",
    )


# Импорт данных из JSON в таблицу organizations
def import_data(json_file, connection):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    cursor = connection.cursor()
    for record in data:
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS organizations (
                    id SERIAL PRIMARY KEY,
                    ParentId INT,
                    Name TEXT NOT NULL,
                    Type INT NOT NULL
                );
                INSERT INTO organizations (id, ParentId, Name, Type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET ParentId = excluded.ParentId,
                    Name = excluded.Name,
                    Type = excluded.Type;

                """,
                (record["id"], record["ParentId"],
                 record["Name"], record["Type"]),
            )
        except psycopg2.errors.UniqueViolation as err:
            print(err)
            break
    connection.commit()
    cursor.close()


if __name__ == "__main__":
    conn = connect_to_db()
    import_data("data.json", conn)
    conn.close()
