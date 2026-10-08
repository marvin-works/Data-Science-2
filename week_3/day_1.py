import sqlite3
import pandas as pd

conn = sqlite3.connect("employees.db")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe"],
    "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales"],
    "salary": [75000, 55000, 90000, 60000, 58000],
    "age": [25, 34, 29, 41, 22]
})
# df[df["department"] == "Sales"][["name", "age"]].sort_values("age")
employees.to_sql("employees", conn, index=False, if_exists="replace")

query = """
SELECT * FROM employees WHERE department = 'Engineering' OR salary > 70000;
"""
# SELECT * FROM employees WHERE salary > 60000;
# SELECT name, department FROM employees;
# SELECT name, age FROM employees WHERE department = 'Sales' ORDER BY age ASC;

result = pd.read_sql_query(query, conn)

print(result)