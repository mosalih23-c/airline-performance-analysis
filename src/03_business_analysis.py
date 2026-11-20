import pandas as pd
import os


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEANED_FILE = os.path.join(
    BASE_DIR,
    "results",
    "flights_cleaned.csv"
)

RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)


# =========================================================
# 1. LOAD CLEAN DATA
# =========================================================

print("=" * 70)
print("LOADING CLEAN DATA")
print("=" * 70)

df = pd.read_csv(
    CLEANED_FILE,
    low_memory=False
)

print(f"Dataset shape: {df.shape}")


# =========================================================
# 2. BASIC KPIs
# =========================================================

print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

total_flights = len(df)

cancelled_flights = df["IS_CANCELLED"].sum()

diverted_flights = df["IS_DIVERTED"].sum()

departure_delayed = df["IS_DEPARTURE_DELAYED"].sum()

arrival_delayed = df["IS_ARRIVAL_DELAYED"].sum()

cancellation_rate = (
    cancelled_flights / total_flights * 100
)

departure_delay_rate = (
    departure_delayed / total_flights * 100
)

arrival_delay_rate = (
    arrival_delayed / total_flights * 100
)

avg_departure_delay = df["DEPARTURE_DELAY"].mean()

avg_arrival_delay = df["ARRIVAL_DELAY"].mean()


print(f"Total Flights: {total_flights:,}")
print(f"Cancelled Flights: {cancelled_flights:,}")
print(f"Cancellation Rate: {cancellation_rate:.2f}%")
print(f"Diverted Flights: {diverted_flights:,}")
print(f"Departure Delay Rate: {departure_delay_rate:.2f}%")
print(f"Arrival Delay Rate: {arrival_delay_rate:.2f}%")
print(f"Average Departure Delay: {avg_departure_delay:.2f} minutes")
print(f"Average Arrival Delay: {avg_arrival_delay:.2f} minutes")


# =========================================================
# 3. SAVE KPI SUMMARY
# =========================================================

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Flights",
        "Cancelled Flights",
        "Cancellation Rate (%)",
        "Diverted Flights",
        "Departure Delay Rate (%)",
        "Arrival Delay Rate (%)",
        "Average Departure Delay (min)",
        "Average Arrival Delay (min)"
    ],
    "Value": [
        total_flights,
        cancelled_flights,
        cancellation_rate,
        diverted_flights,
        departure_delay_rate,
        arrival_delay_rate,
        avg_departure_delay,
        avg_arrival_delay
    ]
})

kpi_summary.to_csv(
    os.path.join(RESULTS_DIR, "kpi_summary.csv"),
    index=False
)


# =========================================================
# 4. AIRLINE PERFORMANCE
# =========================================================

print("\n" + "=" * 70)
print("AIRLINE PERFORMANCE")
print("=" * 70)

airline_analysis = (
    df.groupby(
        ["AIRLINE", "AIRLINE_NAME"],
        as_index=False
    )
    .agg(
        Total_Flights=("AIRLINE", "size"),
        Cancelled_Flights=("IS_CANCELLED", "sum"),
        Diverted_Flights=("IS_DIVERTED", "sum"),
        Delayed_Departures=("IS_DEPARTURE_DELAYED", "sum"),
        Delayed_Arrivals=("IS_ARRIVAL_DELAYED", "sum"),
        Avg_Departure_Delay=("DEPARTURE_DELAY", "mean"),
        Avg_Arrival_Delay=("ARRIVAL_DELAY", "mean")
    )
)

airline_analysis["Cancellation_Rate"] = (
    airline_analysis["Cancelled_Flights"]
    / airline_analysis["Total_Flights"] * 100
)

airline_analysis["Departure_Delay_Rate"] = (
    airline_analysis["Delayed_Departures"]
    / airline_analysis["Total_Flights"] * 100
)

airline_analysis["Arrival_Delay_Rate"] = (
    airline_analysis["Delayed_Arrivals"]
    / airline_analysis["Total_Flights"] * 100
)

airline_analysis = airline_analysis.sort_values(
    "Arrival_Delay_Rate",
    ascending=False
)

print(airline_analysis.to_string(index=False))

airline_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "airline_performance.csv"
    ),
    index=False
)


