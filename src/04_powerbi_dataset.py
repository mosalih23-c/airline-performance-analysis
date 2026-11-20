import pandas as pd
import os


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

FLIGHTS_FILE = os.path.join(DATA_DIR, "flights.csv")
AIRLINES_FILE = os.path.join(DATA_DIR, "airlines.csv")
AIRPORTS_FILE = os.path.join(DATA_DIR, "airports.csv")

os.makedirs(RESULTS_DIR, exist_ok=True)


# =========================================================
# COLUMNS NEEDED FOR POWER BI
# =========================================================

flight_columns = [
    "YEAR",
    "MONTH",
    "DAY",
    "DAY_OF_WEEK",
    "AIRLINE",
    "FLIGHT_NUMBER",
    "ORIGIN_AIRPORT",
    "DESTINATION_AIRPORT",
    "DEPARTURE_DELAY",
    "ARRIVAL_DELAY",
    "CANCELLED",
    "DIVERTED",
    "SCHEDULED_DEPARTURE",
    "DISTANCE",
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]


# =========================================================
# 1. LOAD ONLY REQUIRED FLIGHT COLUMNS
# =========================================================

print("=" * 70)
print("LOADING FLIGHT DATA FOR POWER BI")
print("=" * 70)

flights = pd.read_csv(
    FLIGHTS_FILE,
    usecols=flight_columns,
    low_memory=False
)

print(f"Loaded flights: {flights.shape}")


# =========================================================
# 2. LOAD LOOKUP TABLES
# =========================================================

airlines = pd.read_csv(AIRLINES_FILE)

airports = pd.read_csv(AIRPORTS_FILE)

print(f"Airlines: {airlines.shape}")
print(f"Airports: {airports.shape}")


# =========================================================
# 3. BASIC DATA TYPES
# =========================================================

print("\nConverting data types...")

flights["AIRLINE"] = flights["AIRLINE"].astype(str)

flights["ORIGIN_AIRPORT"] = (
    flights["ORIGIN_AIRPORT"].astype(str)
)

flights["DESTINATION_AIRPORT"] = (
    flights["DESTINATION_AIRPORT"].astype(str)
)


# =========================================================
# 4. CREATE DATE
# =========================================================

print("Creating flight date...")

flights["FLIGHT_DATE"] = pd.to_datetime(
    flights[["YEAR", "MONTH", "DAY"]].rename(
        columns={
            "YEAR": "year",
            "MONTH": "month",
            "DAY": "day"
        }
    ),
    errors="coerce"
)


# =========================================================
# 5. CREATE MONTH NAME
# =========================================================

flights["MONTH_NAME"] = (
    flights["FLIGHT_DATE"].dt.month_name()
)


# =========================================================
# 6. CREATE DAY NAME
# =========================================================

flights["DAY_NAME"] = (
    flights["FLIGHT_DATE"].dt.day_name()
)


# =========================================================
# 7. CREATE DEPARTURE HOUR
# =========================================================

flights["SCHEDULED_DEPARTURE"] = pd.to_numeric(
    flights["SCHEDULED_DEPARTURE"],
    errors="coerce"
)

flights["DEPARTURE_HOUR"] = (
    flights["SCHEDULED_DEPARTURE"] // 100
)


# =========================================================
# 8. CREATE DELAY FLAGS
# =========================================================

flights["IS_DEPARTURE_DELAYED"] = (
    flights["DEPARTURE_DELAY"] > 0
).astype(int)

flights["IS_ARRIVAL_DELAYED"] = (
    flights["ARRIVAL_DELAY"] > 0
).astype(int)


# =========================================================
# 9. CANCELLATION & DIVERSION FLAGS
# =========================================================

flights["IS_CANCELLED"] = (
    flights["CANCELLED"] == 1
).astype(int)

flights["IS_DIVERTED"] = (
    flights["DIVERTED"] == 1
).astype(int)


# =========================================================
# 10. DELAY CATEGORY
# =========================================================

def categorize_delay(delay):

    if pd.isna(delay):
        return "No Data"

    elif delay <= 0:
        return "On Time / Early"

    elif delay <= 15:
        return "Minor Delay"

    elif delay <= 60:
        return "Moderate Delay"

    else:
        return "Severe Delay"


flights["ARRIVAL_DELAY_CATEGORY"] = (
    flights["ARRIVAL_DELAY"]
    .apply(categorize_delay)
)


# =========================================================
# 11. TOTAL DELAY
# =========================================================

