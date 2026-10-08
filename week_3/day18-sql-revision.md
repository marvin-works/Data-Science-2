# SQL Revision Notes — Day 18: Subqueries and CTEs

## Core Concepts

**Why subqueries exist:** some questions can't be answered in one pass — you need the result of one query fed into another. Example: "employees earning more than the average" can't use `WHERE salary > AVG(salary)` directly, because aggregates aren't available at the row-filtering stage (same rule from Day 16 that split `WHERE` from `HAVING`). You need the average calculated *first*, as its own query.

**A subquery** = a query nested inside another, usually in parentheses.
```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
The inner query runs first, collapses to one number, and that number gets used in the outer `WHERE` — like it became a hardcoded value, except computed dynamically.

**Where subqueries can live, each with a different job:**
- **In `WHERE`** — filtering using a computed value (example above).
- **In `FROM`** — treating a query's result as a temporary table:
```sql
SELECT department, avg_salary
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_averages
WHERE avg_salary > 60000;
```
- **In `SELECT`** — pulling a single computed value onto every row:
```sql
SELECT name, salary, (SELECT AVG(salary) FROM employees) AS company_avg
FROM employees;
```

**`IN` with a subquery** — checking membership against a list the subquery produces:
```sql
SELECT name FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE department_name != 'Legal');
```

**CTEs (`WITH ... AS`)** — a named, temporary result defined *before* the main query, referenced like a table. Does the same job as a `FROM`-subquery, but reads top-to-bottom instead of inside-out — that readability is the entire reason CTEs exist. Nothing a CTE does is impossible with a subquery.
```sql
WITH dept_averages AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT department, avg_salary
FROM dept_averages
WHERE avg_salary > 60000;
```
A CTE's computed value can be pulled directly as a scalar, without joining anything:
```sql
WITH avg_price AS (
    SELECT AVG(price) AS average_price FROM products
)
SELECT * FROM products
WHERE price > (SELECT average_price FROM avg_price);
```

**Chaining multiple CTEs**, each building on the last:
```sql
WITH dept_averages AS (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees GROUP BY department_id
),
high_paying_depts AS (
    SELECT department_id FROM dept_averages WHERE avg_salary > 60000
)
SELECT e.name FROM employees e
WHERE e.department_id IN (SELECT department_id FROM high_paying_depts);
```

**The Q4 trap — a `SELECT`-list alias is NOT available inside `WHERE` on the same query:**
```sql
-- FAILS
SELECT name, price, (SELECT AVG(price) FROM products) AS avg_price
FROM products
WHERE price > avg_price;
```
Why: SQL's logical order is roughly `FROM → WHERE → ... → SELECT`. `avg_price` is created *in* the `SELECT` list, which hasn't run yet by the time `WHERE` is evaluated — so the alias doesn't exist yet at that point. Fix: use the full subquery again directly inside `WHERE`, don't reference the alias.

---

## Practice — Dataset, Questions & Verified Answers

```python
products = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6],
    "name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Desk"],
    "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Electronics", "Furniture"],
    "price": [1200, 25, 45, 300, 60, 450],
    "stock": [15, 200, 150, 40, 80, 10]
})
```

**Q1 — products above average price** (average price = 346.67):
```sql
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
```
Result: **Laptop (1200), Desk (450)**.

**Q2 — Electronics products below the Electronics-only average stock** (Electronics avg stock = 97):
```sql
SELECT * FROM products
WHERE category = 'Electronics'
AND stock < (SELECT AVG(stock) FROM products WHERE category = 'Electronics');
```
Result: **Laptop (15), Monitor (40), Webcam (80)**.

**Q3 — Q1 rewritten as a CTE**, idiomatic version:
```sql
WITH avg_price AS (
    SELECT AVG(price) AS average_price FROM products
)
SELECT * FROM products
WHERE price > (SELECT average_price FROM avg_price);
```
Identical result to Q1: **Laptop, Desk**.

**Q4 — why does this fail?**
```sql
SELECT name, price, (SELECT AVG(price) FROM products) AS avg_price
FROM products
WHERE price > avg_price;
```
Fails because `avg_price` is a `SELECT`-list alias, and `WHERE` runs before `SELECT` — the alias isn't available yet. Fix: repeat the subquery directly in `WHERE` instead of referencing the alias.

**Q5 — products in categories where total stock > 300**
(Electronics total = 15+200+150+40+80 = 485; Furniture total = 10 → only Electronics qualifies)
```sql
SELECT name FROM products
WHERE category IN (
    SELECT category FROM products
    GROUP BY category
    HAVING SUM(stock) > 300
);
```
Result: **Laptop, Mouse, Keyboard, Monitor, Webcam** (all Electronics products).

---

## Build — Dataset, Task & Verified Solution

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "customer": ["Ada", "Bo", "Chi", "Ada", "Deji", "Bo", "Efe", "Chi"],
    "category": ["Electronics", "Furniture", "Electronics", "Furniture", "Electronics", "Electronics", "Furniture", "Electronics"],
    "amount": [150, 400, 90, 220, 500, 60, 310, 75]
})
```

**1. Orders above the overall average amount** (average = 1805/8 = 225.625):
```sql
SELECT * FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders);
```
Result:
```
order_id customer     category  amount
2        Bo           Furniture   400
5        Deji         Electronics 500
7        Efe          Furniture   310
```

**2. Customers whose total spend exceeds 300** (CTE + outer filter, not `HAVING` inside the CTE):
```sql
WITH customer_spend AS (
    SELECT customer, SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer
)
SELECT * FROM customer_spend
WHERE total_spend > 300;
```
Per-customer totals: Ada 370, Bo 460, Chi 165, Deji 500, Efe 310.
Result: **Ada (370), Bo (460), Deji (500), Efe (310)** — Chi correctly excluded (165).

**3. Customers who ordered Furniture** (`IN` + subquery + `DISTINCT`):
```sql
SELECT DISTINCT customer FROM orders
WHERE customer IN (
    SELECT customer FROM orders WHERE category = 'Furniture'
);
```
Result: **Ada, Bo, Efe**.
`DISTINCT` matters because a customer can have multiple Furniture orders — without it, that customer would appear once per matching order instead of once total.

---

## Recall Check

1. **Why does `WHERE price > avg_price` fail when `avg_price` is a `SELECT` alias, but work with the full subquery?**
   `WHERE` is evaluated before `SELECT` builds its aliases, so the alias doesn't exist yet at that point. A subquery written directly in `WHERE` is evaluated right there, independent of `SELECT`.

2. **Subquery vs. CTE — real difference?**
   Mainly readability and naming — a CTE is a named, reusable result computed before the main query; almost anything a CTE does, a subquery can also do. CTEs just make multi-step logic easier to read top-to-bottom instead of nested inside-out.

3. **Why did the Furniture-customer query need `DISTINCT`?**
   Without it, a customer with multiple Furniture orders would appear once per matching row, not once overall.

---

## Note

This was the first fully clean Build in the SQL block — every query actually executed, real output pasted, no corrections needed on logic or verification. Worth locking in as the new baseline standard going forward, not a one-off.
