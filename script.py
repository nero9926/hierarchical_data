# Получение сотрудников по идентификатору
import argparse

from db_init import connect_to_db


def get_employees_by_id(employee_id, connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        WITH RECURSIVE hierarchy AS (
            SELECT id, ParentId, Name, Type
            FROM organizations
            WHERE id = %s
            UNION ALL
            SELECT o.id, o.ParentId, o.Name, o.Type
            FROM organizations o
            JOIN hierarchy h ON h.id = o.ParentId
        )
        SELECT Name
        FROM hierarchy
        WHERE Type = 1;
        """,
        (employee_id,)
    )
    employees = cursor.fetchall()
    cursor.close()
    return [employee[0] for employee in employees]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Получение сотрудников по идентификатору")
    parser.add_argument("employee_id", type=int,
                        help="Идентификатор сотрудника")
    args = parser.parse_args()

    conn = connect_to_db()
    employees = get_employees_by_id(args.employee_id, conn)
    print("Сотрудники в том же офисе:", ", ".join(employees))
    conn.close()
