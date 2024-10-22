import pandas as pd
import json

# The JSON data structure
with open("merged_results.json", "r") as json_file:
    data = json.load(json_file)

# Flatten the data and create a list of records
records = []
for symbol, strategies in data.items():
    for strategy, details in strategies.items():
        records.append(
            {
                "symbol": symbol,
                "strategy": strategy,
                "earnings": details["earnings"],
                "sqn": details["sqn"],
            }
        )

# Convert the list of records to a DataFrame
df = pd.DataFrame(records)

# Find the row with the maximum earnings
best_strategy = df.loc[df["earnings"].idxmax()]

# Print the result
print(
    f"The best strategy is {best_strategy['strategy']} from {best_strategy['symbol']} with earnings of {best_strategy['earnings']}"
)

df_sorted_earnings = (
    df.groupby(["strategy"], as_index=False)
    .sum()
    .sort_values(by="earnings", ascending=False)
)
df_sorted_sqn = (
    df.groupby(["strategy"], as_index=False)
    .sum()
    .sort_values(by="sqn", ascending=False)
)
print(df_sorted_earnings)
print(df_sorted_sqn)
df_grouped = (
    df.groupby("strategy", as_index=False)["earnings"]
    .median()
    .sort_values(by="earnings", ascending=False)
)

print(df_grouped)
