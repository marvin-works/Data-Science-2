import pandas as pd


# Filtering with boolean conditions
df = pd.DataFrame({
    "name": ["Ada", "Bo", "Chi", "Deji"],
    "score": [88, 72, 95, 60]
})

print(df["score"] > 75)
# 0     True
# 1    False
# 2     True
# 3    False
# Name: score, dtype: bool

print(df[df["score"] > 75])
#   name  score
# 0  Ada     88
# 2  Chi     95

# Combining conditions
df[(df["score"] > 70) & (df["score"] < 90)]

# .loc and .iloc
# .loc uses labels (index names, column names).
# .iloc uses integer positions, like list indexing.

df.loc[0, "name"]     # "Ada" — label-based
df.iloc[0, 0]           # "Ada" — position-based, same result here since default index is 0,1,2...

# Missing values — represented as NaN

df.isna()               # True/False grid, where data is missing
df.isna().sum()          # count of missing values per column
df.dropna()               # removes rows with ANY missing value
df.fillna(0)                # replaces NaN with a specified value


# Duplicates:
df.duplicated()          # True/False per row — is this row a repeat of an earlier one?
df.drop_duplicates()       # removes repeat rows, keeps first occurrence by default

# Dtypes — every column has one, and mismatched types cause silent bugs (e.g. numbers stored as strings can't be summed correctly):


# df.dtypes                  # dtype per column
df["score"] = df["score"].astype(float)   # convert a column's type