# =========================================================
# 5. MONTHLY ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("MONTHLY ANALYSIS")
print("=" * 70)

monthly_analysis = (
    df.groupby(
        ["MONTH", "MONTH_NAME"],
        as_index=False
    )
    .agg(
        Total_Flights=("MONTH", "size"),
        Cancelled_Flights=("IS_CANCELLED", "sum"),
        Delayed_Departures=("IS_DEPARTURE_DELAYED", "sum"),
        Delayed_Arrivals=("IS_ARRIVAL_DELAYED", "sum"),
        Avg_Departure_Delay=("DEPARTURE_DELAY", "mean"),
        Avg_Arrival_Delay=("ARRIVAL_DELAY", "mean")
    )
)

monthly_analysis["Cancellation_Rate"] = (
    monthly_analysis["Cancelled_Flights"]
    / monthly_analysis["Total_Flights"] * 100
)

monthly_analysis["Departure_Delay_Rate"] = (
    monthly_analysis["Delayed_Departures"]
    / monthly_analysis["Total_Flights"] * 100
)

monthly_analysis["Arrival_Delay_Rate"] = (
    monthly_analysis["Delayed_Arrivals"]
    / monthly_analysis["Total_Flights"] * 100
)

monthly_analysis = monthly_analysis.sort_values(
    "MONTH"
)

print(monthly_analysis.to_string(index=False))

monthly_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "monthly_analysis.csv"
    ),
    index=False
)


# =========================================================
# 6. DAY OF WEEK ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("DAY OF WEEK ANALYSIS")
print("=" * 70)

day_analysis = (
    df.groupby(
        ["DAY_OF_WEEK", "DAY_NAME"],
        as_index=False
    )
    .agg(
        Total_Flights=("DAY_OF_WEEK", "size"),
        Delayed_Departures=("IS_DEPARTURE_DELAYED", "sum"),
        Delayed_Arrivals=("IS_ARRIVAL_DELAYED", "sum"),
        Avg_Departure_Delay=("DEPARTURE_DELAY", "mean"),
        Avg_Arrival_Delay=("ARRIVAL_DELAY", "mean")
    )
)

day_analysis["Departure_Delay_Rate"] = (
    day_analysis["Delayed_Departures"]
    / day_analysis["Total_Flights"] * 100
)

day_analysis["Arrival_Delay_Rate"] = (
    day_analysis["Delayed_Arrivals"]
    / day_analysis["Total_Flights"] * 100
)

day_analysis = day_analysis.sort_values(
    "DAY_OF_WEEK"
)

print(day_analysis.to_string(index=False))

day_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "day_of_week_analysis.csv"
    ),
    index=False
)


# =========================================================
# 7. DEPARTURE HOUR ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("DEPARTURE HOUR ANALYSIS")
print("=" * 70)

hour_analysis = (
    df.groupby(
        "DEPARTURE_HOUR",
        as_index=False
    )
    .agg(
        Total_Flights=("DEPARTURE_HOUR", "size"),
        Delayed_Departures=("IS_DEPARTURE_DELAYED", "sum"),
        Delayed_Arrivals=("IS_ARRIVAL_DELAYED", "sum"),
        Avg_Departure_Delay=("DEPARTURE_DELAY", "mean"),
        Avg_Arrival_Delay=("ARRIVAL_DELAY", "mean")
    )
)

hour_analysis["Departure_Delay_Rate"] = (
    hour_analysis["Delayed_Departures"]
    / hour_analysis["Total_Flights"] * 100
)

hour_analysis["Arrival_Delay_Rate"] = (
    hour_analysis["Delayed_Arrivals"]
    / hour_analysis["Total_Flights"] * 100
)

hour_analysis = hour_analysis.sort_values(
    "DEPARTURE_HOUR"
)

print(hour_analysis.to_string(index=False))

hour_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "departure_hour_analysis.csv"
    ),
    index=False
)


# =========================================================
# 8. DELAY CAUSE ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("DELAY CAUSE ANALYSIS")
print("=" * 70)

delay_cause_analysis = (
    df.groupby(
        "MAIN_DELAY_CAUSE",
        as_index=False
    )
    .agg(
        Flights=("MAIN_DELAY_CAUSE", "size"),
        Total_Delay_Minutes=("TOTAL_DELAY_CAUSES", "sum")
    )
)

