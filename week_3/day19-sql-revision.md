# SQL Revision Notes — Day 19: Window Functions, NULL Handling, DB Concepts

## Core Concepts

**Window functions — the key idea.** `GROUP BY` collapses rows into one row per group. A window function calculates something across a group of related rows **without collapsing anything** — every original row stays visible.

```sql
SELECT name, department, salary,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary
FROM employees;
```
`PARTITION BY` = the window-function version of `GROUP BY`. It defines which rows get grouped together *for the calculation*, but every row still shows up individually in the result.

**The single biggest thing to hold onto:**
```
GROUP BY         → collapses rows (one row per group)
PARTITION BY     → groups rows for a calculation WITHOUT collapsing them
ORDER BY in OVER → controls order for ranking / running calculations
```
You want the non-collapsing version whenever you need **both** an individual row's own data **and** a calculation based on its group at the same time (e.g. "show me each employee's salary next to their department's average").

**`RANK()` vs `ROW_NUMBER()` vs `DENSE_RANK()`** — ranking rows within a partition:
```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;
```
- `RANK()` — ties get the *same* rank, and the next rank number is **skipped** (1, 2, 2, 4).
- `DENSE_RANK()` — ties get the same rank, but **no gap** afterward (1, 2, 2, 3).
- `ROW_NUMBER()` — every row gets a **unique**, sequential number even when values tie (1, 2, 3, 4) — the tie-break order isn't guaranteed unless you add a secondary sort key, e.g. `ORDER BY salary DESC, id`.

**Running totals:**
```sql
SELECT id, name, salary,
       SUM(salary) OVER (ORDER BY id) AS running_total
FROM employees;
```
No `PARTITION BY` → whole table treated as one group. `ORDER BY id` inside `OVER(...)` makes the window grow row by row as you move down the table — row 1's window is just itself, row 2's window is rows 1–2, row 3's is rows 1–3, and so on — that's the actual mechanism behind why it accumulates instead of giving one final total.

