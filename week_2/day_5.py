import pandas as pd

# GroupBy — split, apply, combine

df = pd.DataFrame({
    "region": ["North", "south", "North", "south", "East"],
    "product": ["Phone", "Laptop", "Phone", "Laptop", "Tablet"],
    "sales": [100, 150, 200, 120, 90]
})

print(df.groupby("region")["sales"].sum())

print(df.groupby("region")["sales"].agg(["sum", "mean", "count"]))

print(df.groupby(["region", "product"])["sales"].sum())


# Merge/join

customers = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Ada", "Bo", "Chi"]
})

orders = pd.DataFrame({
    "id": [1, 1, 2],
    "amount": [50, 30, 20]
})

merged = pd.merge(customers, orders, on="id")

#     id name  amount
# 0    1  Ada      50
# 1    1  Ada      30
# 2    2  Bo       20


# Reshaping — pivot:

print(df.pivot_table(values="sales", index="region", aggfunc="sum"))


# Feature creation — deriving a new column from existing ones:

# df["price_per_unit"] = df["total_price"] / df["quantity"]

df["is_high_value"] = df["sales"] > 100


# Q1
df = pd.DataFrame({
    "team": ["A", "B", "A", "B", "A"],
    "points": [10, 20, 15, 25, 5]
})
print(df.groupby("team")["points"].sum())

# Q2
df = pd.DataFrame({
    "team": ["A", "B", "A", "B"],
    "points": [10, 20, 15, 25]
})
print(df.groupby("team")["points"].agg(["mean", "max"]))

# Q3
left = pd.DataFrame({"id": [1, 2, 3], "name": ["X", "Y", "Z"]})
right = pd.DataFrame({"id": [1, 2], "value": [100, 200]})
print(pd.merge(left, right, on="id"))

# Q4 — same merge, but with how="left". What changes?
print(pd.merge(left, right, on="id", how="left"))

# Q5
df = pd.DataFrame({"a": [10, 20, 30], "b": [2, 4, 5]})
df["c"] = df["a"] / df["b"]
print(df)


orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer": ["Ada", "Bo", "Ada", "Chi", "Bo", "Ada"],
    "product": ["Pen", "Book", "Book", "Pen", "Pen", "Book"],
    "quantity": [3, 1, 2, 5, 2, 1],
    "unit_price": [2, 15, 15, 2, 2, 15]
})

orders["total_price"] = orders["quantity"] * orders["unit_price"]
print(orders["total_price"])

print(
    orders.groupby("customer")["total_price"]
    .sum()
    .sort_values(ascending=False)
)