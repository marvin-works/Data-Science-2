import pandas as pd

# Series
s = pd.Series([10, 20, 30])
print(s)
# 0    10
# 1    20
# 2    30
# dtype: int64

s = pd.Series([10, 20, 30], index = ["a", "b", "c"])
print(s["b"])

# DataFrame

data = {
    "region": ["North", "South", "East"],
    "sales": [100, 150, 120]
}
df = pd.DataFrame(data)
print(df)
#   region  sales
# 0  North    100
# 1  South    150
# 2   East    120

# Importing data
df = pd.read_csv("sales.csv")

# Inspecting a DataFrame
df.head()        # first 5 rows — sanity check the data looks right
df.shape          # (rows, columns) — a tuple, like NumPy's .shape
df.info()          # column names, dtypes, non-null counts — catches missing data early
df.columns         # just the column names
df.describe()      # summary stats (mean, std, min, max, etc.) for numeric columns

# selecting a column
print(df["sales"])           # Series
print(df[["region", "sales"]])   # DataFrame (note the double brackets)


students = ["Ada", "Bo", "Chi", "Deji"]
scores = [88, 72, 95, 60]
subjects = ["Math", "Math", "Science", "Science"]

data = pd.DataFrame({
    "Student": students,
    "Score": scores,
    "Subjects": subjects
})
print(data.shape) # tells me the amount of rows and columns available
print(data.info()) # column names, dtypes, non-null counts — catches missing data early
print(data.describe()) # summary stats (mean, std, min, max, etc.) for numeric columns

print(type(data["Score"]))
print(data[["Student", "Score"]]) #Because one bracket selects one column, while two brackets select multiple columns.