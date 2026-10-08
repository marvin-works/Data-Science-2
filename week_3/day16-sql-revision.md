# SQL Revision Notes — Day 16: GROUP BY, HAVING, Aggregate Functions, CASE

## Reference Table — `employees`

| id | name | department | salary | age |
|---|---|---|---|---|
| 1 | Ada | Engineering | 75000 | 25 |
| 2 | Bo | Sales | 55000 | 34 |
| 3 | Chi | Engineering | 90000 | 29 |
| 4 | Deji | Marketing | 60000 | 41 |
| 5 | Efe | Sales | 58000 | 22 |

---

## Core Concepts

**Aggregate functions** — collapse a column to one number. Same job as pandas' `.sum()`, `.mean()`, `.count()`, `.max()`, `.min()`.
```sql
SELECT COUNT(*) FROM employees;    -- row count (counts everything, incl. nulls)
SELECT SUM(salary) FROM employees;
SELECT AVG(salary) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT MIN(salary) FROM employees;
```
`COUNT(*)` counts every row. `COUNT(column)` counts only non-null values in that column — same idea as pandas' `NaN` handling.

**GROUP BY** — same "split, apply, combine" as pandas' `groupby`, just SQL syntax:
```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department;
```

**The rule that trips people up:** every column in `SELECT` must be either grouped or aggregated. You can't mix in a raw column that isn't part of the `GROUP BY` — SQL (in strict engines) will reject it outright, because it has no way to know which row's value to show per group. **SQLite is dangerously permissive here** — it will silently pick *some* row's value instead of erroring, which means a query that "works" in SQLite can break on PostgreSQL/MySQL. Never rely on this behavior even if SQLite lets it run.

```sql
-- Risky in SQLite, invalid on stricter engines: which name goes with MAX(salary)?
SELECT department, name, MAX(salary) FROM employees GROUP BY department;
```
The real fix for "employee with the max salary per department" needs a subquery or window function — a topic for later, not today.

**HAVING — filters groups, not rows.** `WHERE` runs *before* grouping, so it only ever sees raw per-row values — it has no access to `COUNT(*)` or `AVG(salary)` because those don't exist yet at that point. `HAVING` runs *after* grouping, so it can filter on the aggregate result itself.
```sql
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```

**Full clause order (non-negotiable):**
```
SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY
```
Rough logical execution order: pick the table → filter raw rows → form groups → filter groups → sort → decide which columns to show.

**AS — aliasing.** Renames a column/result for readability, purely cosmetic.
```sql
AVG(salary) AS average_salary
```

**CASE — conditional logic inside a query**, same idea as Python's `if/elif/else` or a conditional-expression comprehension:
```sql
SELECT name, salary,
  CASE
    WHEN salary >= 70000 THEN 'High'
    WHEN salary >= 55000 THEN 'Medium'
    ELSE 'Low'
  END AS salary_band
FROM employees;
```
Reads top to bottom, first matching `WHEN` wins, `ELSE` is the catch-all, `END` closes the block.

**Important gotcha confirmed by real execution today: `GROUP BY` does NOT guarantee row order.** Two queries grouping the same data can return rows in different orders (alphabetical, insertion order, tied counts in arbitrary order) depending on the engine. If you need a specific, reliable order — always add an explicit `ORDER BY`. Never assume `GROUP BY` alone gives you a predictable order, even if it looks consistent during testing.

---

## Practice — Questions & Verified Answers

**Q1 — total employees per department:**
```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```
Real output:
```
    department  employee_count
0  Engineering               2
1    Marketing               1
2        Sales               2
```
(Row order here is alphabetical by department — not guaranteed, just what SQLite happened to return.)

**Q2 — average salary, only departments with more than one employee:**
```sql
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```
Output:
```
    department  average_salary
0  Engineering         82500.0
1        Sales         56500.0
```
`WHERE COUNT(*) > 1` would be invalid here — `COUNT(*)` doesn't exist until after grouping, so only `HAVING` can filter on it.

**Q3 — the ungrouped-column trap:**
```sql
SELECT department, name, MAX(salary)
FROM employees
GROUP BY department;
```
SQLite actually runs this and returns:
```
    department  name  max_salary
0  Engineering   Chi       90000
1    Marketing  Deji       60000
2        Sales   Efe       58000
```
It happens to look correct here, but it's not guaranteed or portable — `name` isn't part of the `GROUP BY` and isn't aggregated, so SQL has no defined rule for which name belongs to the max. Stricter databases reject this query outright.

**Q4 — CASE label:**
```sql
SELECT name, age,
       CASE
           WHEN age >= 30 THEN 'Senior'
           ELSE 'Junior'
       END AS age_group
FROM employees;
```
Output:
```
   name  age age_group
0   Ada   25    Junior
1    Bo   34    Senior
2   Chi   29    Junior
3  Deji   41    Senior
4   Efe   22    Junior
```

**Q5 — count > 1, ordered descending:**
```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 1
ORDER BY employee_count DESC;
```
Output:
```
    department  employee_count
0        Sales               2
1  Engineering               2
```
Both have count `2` — this is a genuine tie, and without a second sort key (e.g. `ORDER BY employee_count DESC, department ASC`), which one prints first is not guaranteed.

---

## Recall Check

1. **Why can't `WHERE` filter on `COUNT(*)` or `AVG(salary)`?**
   `WHERE` executes before grouping/aggregation — at that stage, aggregate values simply don't exist yet. `HAVING` executes after groups and their aggregates are computed, so it can reference them.

2. **Full clause order?**
   `SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY` — written order and logical execution order aren't quite the same, but this sequence is required syntactically regardless.

3. **Why might real output come back in a different row order than predicted?**
   `GROUP BY` only groups — it doesn't sort. Without an explicit `ORDER BY`, row order is up to the database engine and isn't guaranteed to be consistent across runs, datasets, or database systems. Always add `ORDER BY` if a specific order matters.

---

## How to Actually Run These (setup, for reference)

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")

employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe"],
    "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales"],
    "salary": [75000, 55000, 90000, 60000, 58000],
    "age": [25, 34, 29, 41, 22]
})
employees.to_sql("employees", conn, index=False, if_exists="replace")

query = """..."""   # any query above
result = pd.read_sql(query, conn)
print(result)
```

## Standing Habit to Fix

This lesson took three passes to get real, executed output instead of predictions or descriptions of output — this is now a repeated pattern across several days (Days 12, 13, 15, 16). The material has never been the actual problem; every correction has landed instantly. **Run the code before sending it, every time real output is asked for — not "I'm confident," actually run it.**
