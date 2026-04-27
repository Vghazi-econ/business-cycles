# World Bank API - Metadata:
import wbgapi as wb

# Get metadata for a series:
wb.series.metadata.get("NY.GDP.MKTP.KD.ZG")
# Get metadata for a series in a DataFrame:
print(wb.series.metadata.get("NY.GDP.MKTP.KD.ZG"))
