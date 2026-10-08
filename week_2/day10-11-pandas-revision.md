# Pandas Revision Notes — Day 10 & Day 11

---

# DAY 10 — Series & DataFrames: Creation, Importing, Inspecting

## Core Concepts

**Series** — a single labeled column of data (like a NumPy array with an index attached).
```python
import pandas as pd

s = pd.Series([10, 20, 30])
# 0    10
# 1    20
# 2    30

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["b"])   # 20
```

**DataFrame** — a 2D table. Built from **one structure that already ties rows and columns together** — most commonly a **dictionary of lists**, where each key becomes a column name and every list must be the **same length**.

```python
data = {
    "region": ["North", "South", "East"],
    "sales": [100, 150, 120]
}
df = pd.DataFrame(data)
```

❌ **Wrong** (the classic mistake): `pd.DataFrame(region, sales)` — passing two loose variables. Pandas treats the first as data and the second as something like an index, not as a second column.

✅ **Right**: `pd.DataFrame({"region": region, "sales": sales})`

**Importing data:**
```python
df = pd.read_csv("sales.csv")
```

**Inspecting a DataFrame (do this first, every time):**
```python
df.head()      # first 5 rows — sanity check
df.shape        # (rows, columns) tuple
df.info()        # column names, dtypes, non-null counts — catches missing data
df.columns       # column names
df.describe()    # summary stats (mean, std, min, max) for numeric columns
```

**Selecting columns:**
```python
df["sales"]              # ONE string -> Series
df[["region", "sales"]]  # LIST of names -> DataFrame (even a list of ONE column still returns a DataFrame)
```
The outer `[]` is pandas' indexing operator; the inner `[...]` (when present) is a plain Python list being handed to it. A list argument means "give me a table back," a bare string means "give me a column back."

---

## Day 10 — Practice Questions & Answers

**Q1.**
```python
s = pd.Series([5, 10, 15], index=["x", "y", "z"])
print(s["y"])
```
**Answer:** `10`

**Q2 (broken — fix it):**
```python
names = ["Ada", "Bo", "Chi"]
ages = [25, 30, 22]
df = pd.DataFrame(names, ages)   # WRONG
```
**Fix:**
```python
df = pd.DataFrame({"name": names, "age": ages})
```

**Q3.**
```python
data = {"product": ["pen", "book", "bag"], "price": [2, 15, 40]}
df = pd.DataFrame(data)
print(df.shape)             # (3, 2)
print(df["price"])          # Series: 2, 15, 40 (dtype: int64)
print(type(df["price"]))    # <class 'pandas.core.series.Series'>
```

**Q4.** What's wrong here?
```python
data = {"a": [1, 2, 3], "b": [4, 5]}
df = pd.DataFrame(data)
```
**Answer:** `ValueError` — all arrays/lists in the dict must be the same length (`a` has 3 values, `b` has 2).

---

## Day 10 — Build Exercise & Solution

**Task:** From `students`, `scores`, `subjects` lists — build a DataFrame with columns `student`, `score`, `subject`; inspect it with `.shape`/`.info()`/`.describe()`; select `score` alone (confirm it's a Series); select `student` + `score` together (confirm it's a DataFrame).

```python
students = ["Ada", "Bo", "Chi", "Deji"]
scores = [88, 72, 95, 60]
subjects = ["Math", "Math", "Science", "Science"]

df = pd.DataFrame({
    "student": students,
    "score": scores,
    "subject": subjects
})

print(df.shape)     # (4, 3)
print(df.info())    # student & subject: object dtype, score: int64, no nulls
print(df.describe())  # score: mean 78.75, min 60, max 95

print(type(df["score"]))          # Series
print(df[["student", "score"]])   # DataFrame
```

**Why double brackets for the last line:** `df["score"]` — one string, pandas returns a Series (one column). `df[["student", "score"]]` — the inner `["student", "score"]` is a Python list, and pandas' indexing operator (outer `[]`) sees a list and returns a DataFrame, even if the list only has one name in it.

---

## Day 10 — Recall Check

1. **Why is `pd.DataFrame(region, sales)` wrong, and what should you pass instead?**
   Pandas treats the first positional arg as data and the second as something like an index — not a second column. Pass a dict of lists: `pd.DataFrame({"region": region, "sales": sales})`.

2. **`df["col"]` vs `df[["col"]]` — what's the real difference?**
   `df["col"]` → Series. `df[["col"]]` → DataFrame, because it's a list being passed in, and a list argument always returns a DataFrame — even with just one column name inside it.

3. **Three things `.info()` tells you that `.describe()` doesn't:**
   Row/entry count, dtype per column, non-null count per column (catches missing data). `.describe()` only covers numeric summary stats (mean, std, min, max, quartiles).

---

# DAY 11 — Selecting/Filtering, Missing Values, Duplicates, Dtypes

## Core Concepts

**Boolean indexing (filtering):**
```python
df["score"] > 75        # Series of True/False, one per row
df[df["score"] > 75]     # filters to only the True rows
```

**Combining conditions — never use `and`/`or`. Use `&` / `|`, and parenthesize each condition:**
```python
df[(df["score"] > 70) & (df["score"] < 90)]
```
`and`/`or` expect one True/False value; a pandas comparison produces a whole Series of them — using `and` raises `ValueError: The truth value of a Series is ambiguous`. Parentheses are required because `&` binds tighter than `>` in plain Python, so `df["age"] > 18 & df["age"] < 30` would evaluate in the wrong order without them.

**`.loc` vs `.iloc`:**
- `.loc` — selects by **label** (index name, column name).
- `.iloc` — selects by **integer position**, like list indexing.
```python
df.loc[0, "name"]   # label-based
df.iloc[0, 0]         # position-based
```

