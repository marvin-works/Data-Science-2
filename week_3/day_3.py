import pandas as pd
import sqlite3

conn = sqlite3.connect("joins.db")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe"],
    "department_id": [10, 20, 10, 30, 20]
})

departments = pd.DataFrame({
    "department_id": [10, 20, 40],
    "department_name": ["engineering", "sales", "legal"]
})

employees.to_sql("employees", conn, index=False, if_exists="replace")
departments.to_sql("departments", conn, index=False, if_exists="replace")

query = """

SELECT e.name, d.department_name
FROM employees as e
INNER JOIN departments as d
    ON e.department_id = d.department_id

"""
result = pd.read_sql_query(query, conn)

print(result)