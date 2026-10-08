import pandas as pd
import sqlite3

conn = sqlite3.connect("joins.db")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe", "Fola"],
    "department": ["Engineering", "Sales", "Engineering", "Sales", "Engineering", "Marketing"],
    "salary": [75000, 55000, 90000, 55000, 68000, 60000]
})



employees.to_sql("employees", conn, index=False, if_exists="replace")
query = """

"""
# SELECT id, name, salary, 
#     (SELECT SUM(salary) OVER (ORDER BY id)) AS total_salary
# FROM employees

# SELECT name, department, salary,
#   ROW_NUMBER () OVER (PARTITION BY department ORDER BY salary desc) AS salary_row_num
# FROM employees

# SELECT name, department, salary,
#   RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
# FROM employees;


# SELECT name, department, salary,
#     AVG(salary) OVER (PARTITION BY department) AS avg_salary
# FROM employees;
result = pd.read_sql_query(query, conn)

print(result)