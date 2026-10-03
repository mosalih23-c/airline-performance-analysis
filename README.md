# ✈️ Airline Performance Analysis

## 📊 Project Overview

This project analyzes airline flight performance using the 2015 U.S. Flight Delays and Cancellations dataset.

The project combines **Python, Pandas, SQL-style business analysis concepts, and Power BI** to transform raw flight data into an interactive business intelligence dashboard.

The analysis focuses on:

- Flight volume
- Flight cancellations
- Departure and arrival delays
- Delay causes
- Airline performance
- Airport performance
- Route performance
- Delay patterns by month, day, and departure hour

---

## 🎯 Business Questions

The analysis aims to answer questions such as:

1. How many flights were operated?
2. What percentage of flights were cancelled?
3. Which airlines handled the largest number of flights?
4. Which airlines had higher arrival delay rates?
5. What were the main recorded causes of delays?
6. Which airports handled the highest number of flights?
7. Which routes had the highest flight volumes?
8. During which hours were arrival delays higher?
9. How did delays vary across days of the week?
10. How did airline and airport performance change when applying filters?

---

## 📁 Dataset

The dataset is based on the **2015 U.S. Flight Delays and Cancellations** data.

Main source tables:

- `flights.csv`
- `airlines.csv`
- `airports.csv`

The original flight dataset contains:

- **5,819,079 flights**
- **31 original columns**
- **14 airlines**
- **322 airports**

Due to the large size of the raw dataset, the original CSV files are not included in the GitHub repository.

---

## 🛠️ Technologies Used

### Python
- Python
- Pandas
- NumPy

### Data Analysis
- Data Cleaning
- Exploratory Data Analysis
- Business Analysis
- Feature Engineering

### Data Visualization & BI
- Microsoft Power BI
- DAX
- Interactive Slicers
- KPI Cards
- Bar Charts
- Column Charts
- Line Charts
- Donut Charts

### Development
- VS Code
- Git
- GitHub

---

## 🔄 Project Workflow

```text
Raw Flight Data
       ↓
Python / Pandas
       ↓
Data Understanding
       ↓
Data Cleaning
       ↓
Business Analysis
       ↓
Star Schema Preparation
       ↓
Power BI Data Model
       ↓
DAX Measures
       ↓
Interactive Dashboard
       ↓
Business Insights
🧹 Data Preparation

The raw flight data was processed using Python.

The cleaning process included:

Handling missing values
Creating flight date fields
Creating delay indicators
Creating cancellation indicators
Creating diversion indicators
Categorizing arrival delays
Identifying the main recorded delay cause
Calculating total delay causes
Merging airline information
Merging airport information
Creating analytical datasets
⭐ Power BI Data Model

A Star Schema was created to support interactive filtering and analysis.

Fact Table

fact_flights

Contains flight-level information such as:

Flight Date
Airline
Flight Number
Origin Airport
Destination Airport
Departure Delay
Arrival Delay
Cancellation
Diversion
Delay Category
Main Delay Cause
Distance
Dimension Tables
dim_airline
dim_date
dim_origin_airport
dim_destination_airport
Model Structure
                 dim_airline
                     │
                     │
dim_date ─────── fact_flights ─────── dim_origin_airport
                     │
                     │
             dim_destination_airport
📐 DAX Measures

Key measures created in Power BI include:

Total Flights
Total Flights =
COUNTROWS(fact_flights)
Cancelled Flights
Cancelled Flights =
CALCULATE(
    COUNTROWS(fact_flights),
    fact_flights[IS_CANCELLED] = 1
)
Cancellation Rate
Cancellation Rate =
DIVIDE(
    [Cancelled Flights],
    [Total Flights]
)
Arrival Delay Rate
Arrival Delay Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS(fact_flights),
        fact_flights[IS_ARRIVAL_DELAYED] = 1
    ),
    [Total Flights]
)
Average Arrival Delay
Average Arrival Delay =
AVERAGE(fact_flights[ARRIVAL_DELAY])
Average Departure Delay
Average Departure Delay =
AVERAGE(fact_flights[DEPARTURE_DELAY])
📊 Dashboard

The Power BI dashboard contains multiple analytical pages.

1. Executive Overview

Provides a high-level view of overall flight operations.

Includes:

Total Flights
Cancelled Flights
Cancellation Rate
Arrival Delay Rate
Flights by Month
Arrival Delay Rate by Month
Arrival Delay Categories
Recorded Delay Causes
2. Airline Performance

Focuses on comparing airline-level performance.

Includes:

Total Flights by Airline
Arrival Delay Rate by Airline
Average Arrival Delay by Airline
Cancelled Flights
Cancellation Rate

Interactive filters allow users to analyze airline performance by month and airport.

3. Airport & Route Analysis

Focuses on airport and route activity.

Includes:

Top 10 Origin Airports
Top 10 Destination Airports
Top 10 Routes
Top 10 Origin Airports by Average Arrival Delay
4. Flight Delay Analysis

Focuses specifically on flight delays.

Includes:

Recorded Delay Causes
Arrival Delay Categories
Average Arrival Delay by Departure Hour
Arrival Delay Rate by Day of Week
📈 Key Metrics
Metric	Value
Total Flights	5,819,079
Cancelled Flights	89,884
Cancellation Rate	1.54%
Diverted Flights	15,187
Departure Delay Rate	36.53%
Arrival Delay Rate	35.86%
Average Departure Delay	9.37 min
Average Arrival Delay	4.41 min
🔎 Delay Categories

The analysis categorized flights according to arrival delay:

Category	Flights
On Time / Early	3,627,112
Minor Delay	1,063,398
Moderate Delay	704,406
Severe Delay	319,092
No Data	105,071
🚨 Recorded Delay Causes

The main recorded causes included:

Late Aircraft
Airline
Air System
Weather
Security

A large portion of flights did not have a recorded delay cause in the available cause fields.

📂 Project Structure
airline-performance-analysis/
│
├── data/
│   ├── flights.csv
│   ├── airlines.csv
│   └── airports.csv
│
├── src/
│   ├── 01_data_understanding.py
│   ├── 02_data_cleaning.py
│   ├── 03_business_analysis.py
│   └── 04_powerbi_dataset.py
│
├── results/
│   ├── kpi_summary.csv
│   ├── airline_performance.csv
│   ├── monthly_analysis.csv
│   ├── day_of_week_analysis.csv
│   ├── departure_hour_analysis.csv
│   ├── delay_cause_analysis.csv
│   ├── airport_performance.csv
│   ├── route_analysis.csv
│   └── delay_category_analysis.csv
│
├── .gitignore
└── README.md
💡 Project Outcome

This project demonstrates an end-to-end data analytics workflow:

Raw Data → Python → Data Cleaning → Business Analysis → Data Modeling → Power BI → Interactive Dashboard

It combines technical data preparation with business-focused analysis and interactive visualization.

👨‍💻 Author

Mohamed Salih

Data Analytics | Data Science | Python | Power BI

GitHub: mosalih23-c