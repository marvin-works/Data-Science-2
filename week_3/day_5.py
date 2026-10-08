import pandas as pd
import sqlite3

conn = sqlite3.connect("WINDOW.db")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
        "name": ["Ada", "Bo", "Chi", "Deji", "Efe"],
        "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales"],
        "salary": [75000, 55000, 90000, 60000, 58000],
        "age": [25, 34, 29, 41, 22]

})
query = """
SELECT name, department, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;
"""
# SELECT name, department, salary,
#   AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary
# FROM employees;


employees.to_sql("employees", conn, index=False, if_exists="replace")
result = pd.read_sql_query(query, conn)
print(result)

import sqlite3
import pandas as pd

conn = sqlite3.connect("assessment.db")

staff = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe", "Fola", "Gina", "Hugo"],
    "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales", "Engineering", "Sales", "Marketing"],
    "salary": [82000, 61000, 95000, 58000, 61000, 70000, 72000, 65000],
    "years_at_company": [3, 1, 5, 2, 4, 2, 1, 6]
})

departments = pd.DataFrame({
    "department": ["Engineering", "Sales", "Marketing", "Legal"],
    "budget": [500000, 300000, 200000, 150000]
})

query = """
SELECT name, department, years_at_company AS years_worked,
    CASE
        WHEN years_at_company >= 4 THEN 'Veteran'
        WHEN years_at_company BETWEEN 2 AND 3 THEN 'Established'
        ELSE 'Newbie'
    END AS staff_tag
FROM staff


"""
# SELECT department, COUNT(*) AS head_count, AVG(salary) AS avg_salary
# FROM staff
# GROUP BY department
# HAVING COUNT(*) > 2

# SELECT name, salary FROM staff
# WHERE salary >= 65000
# ORDER BY salary DESC


staff.to_sql("staff", conn, index=False, if_exists="replace")
departments.to_sql("departments", conn, index=False, if_exists="replace")

result = pd.read_sql_query(query, conn)
print(result)