import pandas as pd
import numpy as np

# Load your CSV (replace with your path)
df = pd.read_csv("data.csv")

weeks = [str(w) for w in range(1, 19)]  # weeks 1 to 18

# Replace non-numeric markers with NaN and convert to float
for w in weeks:
    df[w] = df[w].replace(['-', 'BYE'], np.nan).astype(float)

# Calculate rolling mean (window=3) across weeks (columns)
rolling_means = df[weeks].T.rolling(window=3, min_periods=1).mean().T

# Calculate average fantasy points per player (ignoring NaNs)
df['AvgPoints'] = df[weeks].mean(axis=1)

# Calculate standard deviation of rolling means as consistency metric
df['SMA_std'] = rolling_means.std(axis=1)

# Consistency score: higher avg points and lower std dev = better
df['ConsistencyScore'] = df['AvgPoints'] / (df['SMA_std'] + 1e-5)  # avoid div by zero

# Rank by consistency score descending; fill NaN ranks with large number then convert to int
df['ConsistencyRank'] = df['ConsistencyScore'].rank(ascending=False, method='min')
df['ConsistencyRank'] = df['ConsistencyRank'].fillna(9999).astype(int)

# Sort dataframe by consistency rank
df_sorted = df.sort_values('ConsistencyRank')

# Print selected columns for top 20 players
print(df_sorted[['Player', 'AvgPoints', 'SMA_std', 'ConsistencyScore', 'ConsistencyRank']].head(40))


