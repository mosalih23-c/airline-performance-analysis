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

OUTPUT_FILE = os.path.join(RESULTS_DIR, "flights_cleaned.csv")


# Create results folder if it doesn't exist
os.makedirs(RESULTS_DIR, exist_ok=True)


# =========================================================
# 1. LOAD DATA
# =========================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

flights = pd.read_csv(
    FLIGHTS_FILE,
    low_memory=False
)

airlines = pd.read_csv(AIRLINES_FILE)
airports = pd.read_csv(AIRPORTS_FILE)

print(f"Flights: {flights.shape}")
print(f"Airlines: {airlines.shape}")
print(f"Airports: {airports.shape}")


# =========================================================
# 2. FIX AIRPORT CODE COLUMNS
# =========================================================

print("\n" + "=" * 70)
print("FIXING AIRPORT CODES")
print("=" * 70)

flights["ORIGIN_AIRPORT"] = flights["ORIGIN_AIRPORT"].astype(str)
flights["DESTINATION_AIRPORT"] = flights["DESTINATION_AIRPORT"].astype(str)

print("Airport code columns converted to string.")


# =========================================================
# 3. MERGE AIRLINE NAMES
# =========================================================

print("\n" + "=" * 70)
print("MERGING AIRLINE NAMES")
print("=" * 70)

flights = flights.merge(
    airlines,
    left_on="AIRLINE",
    right_on="IATA_CODE",
    how="left"
)

# Rename airline name column
flights.rename(
    columns={"AIRLINE_y": "AIRLINE_NAME"},
    inplace=True
)

# Keep original airline code
if "AIRLINE_x" in flights.columns:
    flights.rename(
        columns={"AIRLINE_x": "AIRLINE"},
        inplace=True
    )

# Remove unnecessary lookup column
if "IATA_CODE" in flights.columns:
    flights.drop(columns=["IATA_CODE"], inplace=True)

print("Airline names merged successfully.")


# =========================================================
# 4. CREATE FLIGHT DATE
# =========================================================

print("\n" + "=" * 70)
print("CREATING DATE FEATURES")
print("=" * 70)

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

flights["MONTH_NAME"] = flights["FLIGHT_DATE"].dt.month_name()

flights["DAY_NAME"] = flights["FLIGHT_DATE"].dt.day_name()

flights["DAY_OF_MONTH"] = flights["FLIGHT_DATE"].dt.day


# =========================================================
# 5. CREATE DEPARTURE HOUR
# =========================================================

print("Creating departure hour...")

# Scheduled departure is stored as HHMM
flights["SCHEDULED_DEPARTURE"] = pd.to_numeric(
    flights["SCHEDULED_DEPARTURE"],
    errors="coerce"
)

flights["DEPARTURE_HOUR"] = (
    flights["SCHEDULED_DEPARTURE"] // 100
).astype("Int64")


# =========================================================
# 6. CREATE DELAY FLAGS
# =========================================================

print("\n" + "=" * 70)
print("CREATING DELAY FEATURES")
print("=" * 70)

# Departure delay
flights["IS_DEPARTURE_DELAYED"] = (
    flights["DEPARTURE_DELAY"] > 0
).astype(int)

# Arrival delay
flights["IS_ARRIVAL_DELAYED"] = (
    flights["ARRIVAL_DELAY"] > 0
).astype(int)


# =========================================================
# 7. CREATE CANCELLATION / DIVERSION FLAGS
# =========================================================

flights["IS_CANCELLED"] = (
    flights["CANCELLED"] == 1
).astype(int)

flights["IS_DIVERTED"] = (
    flights["DIVERTED"] == 1
).astype(int)


# =========================================================
# 8. CREATE DELAY CATEGORY
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
    flights["ARRIVAL_DELAY"].apply(categorize_delay)
)


# =========================================================
# 9. CREATE TOTAL DELAY CAUSES
# =========================================================

