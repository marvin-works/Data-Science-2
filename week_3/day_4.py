import pandas as pd
import sqlite3

conn = sqlite3.connect("employees.db")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
        "name": ["Ada", "Bo", "Chi", "Deji", "Efe"],
        "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales"],
        "salary": [75000, 55000, 90000, 60000, 58000],
        "age": [25, 34, 29, 41, 22]

})

query = """
WITH avg_price AS (
    SELECT AVG(price) AS average_price FROM products
)
SELECT * FROM products
WHERE price > (SELECT average_price FROM avg_price);

"""
# WITH dept_averages AS (
#     SELECT department, AVG(salary) AS avg_salary
#     FROM employees
#     GROUP BY department
# )
# SELECT department, avg_salary
# FROM dept_averages
# WHERE avg_salary > 60000;

# SELECT department, avg_salary
# FROM (
#     SELECT department, AVG(salary) AS avg_salary
#     FROM employees
#     GROUP BY department
# ) AS dept_averages
# WHERE avg_salary > 60000
# SELECT name, salary
# FROM employees
# WHERE salary > (SELECT AVG(salary) FROM employees);

employees.to_sql("employees", conn, index=False, if_exists="replace")

result = pd.read_sql_query(query, conn)
print(result)