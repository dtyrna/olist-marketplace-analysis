# Olist Marketplace Optimization 🇧🇷📦
**An End-to-End Enterprise Data Pipeline & Machine Learning Project**

This project analyzes the Brazilian E-Commerce dataset provided by Olist. We built a scalable AWS cloud data pipeline using the Medallion Architecture, combined with localized predictive modeling to optimize customer experience and marketplace success. 

**[Key questions]**:

The analysis will investigate:

- Which sellers have much more processing time than the average?
- Is long processing time linked to delayed deliveries?
- Are incoming orders at the weekend, single categories or products responsible for delays?
- Could order splitting increase processing time?
- Which product categories receive lower review scores?
- Which regions have particularly long delivery times?
- Where are freight costs unusually high?
- Which combinations of seller, product, and region perform poorly?
- Which features influence the delivery process the most and effect customer reviews?

The goal is to identify specific and actionable problem areas rather than relying only on overall averages.

---

## 👥 The Team & Roles

To ensure a professional development workflow, we divided our responsibilities into specialized data roles. You can find the individual contributions and deep dives in the respective notebooks.

* **[Jakob Neubig] (Data Analyst & ML Engineer):** Focused on feature engineering (delivery and distance processes), predictive modeling using **Logistic Regression** (customer satisfaction classification and threshold optimization), and integration of ML insights into Power BI. Developed the Kaggle API integration (uitilizing environmental variables) and implemented the AWS script for date preprocessing.
* **[David Tyrna] (Data Analyst / Analytics Engineer):** Focused on Athena SQL transformations, Exploratory Data Analysis (EDA), KPI definition, and interactive **Power BI Dashboarding**.
* **[Parick Janotte] (Data Engineer):** Focused on cloud infrastructure architecture (**AWS Lambda, S3, Athena**), Bronze-to-Silver preprocessing pipelines, secure API integrations, and schema validation.

---

## 🏗️ Cloud Data Architecture & Pipeline (AWS & Medallion)

Instead of relying on local files, we designed a production-ready, secure cloud data pipeline using **Amazon Web Services (AWS)** and the **Medallion Schema**.

```
[Kaggle API via Lambda] ➔ [Secure AWS S3 Bucket] ➔ [AWS Lambda (Preprocessing)] ➔ [AWS Athena (SQL)] ➔ [Power BI DirectQuery]
```

### 🥉 Bronze Layer (Raw Cloud Ingestion)
* **Secure API Ingestion:** Built an **AWS Lambda** script to dynamically pull the 9 relational Olist tables directly from the Kaggle API. --> scripts/bronze/bronze_API_kaggle.ipynb
* **Security Best Practices:** Kaggle API keys were securely injected via **environment variables** to prevent credential leaks.

### 🥈 Silver Layer (Serverless Preprocessing)
* **Serverless Compute:** Python preprocessing notebooks were refactored into modular **AWS Lambda scripts** triggered by data arrival.
* **Real-World Data Challenge Solved:** Faced severe inconsistencies with geographic data (missing coordinates for some zip codes, but hundreds of duplicate, conflicting GPS points for others).
* **The Solution:** We resolved this pragmatically by grouping the data by zip code prefix and applying `keep='first'` to quickly remove redundant entries, keep the dataset lightweight, and stabilize          the pipeline. 
* **Data Verification:** All preprocessing steps, text cleaning (using the `.join()` approach), and surrogate key creations are documented in the notebook: *scriptscripts/silver/silver_clean_geo_location.order_items.product_category_names.ipynb


### 🥇 Gold Layer (Cloud Analytics & Business Logic)
* **Serverless Querying:** Utilized **AWS Athena** to run optimized **SQL** queries directly over our cleaned S3 files to build analytical aggregates without maintaining a costly database server.
* **BI Integration:** The Gold data tables were connected to **Power BI** via direct streaming for seamless dashboard reporting.

---

## 💻 Hybrid Infrastructure & Production Trade-offs (ML)

In a real enterprise environment, architecture is driven by budget constraints. We intentionally adopted a **hybrid infrastructure** approach:

* **Why ML Ran Locally:** Due to **AWS Free Tier resource limits**, hosting a continuous cloud-based training compute instance was not cost-effective. The complete modeling notebook was executed locally to optimize resource consumption.
* **Power BI & Python Constraints:** Because Power BI restricts native Python scripts in cloud-refreshed environments, we pre-calculated the ML insights and successfully injected them via a **Power BI Python Visual**. Due to project imeline constraints, the connected Power BI dashboard visualizes an earlier iteration of our predictive model. The final model is in scripts (scripts/gold/gold_machine_learning.ipynb).
* **Reproducibility:** Every single step of our modeling, evaluation, and visualization is **fully preserved, executed, and commented with Markdown** inside the (scripts/gold/gold_machine_learning.ipynb) notebook.

---

## 🛠️ Tech Stack


* **Cloud Infrastructure:** AWS (S3, Lambda, Athena)
* **Data Engineering & Analysis:** Python (Pandas, NumPy), SQL (Athena)
* **Machine Learning:** Scikit-Learn (Logistic Regression)
* **Visualization & Reporting:** Power BI (including Python Visuals), Matplotlib, Seaborn
=======
**Which regions, product categories, and sellers show the largest customer experience problems?**