**NULL handling:**
```sql
COALESCE(column, 'default_value')   -- first non-NULL value, else the fallback
```
```sql
SELECT name, COALESCE(department_name, 'Unassigned') AS department_name
FROM employees LEFT JOIN departments ON ...;
```
**Aggregates automatically ignore `NULL`** — `SUM()`, `AVG()`, `COUNT(column)` all skip `NULL` rows entirely rather than treating them as `0`. `AVG()` divides by the count of *non-null* rows, not all rows. No error occurs. (Mirrors pandas' default `NaN`-skipping behavior in `.mean()`/`.sum()`.)

**Basic database vocabulary:**
- **Primary key** — uniquely identifies each row in a table (e.g. `employees.id`); never `NULL`, never duplicated.
- **Foreign key** — a column referencing another table's primary key (e.g. `employees.department_id` → `departments.department_id`); this is what makes JOINs possible.
- **Schema** — the structure of a database: which tables exist, their columns, and column types.
- **Index** — a lookup structure built on a column to speed up searching/filtering, at the cost of extra storage (conceptually like why set lookups beat list scans — Day 4).

---

## Practice — Dataset, Questions & Verified Answers

```python
employees = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6],
    "name": ["Ada", "Bo", "Chi", "Deji", "Efe", "Fola"],
    "department": ["Engineering", "Sales", "Engineering", "Sales", "Engineering", "Marketing"],
    "salary": [75000, 55000, 90000, 55000, 68000, 60000]
})
```

**Q1 — department average, no collapsing:**
```sql
SELECT name, department, salary,
       ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary
FROM employees;
```
Result: every employee keeps their row; Engineering shows `77666.67` for all three (Ada, Chi, Efe), Sales shows `55000.00` (Bo, Deji), Marketing shows `60000.00` (Fola).

**Q2 — `RANK()` within department:**
```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;
```
Engineering: Chi 90000→1, Ada 75000→2, Efe 68000→3.
Sales: Bo 55000→1, Deji 55000→**1** (tied, no rank 2 exists for Sales at all — `RANK()` skips it).
Marketing: Fola 60000→1.

**Q3 — `ROW_NUMBER()` within department:**
Same as Q2, except Sales gets **Bo→1, Deji→2** — every row gets a unique number even on a tie. (Without a secondary `ORDER BY` key, which of the tied rows gets 1 vs. 2 isn't guaranteed.)

**Q4 — running total ordered by id:**
```sql
SELECT id, name, salary,
       SUM(salary) OVER (ORDER BY id) AS running_total
FROM employees;
```
`75000 → 130000 → 220000 → 275000 → 343000 → 403000` — accumulates row by row down the table.

**Q5 — `NULL` in `AVG()`:** with Chi's salary set to `NULL` (data: 75000, 55000, NULL, 55000, 68000, 60000):
```
SUM(salary) = 313000, COUNT(salary) = 5, AVG(salary) = 62600
```
`NULL` is excluded from both the sum and the count — not treated as 0 — and no error occurs.

---

## Build — Dataset, Task & Verified Solution

```python
sales = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7],
    "rep": ["Ada", "Bo", "Ada", "Chi", "Bo", "Chi", "Ada"],
    "region": ["North", "South", "North", "North", "South", "North", "North"],
    "amount": [1200, 800, 950, 1500, 600, 1100, 1300]
})
```

**1. Region average, no collapsing:**
```sql
SELECT id, rep, region, amount,
       AVG(amount) OVER (PARTITION BY region) AS region_avg
FROM sales
ORDER BY id;
```
North avg = `(1200+950+1500+1100+1300)/5 = 1210`. South avg = `(800+600)/2 = 700`. Every row keeps its own `amount` next to its region's average.

**2. `RANK()` within region:**
```sql
SELECT id, rep, region, amount,
       RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS sale_rank
FROM sales
ORDER BY region, sale_rank, id;
```
North: 1500→1, 1300→2, 1200→3, 1100→4, 950→5 (no ties). South: 800→1, 600→2 (no ties). If two North sales had both been 1300, they'd tie at rank 2 and rank 3 would be skipped, jumping to 4.

**3. Running total, whole table, ordered by id:**
```sql
SELECT id, rep, region, amount,
       SUM(amount) OVER (ORDER BY id) AS running_total
FROM sales
ORDER BY id;
```
`1200 → 2000 → 2950 → 4450 → 5050 → 6150 → 7450` — no `PARTITION BY`, so the whole table is treated as one running window, region ignored.

---

## Recall Check

1. **`GROUP BY` vs `PARTITION BY` — why would you want the non-collapsing version?**
   `GROUP BY` changes the shape of the result (fewer rows, one per group). `PARTITION BY` groups rows for a window calculation but keeps every row. You want the non-collapsing version when you need both the individual row's data *and* a group-level calculation displayed together — e.g. each employee's own salary next to their department's average.

2. **`RANK()` vs `ROW_NUMBER()` — which one guarantees every row a distinct number?**
   `ROW_NUMBER()`. `RANK()` gives tied rows the same number and skips the next one; `ROW_NUMBER()` always assigns a unique sequential number, even on ties (tie order isn't guaranteed without a secondary sort key).

3. **Why does `SUM(x) OVER (ORDER BY id)` produce a running total instead of one final sum?**
   `ORDER BY` inside `OVER(...)` makes the window grow as you move down the rows — each row's window includes only the rows up to and including itself, so the sum accumulates progressively rather than covering the whole table at once.

---

## Personal Note

This lesson's material was consistently strong once actually completed — no logic or math errors anywhere across Practice, Build, or Recall. The real issue was avoidance: a direct question about whether results were genuinely executed got sidestepped, and there was an attempt to skip straight to the next day without finishing Build or Recall. Day 18 proved this can be done cleanly and fully unprompted — the standard to hold isn't just "get the SQL right," it's "finish everything asked, in order, without needing a second push."