delay_columns = [
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

# Important:
# NaN in these columns generally means that no delay amount
# was recorded for that cause.
flights["TOTAL_DELAY_CAUSES"] = (
    flights[delay_columns]
    .fillna(0)
    .sum(axis=1)
)


# =========================================================
# 10. CREATE MAIN DELAY CAUSE
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
# 11. MERGE AIRPORT INFORMATION
# =========================================================

print("\n" + "=" * 70)
print("MERGING AIRPORT INFORMATION")
print("=" * 70)

# Origin airport information
origin_airports = airports.copy()

origin_airports = origin_airports.rename(
    columns={
        "IATA_CODE": "ORIGIN_AIRPORT",
        "AIRPORT": "ORIGIN_AIRPORT_NAME",
        "CITY": "ORIGIN_CITY",
        "STATE": "ORIGIN_STATE",
        "COUNTRY": "ORIGIN_COUNTRY",
        "LATITUDE": "ORIGIN_LATITUDE",
        "LONGITUDE": "ORIGIN_LONGITUDE"
    }
)

origin_airports = origin_airports[
    [
        "ORIGIN_AIRPORT",
        "ORIGIN_AIRPORT_NAME",
        "ORIGIN_CITY",
        "ORIGIN_STATE",
        "ORIGIN_COUNTRY",
        "ORIGIN_LATITUDE",
        "ORIGIN_LONGITUDE"
    ]
]

flights = flights.merge(
    origin_airports,
    on="ORIGIN_AIRPORT",
    how="left"
)


# Destination airport information
destination_airports = airports.copy()

destination_airports = destination_airports.rename(
    columns={
        "IATA_CODE": "DESTINATION_AIRPORT",
        "AIRPORT": "DESTINATION_AIRPORT_NAME",
        "CITY": "DESTINATION_CITY",
        "STATE": "DESTINATION_STATE",
        "COUNTRY": "DESTINATION_COUNTRY",
        "LATITUDE": "DESTINATION_LATITUDE",
        "LONGITUDE": "DESTINATION_LONGITUDE"
    }
)

destination_airports = destination_airports[
    [
        "DESTINATION_AIRPORT",
        "DESTINATION_AIRPORT_NAME",
        "DESTINATION_CITY",
        "DESTINATION_STATE",
        "DESTINATION_COUNTRY",
        "DESTINATION_LATITUDE",
        "DESTINATION_LONGITUDE"
    ]
]

flights = flights.merge(
    destination_airports,
    on="DESTINATION_AIRPORT",
    how="left"
)


# =========================================================
# 12. CLEAN UNNECESSARY COLUMNS
# =========================================================

print("\n" + "=" * 70)
print("CLEANING COLUMNS")
print("=" * 70)

# The original lookup columns are no longer necessary
# after merging airline and airport information.

# Keep the dataset comprehensive for Power BI.
# We are not deleting useful delay or flight information.


# =========================================================
# 13. SAVE CLEAN DATA
# =========================================================

print("\n" + "=" * 70)
print("SAVING CLEAN DATA")
print("=" * 70)

print(f"Final shape: {flights.shape}")

flights.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved to:")
print(OUTPUT_FILE)


# =========================================================
# 14. BASIC VALIDATION
# =========================================================

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

print("\nCancellation:")
print(
    flights["IS_CANCELLED"].value_counts()
)

print("\nDiversion:")
print(
    flights["IS_DIVERTED"].value_counts()
)

print("\nDeparture delay:")
print(
    flights["IS_DEPARTURE_DELAYED"].value_counts()
)

print("\nArrival delay:")
print(
    flights["IS_ARRIVAL_DELAYED"].value_counts()
)

print("\nDelay categories:")
print(
    flights["ARRIVAL_DELAY_CATEGORY"].value_counts()
)

print("\nMain delay causes:")
print(
    flights["MAIN_DELAY_CAUSE"].value_counts()
)

print("\nAirlines:")
print(
    flights["AIRLINE_NAME"].value_counts()
)

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)