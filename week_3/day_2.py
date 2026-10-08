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

"""
# SELECT department, AVG(salary) AS avg_salary
# FROM employees
# GROUP BY department
# HAVING AVG(salary) > 65000;
# SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY
# SELECT department, AVG(salary)
# FROM employees
# GROUP BY department;
# SELECT COUNT(*) FROM employees;          
# SELECT SUM(salary) FROM employees;        
# SELECT AVG(salary) FROM employees;         
# SELECT MAX(salary) FROM employees;           
# SELECT MIN(salary) FROM employees;            
# GROUP BY

# SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY

result = pd.read_sql_query(query, conn)

print(result)