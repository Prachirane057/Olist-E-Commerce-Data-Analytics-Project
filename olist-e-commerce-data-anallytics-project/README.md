# Olist E-Commerce Performance Intelligence

An end-to-end data analytics project focused on analyzing Brazilian e-commerce performance using the Olist dataset. This project covers data cleaning, SQL analysis, business intelligence dashboards, and actionable business insights.

## 📌 Project Overview

The objective of this project is to transform raw e-commerce data into meaningful insights related to sales performance, customer behavior, product categories, seller performance, delivery operations, payment methods, and customer satisfaction.

The project uses Python for data cleaning, MySQL for querying and analysis, and Power BI for interactive dashboards and business reporting.

## 🛠️ Tools & Technologies

- **Python** — Data cleaning and preprocessing
- **Pandas** — Data manipulation and analysis
- **MySQL** — SQL queries and business analysis
- **Power BI** — Interactive dashboards and data visualization
- **Microsoft Excel / CSV** — Data inspection and storage
- **GitHub** — Project documentation and version control

## 📂 Repository Structure

```text
Olist-E-Commerce-Data-Analytics-Project/
│
├── Raw Data/
│   └── Original source datasets
│
├── Cleaned Data/
│   └── Cleaned and processed CSV files
│
├── Code/
│   └── Python data-cleaning scripts
│
├── Dashboards and Insights/
│   ├── Power BI dashboard (.pbix)
│   ├── Business Insights report (.pdf)
│   
│
│
└── README.md
```



## 📊 Dataset Description

The project uses the Brazilian E-Commerce Public Dataset by Olist, containing information about orders, customers, sellers, products, payments, reviews, and geolocation.

| Dataset | Records / Description |
|---|---:|
| Orders | 99,441 |
| Order Items | 112,650 |
| Payments | 103,886 |
| Reviews | 99,224 |
| Customers | 99,441 |
| Products | 32,951 |
| Sellers | 3,095 |
| Product Category Translation | 71 |
| Geolocation | Geographic coordinates and location information |

The dataset primarily covers orders from September 2016 to October 2018. The final months of 2018 have limited data and should be interpreted carefully.

## 🔄 Project Workflow

1. **Data Inspection:** Examined the original datasets, their structure, columns, missing values, and potential quality issues.
2. **Data Cleaning:** Used Python and Pandas to clean and prepare the datasets for analysis while preserving the original source files.
3. **Data Preparation:** Checked data types, handled data-quality issues, and prepared the tables for integration.
4. **SQL Analysis:** Used MySQL to explore sales, orders, products, sellers, customers, payments, and delivery performance.
5. **Data Modeling:** Connected relevant datasets using appropriate keys and relationships.
6. **Power BI Development:** Created interactive dashboards to track key performance indicators and business trends.
7. **Business Insights:** Identified patterns, performance indicators, and areas for further investigation.
8. **Documentation:** Organized project files and documented the findings.

## 📈 Power BI Dashboard Pages

### 1. Executive Overview

Provides a high-level view of overall e-commerce performance.

**Key metrics and analysis:**
- Total orders and sales
- Order and sales trends
- Average order value
- Customer and transaction overview
- High-level business performance indicators

### 2. Sales & Order Trends

Analyzes sales performance and changes in order activity over time.

**Key analysis:**
- Monthly sales and order trends
- Year-over-year comparisons
- Order-value distribution
- Sales performance by time period
- Identification of peak sales months

### 3. Product & Seller Performance

Evaluates product category performance and seller contribution.

**Key analysis:**
- Top-performing product categories
- Product sales and item volume
- Seller-level sales performance
- Contribution of leading sellers
- Product price and freight patterns

### 4. Delivery & Operations

Examines delivery efficiency and operational performance.

**Key analysis:**
- On-time versus late deliveries
- Average delivery time
- Purchase-to-carrier and carrier-to-customer timelines
- Delivery performance patterns
- Potential operational improvement areas

### 5. Customer Experience & Payments

Explores customer satisfaction, review scores, and payment behavior.

**Key analysis:**
- Review score distribution
- Average customer review score
- Payment methods and payment value
- Installment behavior
- Repeat versus one-time customers

## 🔍 Key Business Insights

### Sales Performance

- The dataset contains **99,441 orders** and **112,650 order-item records**.
- Total item-price sales were approximately **R$13.59 million**.
- Total recorded payment value was approximately **R$16.01 million**.
- November 2017 was the strongest month in the report, with approximately **R$1.01 million in item-price sales** across 7,544 orders.
- Reported 2018 sales exceeded 2017 sales, but the 2018 dataset is incomplete. Therefore, a direct full-year comparison should be treated cautiously.
- Approximately **95.68% of orders** fell within the R$0–R$500 order-value band used in the analysis.

### Product & Seller Performance

- **Health & Beauty** generated approximately R$1.26 million in item-price sales.
- **Watches & Gifts** generated approximately R$1.21 million in item-price sales.
- **Bed, Bath & Table** recorded the highest item volume among the categories highlighted in the report, with 11,115 items.
- The leading seller generated approximately R$229,472 in sales across 1,156 order-item records.
- The top 10 sellers collectively contributed approximately R$1.79 million, or about 13.15% of item-price sales.
- The analysis reported a positive correlation of approximately **0.414 between item price and freight value**. This is an association, not proof of causation.