**Missing values (`NaN`):**
```python
df.isna()             # True/False grid
df.isna().sum()         # missing-value count per column
df.dropna()              # drop rows with ANY missing value
df.fillna(0)               # replace NaN with a value
```
**Comparing `NaN` with `>=`, `>`, `<` etc. does NOT raise an error — it silently returns `False`.** This means a row with a missing value in a filtered column gets silently dropped from the result, not flagged.

**Duplicates:**
```python
df.duplicated()         # True/False per row — is this a repeat of an earlier row?
df.drop_duplicates()      # removes repeats, keeps first occurrence, ORIGINAL INDEX VALUES ARE KEPT (not reset)
```

**Dtypes:**
```python
df.dtypes
df["score"] = df["score"].astype(float)   # or pd.to_numeric(df["score"])
```
Numbers stored as strings won't sum correctly — `"10" + "20" + "30"` concatenates into `"102030"` instead of adding to `60`.

---

## Day 11 — Practice Questions & Answers

**Q1.**
```python
df = pd.DataFrame({"name": ["Ada", "Bo", "Chi"], "age": [25, 17, 30]})
print(df[df["age"] >= 18])
```
**Answer:**
```
   name  age
0   Ada   25
2   Chi   30
```

**Q2 (raises an error — why?):**
```python
df[(df["age"] > 18 and df["age"] < 30)]
```
**Answer:** `ValueError: The truth value of a Series is ambiguous`. `and` expects a single True/False; each comparison here produces a whole Series. Fix:
```python
df[(df["age"] > 18) & (df["age"] < 30)]
```

**Q3.**
```python
df = pd.DataFrame({
    "name": ["Ada", "Bo", "Chi", None],
    "score": [88, None, 95, 60]
})
print(df.isna().sum())
```
**Answer:**
```
name     1
score    1
dtype: int64
```

**Q4.**
```python
df = pd.DataFrame({"x": [1, 2, 2, 3], "y": ["a", "b", "b", "c"]})
print(df.duplicated())
```
**Answer:**
```
0    False
1    False
2     True
3    False
```
(Row 2 is a repeat of row 1.)
```python
print(df.drop_duplicates())
```
**Answer:**
```
   x  y
0  1  a
1  2  b
3  3  c
```
(Note: row 3 keeps its **original index label** `3` — the index is not reset after dropping.)

**Q5.**
```python
df = pd.DataFrame({"price": ["10", "20", "30"]})
print(df["price"].sum())
```
**Answer:** `"102030"` — string concatenation, because `price` is stored as text, not numbers. Fix: `df["price"] = df["price"].astype(int)` → `.sum()` gives `60`.

---

## Day 11 — Build Exercise & Solution

**Task:** Messy dataset with duplicate rows, a missing name, a missing age, and scores stored as strings.

```python
data = {
    "name": ["Ada", "Bo", "Chi", "Deji", "Ada", None],
    "age": [25, 17, 30, None, 25, 40],
    "score": ["88", "72", "95", "60", "88", "77"]
}
df = pd.DataFrame(data)

df["score"] = pd.to_numeric(df["score"])
df = df[(df["age"] >= 18) & (df["score"] > 70)]
df = df.drop_duplicates()

print(df)
print(df.isna().sum())
```

**Correct output:**
```
   name   age  score
0   Ada  25.0     88
2   Chi  30.0     95
5  None  40.0     77

name     1
age      0
score    0
dtype: int64
```

**Trace, row by row, through the filter step:**
- Row 0 (Ada, 25, 88) → passes both conditions → kept
- Row 1 (Bo, 17, 72) → age fails (`17 >= 18` is False) → dropped
- Row 2 (Chi, 30, 95) → passes → kept
- Row 3 (Deji, `NaN`, 60) → `NaN >= 18` silently returns `False` → dropped (no error)
- Row 4 (Ada, 25, 88) → passes, but identical to row 0 → dropped later by `drop_duplicates()`
- Row 5 (`None` name, 40, 77) → passes both conditions, no duplicate (its `name` is unique) → kept

Result: 3 rows survive. The missing-`age` row (Deji) is removed by the filter itself, silently, not by an error. The missing-`name` row (row 5) survives because a missing *name* was never part of the filter condition — it only affects the `isna()` count at the end.

---

## Day 11 — Recall Check

1. **Why does `df[(cond1) & (cond2)]` need parentheses, and why does `and` fail?**
   `&` is element-wise and has different (tighter) operator precedence than `>`/`<` in plain Python, so each condition must be parenthesized to force correct evaluation order. `and` fails because it needs one Boolean, not a Series of them.

2. **What happens when you compare `NaN` with `>=`, `>`, `<`?**
   No error — it returns `False`. This means rows with missing values silently disappear from filtered results rather than causing a crash or a flag.

3. **`.loc` vs `.iloc`?**
   `.loc` selects by label (row/column *name*). `.iloc` selects by integer position (like a list index), regardless of what the labels actually are.

---

## Personal Weak Spots Flagged Across These Two Days

- **Verification discipline, not knowledge.** Twice now (once on the NumPy Build, once on this Day 11 Build), output was sent that didn't match what the actual code would produce — because it was written from memory/expectation rather than traced or run. The reasoning was always correct once pushed to actually trace it — the gap is in checking your own work before sending it, not in understanding the material.
- **"Explain in your own words" tasks** are more likely to trigger copying the tutor's own phrasing back verbatim than "write code" tasks are. Watch for this specifically when a question asks you to describe or explain a concept rather than solve a problem.
