import matplotlib.pyplot as plt

df = {
    "month": "jan"
}
# 1. Learn
plt.plot(df["month"], df["revenue"])
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title("Revenue Over Time")
plt.show()

# Bar chart — comparing categories:
plt.bar(df["region"], df["sales"])

# Histogram — distribution of one numeric column
plt.hist(df["score"], bins=10)

# Scatter plot — relationship between two numeric variables
plt.scatter(df["hours_studied"], df["score"])

# Seaborn versions — same ideas, cleaner syntax, works directly with DataFrames
import seaborn as sns

sns.lineplot(data=df, x="month", y="revenue")
sns.barplot(data=df, x="region", y="sales")
sns.histplot(data=df, x="score", bins=10)
sns.scatterplot(data=df, x="hours_studied", y="score")
sns.boxplot(data=df, x="team", y="score")   # shows median, quartiles, outliers per category




import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [1200, 1350, 1100, 1600, 1750, 1500],
    "region": ["North", "South", "North", "South", "North", "South"]
})

# Chart 1: Line chart
plt.plot(df["month"], df["revenue"])
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title("Revenue Over Time")
plt.show()


# Chart 2: Bar chart — aggregate revenue by region first
region_revenue = df.groupby("region")["revenue"].sum()

plt.bar(region_revenue.index, region_revenue.values)
plt.xlabel("Region")
plt.ylabel("Total Revenue")
plt.title("Total Revenue by Region")
plt.show()


# Chart 3: Histogram
plt.hist(df["revenue"])
plt.xlabel("Revenue")
plt.ylabel("Frequency")
plt.title("Distribution of Revenue")
plt.show()