delay_columns = [
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

flights["TOTAL_DELAY_CAUSES"] = (
    flights[delay_columns]
    .fillna(0)
    .sum(axis=1)
)


# =========================================================
# 12. MAIN DELAY CAUSE
# =========================================================

def get_main_delay_cause(row):

    causes = {
        "Air System": row["AIR_SYSTEM_DELAY"],
        "Security": row["SECURITY_DELAY"],
        "Airline": row["AIRLINE_DELAY"],
        "Late Aircraft": row["LATE_AIRCRAFT_DELAY"],
        "Weather": row["WEATHER_DELAY"]
    }

    valid_causes = {
        key: value
        for key, value in causes.items()
        if pd.notna(value) and value > 0
    }

    if not valid_causes:
        return "No Recorded Cause"

    return max(
        valid_causes,
        key=valid_causes.get
    )


print("Creating main delay cause...")

flights["MAIN_DELAY_CAUSE"] = flights.apply(
    get_main_delay_cause,
    axis=1
)


# =========================================================
# 13. FACT FLIGHTS
# =========================================================

fact_columns = [
    "FLIGHT_DATE",
    "YEAR",
    "MONTH",
    "MONTH_NAME",
    "DAY",
    "DAY_OF_WEEK",
    "DAY_NAME",
    "DEPARTURE_HOUR",
    "AIRLINE",
    "FLIGHT_NUMBER",
    "ORIGIN_AIRPORT",
    "DESTINATION_AIRPORT",
    "DEPARTURE_DELAY",
    "ARRIVAL_DELAY",
    "CANCELLED",
    "DIVERTED",
    "IS_CANCELLED",
    "IS_DIVERTED",
    "IS_DEPARTURE_DELAYED",
    "IS_ARRIVAL_DELAYED",
    "ARRIVAL_DELAY_CATEGORY",
    "MAIN_DELAY_CAUSE",
    "TOTAL_DELAY_CAUSES",
    "DISTANCE"
]

fact_flights = flights[fact_columns].copy()


# =========================================================
# 14. DIM AIRLINE
# =========================================================

print("Creating Dim Airline...")

dim_airline = airlines.copy()

dim_airline = dim_airline.rename(
    columns={
        "IATA_CODE": "AIRLINE"
    }
)

dim_airline = dim_airline[
    [
        "AIRLINE",
        "AIRLINE"
    ]
]

# The previous structure has duplicate column names,
# so create the dimension directly.

dim_airline = airlines.rename(
    columns={
        "IATA_CODE": "AIRLINE",
        "AIRLINE": "AIRLINE_NAME"
    }
)

dim_airline = dim_airline[
    [
        "AIRLINE",
        "AIRLINE_NAME"
    ]
].drop_duplicates()


# =========================================================
# 15. DIM AIRPORT
# =========================================================

print("Creating Dim Airport...")

dim_airport = airports.rename(
    columns={
        "IATA_CODE": "AIRPORT_CODE",
        "AIRPORT": "AIRPORT_NAME"
    }
)

dim_airport = dim_airport[
    [
        "AIRPORT_CODE",
        "AIRPORT_NAME",
        "CITY",
        "STATE",
        "COUNTRY",
        "LATITUDE",
        "LONGITUDE"
    ]
].drop_duplicates()


# =========================================================
# 16. DIM DATE
# =========================================================

print("Creating Dim Date...")

date_min = flights["FLIGHT_DATE"].min()
date_max = flights["FLIGHT_DATE"].max()

date_range = pd.date_range(
    start=date_min,
    end=date_max,
    freq="D"
)

dim_date = pd.DataFrame({
    "DATE": date_range
})

dim_date["YEAR"] = (
    dim_date["DATE"].dt.year
)

dim_date["MONTH"] = (
    dim_date["DATE"].dt.month
)

dim_date["MONTH_NAME"] = (
    dim_date["DATE"].dt.month_name()
)

dim_date["DAY"] = (
    dim_date["DATE"].dt.day
)

dim_date["DAY_OF_WEEK"] = (
    dim_date["DATE"].dt.dayofweek + 1
)

dim_date["DAY_NAME"] = (
    dim_date["DATE"].dt.day_name()
)


# =========================================================
# 17. SAVE FILES
# =========================================================

print("\n" + "=" * 70)
print("SAVING POWER BI DATA MODEL")
print("=" * 70)

fact_file = os.path.join(
    RESULTS_DIR,
    "fact_flights.csv"
)

airline_file = os.path.join(
    RESULTS_DIR,
    "dim_airline.csv"
)

airport_file = os.path.join(
    RESULTS_DIR,
    "dim_airport.csv"
)

date_file = os.path.join(
    RESULTS_DIR,
    "dim_date.csv"
)

fact_flights.to_csv(
    fact_file,
    index=False
)

dim_airline.to_csv(
    airline_file,
    index=False
)

dim_airport.to_csv(
    airport_file,
    index=False
)

dim_date.to_csv(
    date_file,
    index=False
)


# =========================================================
# 18. VALIDATION
# =========================================================

print("\nFact Flights:")
print(fact_flights.shape)

print("\nDim Airline:")
print(dim_airline.shape)

print("\nDim Airport:")
print(dim_airport.shape)

print("\nDim Date:")
print(dim_date.shape)

print("\nFiles created:")

print("✓ results/fact_flights.csv")
print("✓ results/dim_airline.csv")
print("✓ results/dim_airport.csv")
print("✓ results/dim_date.csv")

print("\n" + "=" * 70)
print("POWER BI DATA MODEL READY")
print("=" * 70)