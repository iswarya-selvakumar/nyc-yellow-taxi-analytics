# nyc-yellow-taxi-analytics

Built an end-to-end AWS Data Engineering pipeline using S3, AWS Glue, PySpark, Athena, and Power BI. Processed 24.08M NYC taxi trip records, implemented data quality validation, designed a Star Schema, automated workflow orchestration, and delivered business insights through interactive dashboards.

## Project Overview

This project demonstrates an end-to-end Data Engineering pipeline built on AWS using the NYC TLC Yellow Taxi dataset. The solution follows the Medallion Architecture (Raw → Silver → Gold) and processes large-scale taxi trip data using PySpark on AWS Glue.

The pipeline performs data quality validation, transforms raw trip records into curated analytical datasets, builds a dimensional model (Star Schema), and enables business reporting through Amazon Athena and Power BI.

## Technology Stack

| Layer | Technology |
|---------|------------|
| Storage | Amazon S3 |
| Processing | AWS Glue, PySpark |
| Data Catalog | AWS Glue Catalog |
| Orchestration | AWS Glue Workflows |
| Query Engine | Amazon Athena |
| Visualization | Power BI |
| File Format | Parquet |

## Business Objective

The objective of this project is to transform raw NYC taxi trip data into a structured analytical platform that supports:

* Revenue analysis
* Trip volume analysis
* Payment method analysis
* Vendor performance analysis
* Location-based insights
* Dashboard reporting and business intelligence

## Dataset

Source: NYC TLC Yellow Taxi Trip Records

Analysis Period: January 2025 – June 2025

### Data Volume

| Metric           | Value      |
| ---------------- | ---------- |
| Raw Records      | 24,083,384 |
| Valid Records    | 22,020,272 |
| Rejected Records | 2,063,112  |
| Rejection Rate   | 8.57%      |

## Architecture

![Architecture Diagram](architecture/Architecture_diagram.png)

The solution implements a Medallion Architecture (Raw → Silver → Gold) using AWS services for scalable data processing, analytics, and reporting.

## Silver Layer Processing

The Silver layer performs data cleansing and validation.

### Data Quality Checks

* Null value handling
* Invalid trip distance removal
* Invalid fare amount removal
* Pickup/Dropoff timestamp validation
* Data quality flag generation

### Transformations

* Pickup date extraction
* Pickup year extraction
* Pickup month extraction
* Trip duration calculation
* Partitioning by year and month

## Gold Layer Processing

The Gold layer transforms curated data into a dimensional model for analytics.

### Fact Table

* fact_trip

### Dimension Tables

* dim_date
* dim_vendor
* dim_payment
* dim_ratecode
* dim_location

### Modeling Approach

Star Schema

## Project Structure

```text
nyc-yellow-taxi-analytics/
│
├── README.md
├── architecture/
│   └── Architecture_diagram.png
├── glue_jobs/
│   ├── silver_etl.py
│   └── gold_etl.py
├── athena_queries/
│   └── analytics_queries.csv
├── dashboards/
│   └── nyc_taxi_dashboard.pbix
└── screenshots/
    ├── workflow_orchestration.png
    ├── dashboard_page1.png
    └── dashboard_page2.png
```

## Workflow Orchestration

AWS Glue Workflow orchestrates the pipeline execution:

Silver Job
→ Gold Job
→ Glue Crawler

This ensures that the catalog is automatically updated after ETL processing.

![workflow Orchestration](screenshots/workflow_orchestration.png)

## Analytics Queries

The following analytical queries were developed in Amazon Athena:

1. Monthly Revenue Trend
2. Monthly Trip Volume
3. Average Trip Distance
4. Average Trip Duration
5. Payment Method Distribution
6. Revenue by Payment Type
7. Top 10 Pickup Locations
8. Top 10 Revenue Generating Pickup Zones
9. Vendor Performance
10. Average Tip by Payment Type

## Power BI Dashboard

The final analytics layer is visualized using Power BI dashboards that provide executive and operational insights.

## Dashboard KPIs

* Total Revenue: $621.20M
* Total Trips: 22.02M
* Average Trip Duration: 16.69 Minutes
* Average Trip Distance: 6.52 Miles

## Dashboard Pages

### Executive Overview

* Revenue Trend
* Trip Volume Trend
* KPI Cards
* Payment Method Distribution

![Executive Overview](screenshots/dashboard_page1.png)

### Operational Analysis

* Vendor Performance
* Revenue by Payment Type
* Top Pickup Locations
* Top Revenue Generating Zones

![Operational Analysis](screenshots/dashboard_page2.png)

## Key Insights

- Generated $621.20M in revenue during Jan–Jun 2025.
- Processed 22.02M valid taxi trips.
- Credit Card was the dominant payment method.
- JFK Airport and Midtown areas generated the highest revenue.
- Average trip duration was 16.69 minutes.
- Average trip distance was 6.52 miles.

## Key Learnings

Through this project I gained hands-on experience with:

* Data Lake Architecture
* AWS Glue ETL Development
* PySpark Transformations
* Data Quality Framework Design
* Star Schema Modeling
* Athena Query Optimization
* Workflow Orchestration
* Business Intelligence Dashboard Development
  
## Project Highlights

- Processed 24.08M raw records using PySpark on AWS Glue.
- Removed 2.06M invalid records through data quality validation.
- Designed and implemented a Star Schema with 1 fact table and 5 dimension tables.
- Automated ETL execution using AWS Glue Workflows.
- Queried analytical datasets using Amazon Athena.
- Built interactive Power BI dashboards for business reporting.
