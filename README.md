# The Workflow: Search, Fetch, Process

This project follows a three-step data science pipeline to analyze economic trends.

### 1. Search 🔍

Find the precise **Series ID** using the `wbgapi` search engine to ensure data accuracy.

```python
import wbgapi as wb
# Example: Search for 'unemployment'
wb.series.info(q='unemployment')
```


# IDs: GDP Growth, Inflation, Exports

indicators = ['NY.GDP.MKTP.KD.ZG', 'FP.CPI.TOTL.ZG', 'NE.EXP.GNFS.ZS']
countries = ['SAU', 'EGY']

# Pulling data for the last 5 years

df = wb.data.DataFrame(indicators, countries, mrv=5)


# Remove 'YR' prefix and Flip the table

df.columns = [col.replace('YR', '') for col in df.columns]
df_final = df.T

print(df_final)
