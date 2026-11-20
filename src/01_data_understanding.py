import pandas as pd
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FLIGHTS_FILE = DATA_DIR / "flights.csv"
AIRLINES_FILE = DATA_DIR / "airlines.csv"
AIRPORTS_FILE = DATA_DIR / "airports.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

flights = pd.read_csv(FLIGHTS_FILE)
airlines = pd.read_csv(AIRLINES_FILE)
airports = pd.read_csv(AIRPORTS_FILE)

print("\nFiles loaded successfully.")


# =========================================================
# BASIC INFORMATION
# =========================================================

datasets = {
    "Flights": flights,
    "Airlines": airlines,
    "Airports": airports
}

for name, df in datasets.items():

    print("\n" + "=" * 70)
    print(f"{name.upper()} DATASET")
    print("=" * 70)

    print(f"\nShape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())


# =========================================================
# MISSING VALUES
# =========================================================

for name, df in datasets.items():

    print("\n" + "=" * 70)
    print(f"{name.upper()} - MISSING VALUES")
    print("=" * 70)

    missing = df.isnull().sum()

    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values found.")

    else:
        missing_percentage = (missing / len(df) * 100).round(2)

        missing_table = pd.DataFrame({
            "Missing Values": missing,
            "Percentage": missing_percentage
        })

        print(missing_table)


# =========================================================
# DUPLICATES
# =========================================================

for name, df in datasets.items():

    print("\n" + "=" * 70)
    print(f"{name.upper()} - DUPLICATES")
    print("=" * 70)

    duplicates = df.duplicated().sum()

    print(f"Duplicate rows: {duplicates}")


# =========================================================
# DESCRIPTIVE STATISTICS
# =========================================================

print("\n" + "=" * 70)
print("FLIGHTS - DESCRIPTIVE STATISTICS")
print("=" * 70)

print(flights.describe(include="all").transpose())


# =========================================================
# UNIQUE VALUES
# =========================================================

print("\n" + "=" * 70)
print("IMPORTANT UNIQUE VALUES")
print("=" * 70)

if "AIRLINE" in flights.columns:
    print(f"\nNumber of Airlines: {flights['AIRLINE'].nunique()}")
    print("Airline Codes:")
    print(flights["AIRLINE"].unique())

if "ORIGIN_AIRPORT" in flights.columns:
    print(f"\nNumber of Origin Airports: {flights['ORIGIN_AIRPORT'].nunique()}")

if "DESTINATION_AIRPORT" in flights.columns:
    print(f"Number of Destination Airports: {flights['DESTINATION_AIRPORT'].nunique()}")

if "MONTH" in flights.columns:
    print(f"\nNumber of Months: {flights['MONTH'].nunique()}")
    print("Months:")
    print(sorted(flights["MONTH"].dropna().unique()))


# =========================================================
# TARGET / OUTCOME COLUMNS
# =========================================================

print("\n" + "=" * 70)
print("FLIGHT OUTCOME INFORMATION")
print("=" * 70)

if "CANCELLED" in flights.columns:
    print("\nCancelled flights:")
    print(flights["CANCELLED"].value_counts(dropna=False))

if "DIVERTED" in flights.columns:
    print("\nDiverted flights:")
    print(flights["DIVERTED"].value_counts(dropna=False))


# =========================================================
# DELAY COLUMNS
# =========================================================

delay_columns = [
    "DEPARTURE_DELAY",
    "ARRIVAL_DELAY",
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

available_delay_columns = [
    col for col in delay_columns if col in flights.columns
]

print("\n" + "=" * 70)
print("DELAY COLUMNS")
print("=" * 70)

print(available_delay_columns)


# =========================================================
# AIRLINES DATASET
# =========================================================

print("\n" + "=" * 70)
print("AIRLINES LOOKUP TABLE")
print("=" * 70)

print(airlines)


# =========================================================
# AIRPORTS DATASET
# =========================================================

print("\n" + "=" * 70)
print("AIRPORTS LOOKUP TABLE")
print("=" * 70)

print(airports.head())

print(f"\nNumber of airports: {len(airports)}")


# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

for name, df in datasets.items():
    print(f"{name}: {df.shape[0]:,} rows × {df.shape[1]} columns")

print("\nData understanding completed.")