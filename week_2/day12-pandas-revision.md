# Pandas Revision Notes — Day 12: GroupBy, Merge/Join, Reshaping, Feature Creation

## Core Concepts

**GroupBy — "split, apply, combine"**
```python
df.groupby("region")["sales"].sum()
```
- **Split** — `groupby("region")` breaks the DataFrame into one group per unique region.
- **Apply** — `.sum()` (or `.mean()`, `.max()`, etc.) runs on each group separately.
- **Combine** — pandas stitches the per-group results back into one Series/DataFrame, indexed by the group key.

**Multiple aggregations at once:**
```python
df.groupby("region")["sales"].agg(["sum", "mean", "count"])
```

**Grouping by more than one column:**
```python
df.groupby(["customer", "product"])["quantity"].sum()
# result is indexed by (customer, product) pairs
```

**Merge/join — combining two DataFrames on a shared key:**
```python
pd.merge(left, right, on="id")                 # inner join (default) — keeps only matching ids
pd.merge(left, right, on="id", how="left")       # keeps ALL of left; unmatched rows get NaN on right's columns
pd.merge(left, right, on="id", how="outer")      # keeps everything from both sides
```
Simple way to remember: **inner → only matches. left → everything from the left + matches from the right.**
Watch dtypes after a left/outer merge: a numeric column that gains `NaN` values (from unmatched rows) often converts from `int` to `float`, since integer columns in pandas can't hold `NaN`.

**Reshaping (pivot):**
```python
df.pivot_table(values="sales", index="region", columns="product", aggfunc="sum")
```
Turns unique values of `columns` into new columns, `index` into rows, filling the grid with the aggregated `values`.

**Feature creation — deriving a new column from existing ones:**
```python
df["total_price"] = df["quantity"] * df["unit_price"]
```
Just assign to a column name that doesn't exist yet — pandas creates it. **This must happen before anything downstream references it** — a `groupby` or filter that uses a column you haven't created yet will raise `KeyError`, because pandas looks the name up in `df.columns` and it simply isn't there yet.

---

## Practice Questions & Answers

**Q1.**
```python
df = pd.DataFrame({"team": ["A","B","A","B","A"], "points": [10,20,15,25,5]})
df.groupby("team")["points"].sum()
```
**Answer:**
```
team
A    30
B    45
```

**Q2.**
```python
df = pd.DataFrame({"team": ["A","B","A","B"], "points": [10,20,15,25]})
df.groupby("team")["points"].agg(["mean", "max"])
```
**Answer:**
```
      mean  max
team
A     12.5   15
B     22.5   25
```

**Q3 — default merge:**
```python
left = pd.DataFrame({"id": [1,2,3], "name": ["X","Y","Z"]})
right = pd.DataFrame({"id": [1,2], "value": [100,200]})
pd.merge(left, right, on="id")
```
**Answer:**
```
   id name  value
0   1    X    100
1   2    Y    200
```
(`id=3` dropped — no match in `right`, inner join.)

**Q4 — same merge with `how="left"`:**
```
   id name  value
0   1    X  100.0
1   2    Y  200.0
2   3    Z    NaN
```
(`id=3` kept, `value` becomes `NaN` — and note the whole `value` column becomes `float` because of the `NaN`.)

**Q5 — feature creation:**
```python
df = pd.DataFrame({"a": [10,20,30], "b": [2,4,5]})
df["c"] = df["a"] / df["b"]
```
**Answer:**
```
    a  b    c
0  10  2  5.0
1  20  4  5.0
2  30  5  6.0
```

---

## Build Exercise & Full Solution

**Task, in the correct order — don't skip steps, later steps depend on earlier ones:**

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer": ["Ada", "Bo", "Ada", "Chi", "Bo", "Ada"],
    "product": ["Pen", "Book", "Book", "Pen", "Pen", "Book"],
    "quantity": [3, 1, 2, 5, 2, 1],
    "unit_price": [2, 15, 15, 2, 2, 15]
})

# Step 1 — create total_price BEFORE anything else uses it
orders["total_price"] = orders["quantity"] * orders["unit_price"]
print(orders)

# Step 2 — total spend per customer, sorted highest to lowest
customer_spend = (
    orders.groupby("customer")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
print(customer_spend)

# Step 3 — total quantity per customer per product (multi-column groupby)
quantity_by_customer_product = (
    orders.groupby(["customer", "product"])["quantity"]
    .sum()
)
print(quantity_by_customer_product)

# Step 4 — merge customer info (city) onto the spend totals
customer_info = pd.DataFrame({
    "customer": ["Ada", "Bo", "Chi"],
    "city": ["Lagos", "Abuja", "Ibadan"]
})
result = pd.merge(customer_spend, customer_info, on="customer")
print(result)
```

**Step 1 output** (`total_price` per row): `6, 15, 30, 10, 4, 15`
(row by row: `3×2, 1×15, 2×15, 5×2, 2×2, 1×15`)

**Step 2 output:**
```
  customer  total_price
0      Ada           51
1       Bo           19
2      Chi           10
```
(Ada: `6+30+15=51`. Bo: `15+4=19`. Chi: `10`.)

**Step 3 output:**
```
customer  product
Ada       Book       3
          Pen        3
Bo        Book       1
          Pen        2
Chi       Pen        5
Name: quantity, dtype: int64
```

**Step 4 output:**
```
  customer  total_price    city
0      Ada           51   Lagos
1       Bo           19   Abuja
2      Chi           10  Ibadan
```

**Why `reset_index()` matters here:** after a `groupby(...).sum()`, the group key (`customer`) becomes the *index*, not a normal column. `reset_index()` turns it back into a regular column, which is required before merging on it with `pd.merge(..., on="customer")` — merge needs `customer` to be an actual column in both DataFrames, not an index.

---

## Recall Check

1. **What does "split, apply, combine" mean?**
   Split: `groupby` breaks the data into groups by key. Apply: an aggregation runs separately on each group. Combine: results are reassembled into one output, indexed by the group key.

2. **Why does `groupby("customer")["total_price"]` raise `KeyError` if `total_price` hasn't been created yet?**
   `["total_price"]` is a column lookup — pandas searches `df.columns` for that exact name. If the column was never assigned, the name isn't there, so pandas raises `KeyError: 'total_price'`. This is why feature-creation steps must run *before* anything downstream references the new column.

3. **Inner merge vs. `how="left"` — which rows survive?**
   Inner: only rows whose key exists in *both* DataFrames. Left: every row from the left DataFrame is kept regardless of a match; unmatched rows get `NaN` in the right-side columns.

---

## Personal Note — Pattern to Watch Tomorrow

The pandas mechanics (groupby, agg, merge, feature creation) have all been solid once fully executed. The recurring miss across Days 8, 11, and 12 hasn't been a knowledge gap — it's been **skipping or reordering steps in a multi-part task**, especially setup steps that later steps silently depend on (e.g. building `total_price` before grouping by it). Before sending a multi-step Build answer, check the finished code against the original numbered task line by line — confirm every step is present, in order, and actually run/traced rather than remembered from a similar example.