### Customer & Geographic Insights

- São Paulo (SP) was the leading customer state in the report, accounting for approximately **R$5.20 million**, or 38.3% of item-price sales.
- The average freight value was approximately **R$19.99 per order-item record**.
- The customer dataset contains 99,441 records, while the report identified 96,096 unique customer identities.

### Delivery & Operations

- The reported on-time delivery rate was approximately **91.88%–91.89%**, depending on the denominator used.
- The report recorded approximately 88,644 on-time deliveries and 7,825 late deliveries.
- Average delivery time was approximately **12.56 days**, while the median was approximately **10.22 days**.
- The report also examined different stages of the delivery process to identify where delays may occur.

### Customer Experience

- The average review score was approximately **4.09 out of 5**.
- Approximately **77.07%** of reviews were rated 4 or 5.
- Approximately **14.69%** of reviews were rated 1 or 2.
- The report recorded 57,328 five-star reviews and 11,424 one-star reviews.
- Approximately 96.88% of customers were classified as one-time customers and 3.12% as repeat customers under the report's methodology.

### Payment Behavior

- Credit cards accounted for approximately **R$12.54 million**, or 78.34% of recorded payment value.
- Boleto payments accounted for approximately **R$2.87 million**, or 17.92% of recorded payment value.
- Approximately 49.42% of payment records involved more than one installment.

## 📌 Key Performance Indicators (KPIs)

The project analyzes business indicators such as:

- Total Orders
- Total Item-Price Sales
- Total Payment Value
- Average Order Value
- Average Freight Value
- Sales by Product Category
- Sales by Seller
- On-Time Delivery Rate
- Average Delivery Time
- Average Review Score
- Positive and Low Review Share
- Payment Method Distribution
- Repeat Customer Share

**Metric note:** Item-price sales, total payment value, and average order value are different measures. Their values can differ because of freight, payment records, order composition, and the calculation method. KPI definitions should be checked before comparing results across dashboards or reports.

## ⚠️ Data Quality & Limitations

- The source datasets require cleaning and validation before analysis.
- The 2018 data is incomplete, especially toward the end of the available period.
- Delivery percentages and counts should be reconciled against one consistent eligible-order denominator.
- The report contains small differences in the reported on-time delivery rate and average order value across calculations. These should be validated against the final Power BI measures and SQL queries.
- Payment value should not be treated as identical to item-price sales.
- Correlation and observed patterns do not establish causation.
- Customer repeat-purchase results depend on how customer identities and repeat orders are defined.
- Findings describe the available dataset and may not represent all e-commerce businesses or current market conditions.

## 💡 Business Recommendations

Based on the patterns identified in the analysis:

1. **Improve delivery monitoring:** Track late deliveries and delivery-stage durations to identify potential operational bottlenecks.
2. **Support high-performing categories:** Monitor sales and item-volume trends to inform product assortment and merchandising decisions.
3. **Evaluate seller performance:** Compare sales contribution, order volume, and delivery outcomes to identify sellers who may benefit from operational support.
4. **Strengthen customer retention:** Investigate the low repeat-customer share and explore opportunities to encourage repeat purchases.
5. **Monitor customer feedback:** Review low-rated orders alongside delivery and order details to identify recurring service issues.
6. **Review payment behavior:** Use payment-method and installment patterns to understand how customers complete purchases.
7. **Validate business metrics:** Standardize KPI definitions and denominators so that reports and dashboards remain consistent.

These recommendations are based on descriptive analysis. Further investigation would be required to test their impact.

## 🎯 Project Objectives

- Build a complete data analytics workflow from raw data to business reporting.
- Apply Python and Pandas to data cleaning and preprocessing.
- Use MySQL to analyze e-commerce performance.
- Build interactive Power BI dashboards.
- Identify trends in sales, customer behavior, product categories, sellers, payments, and deliveries.
- Communicate findings through structured documentation and visualizations.

## 🚀 Skills Demonstrated

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Python and Pandas
- SQL Querying and Aggregation
- Data Modeling and Relationships
- KPI Design and Validation
- Power BI Dashboard Development
- Business Intelligence and Data Storytelling
- Data Quality Checks
- Technical Documentation

## 📁 Project Files

Explore the repository folders to access:

- **Raw Data:** Original source datasets
- **Cleaned Data:** Processed datasets prepared for analysis
- **Code:** Python scripts used for data cleaning
- **Dashboards and Insights:** Power BI dashboard and business insights report
- **SQL:** SQL analysis scripts, if included
- **Documentation:** Supporting project documentation, if included

## 👥 Project Contributors

- Mayank Naresh Ganeshe
- Prachi Rane

## 🏁 Conclusion

This project demonstrates how raw e-commerce data can be transformed into structured datasets, SQL-based analysis, interactive dashboards, and business insights. By examining sales, products, sellers, delivery performance, customer reviews, and payment behavior, the project provides a consolidated view of the Olist e-commerce ecosystem.

The project also highlights the importance of data quality, consistent KPI definitions, and careful interpretation of incomplete or descriptive data.

---

**Tools:** Python | Pandas | MySQL | Power BI | GitHub

**Project Type:** End-to-End Data Analytics & Business Intelligence