delay_cause_analysis["Percentage"] = (
    delay_cause_analysis["Flights"]
    / total_flights * 100
)

delay_cause_analysis = delay_cause_analysis.sort_values(
    "Flights",
    ascending=False
)

print(
    delay_cause_analysis.to_string(index=False)
)

delay_cause_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "delay_cause_analysis.csv"
    ),
    index=False
)


# =========================================================
# 9. AIRPORT PERFORMANCE
# =========================================================

print("\n" + "=" * 70)
print("ORIGIN AIRPORT PERFORMANCE")
print("=" * 70)

airport_analysis = (
    df.groupby(
        [
            "ORIGIN_AIRPORT",
            "ORIGIN_AIRPORT_NAME",
            "ORIGIN_CITY",
            "ORIGIN_STATE"
        ],
        as_index=False
    )
    .agg(
        Total_Flights=("ORIGIN_AIRPORT", "size"),
        Delayed_Departures=("IS_DEPARTURE_DELAYED", "sum"),
        Avg_Departure_Delay=("DEPARTURE_DELAY", "mean"),
        Cancelled_Flights=("IS_CANCELLED", "sum")
    )
)

airport_analysis["Departure_Delay_Rate"] = (
    airport_analysis["Delayed_Departures"]
    / airport_analysis["Total_Flights"] * 100
)

# Avoid ranking airports with very few flights
airport_analysis_filtered = airport_analysis[
    airport_analysis["Total_Flights"] >= 1000
].copy()

airport_analysis_filtered = airport_analysis_filtered.sort_values(
    "Departure_Delay_Rate",
    ascending=False
)

print(
    airport_analysis_filtered.head(20).to_string(
        index=False
    )
)

airport_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "airport_performance.csv"
    ),
    index=False
)


# =========================================================
# 10. ROUTE ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("ROUTE ANALYSIS")
print("=" * 70)

route_analysis = (
    df.groupby(
        [
            "ORIGIN_AIRPORT",
            "DESTINATION_AIRPORT"
        ],
        as_index=False
    )
    .agg(
        Total_Flights=("ORIGIN_AIRPORT", "size"),
        Delayed_Arrivals=("IS_ARRIVAL_DELAYED", "sum"),
        Avg_Arrival_Delay=("ARRIVAL_DELAY", "mean")
    )
)

route_analysis["Arrival_Delay_Rate"] = (
    route_analysis["Delayed_Arrivals"]
    / route_analysis["Total_Flights"] * 100
)

# Only routes with at least 500 flights
route_analysis_filtered = route_analysis[
    route_analysis["Total_Flights"] >= 500
].copy()

route_analysis_filtered = route_analysis_filtered.sort_values(
    "Arrival_Delay_Rate",
    ascending=False
)

print(
    route_analysis_filtered.head(20).to_string(
        index=False
    )
)

route_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "route_analysis.csv"
    ),
    index=False
)


# =========================================================
# 11. DELAY CATEGORY ANALYSIS
# =========================================================

print("\n" + "=" * 70)
print("DELAY CATEGORY ANALYSIS")
print("=" * 70)

delay_category_analysis = (
    df.groupby(
        "ARRIVAL_DELAY_CATEGORY",
        as_index=False
    )
    .agg(
        Flights=("ARRIVAL_DELAY_CATEGORY", "size")
    )
)

delay_category_analysis["Percentage"] = (
    delay_category_analysis["Flights"]
    / total_flights * 100
)

print(
    delay_category_analysis.to_string(
        index=False
    )
)

delay_category_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "delay_category_analysis.csv"
    ),
    index=False
)


# =========================================================
# 12. FINAL SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED")
print("=" * 70)

print("\nFiles created:")

files_created = [
    "kpi_summary.csv",
    "airline_performance.csv",
    "monthly_analysis.csv",
    "day_of_week_analysis.csv",
    "departure_hour_analysis.csv",
    "delay_cause_analysis.csv",
    "airport_performance.csv",
    "route_analysis.csv",
    "delay_category_analysis.csv"
]

for file in files_created:
    print(f"✓ results/{file}")

print("\nReady for Power BI.")