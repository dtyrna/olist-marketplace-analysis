# Olist Marketplace Optimization

> End-to-end data analytics project based on the Olist Brazilian E-Commerce dataset.

---

## 1. Introduction

This project analyzes the Brazilian E-Commerce dataset provided by Olist.

The main objective is to understand how Olist can improve its customer experience and strengthen the long-term success of its marketplace through data-driven decisions.

The project combines customer behavior, orders, products, sellers, delivery performance, reviews, payments, and geographic information.

The goal is not only to describe what happened, but also to identify relevant patterns, understand potential causes, develop predictive models, and translate the results into actionable business recommendations.

---

## 2. Business Problem

Olist operates as an e-commerce marketplace connecting customers and sellers across Brazil.

For a marketplace, long-term success depends on more than generating sales. Customer satisfaction, reliable delivery, and strong seller performance are important components of the overall customer experience.

Therefore, Olist needs to understand:

- Which factors are associated with repeat purchases?
- Which factors have the strongest relationship with customer satisfaction?
- Where do the largest customer experience problems occur?
- Which sellers perform best within specific product categories?
- Which actions should Olist prioritize to improve the marketplace?

### Main Business Question

> **How can Olist improve its customer experience and, through the targeted selection of high-performing sellers, increase long-term marketplace success?**

---

## 3. Research Questions

To answer the main business question, the project is divided into several analytical areas.

### 3.1 Customer Retention

**Which factors are associated with repeat purchases within the observed Olist customer base?**

We will investigate factors such as:

- Order value
- Product category
- Delivery time
- Delivery delays
- Review score
- Freight cost
- Customer location
- Number of previous orders

A particular focus will be placed on the differences between customers with one observed order and customers with multiple observed orders.

> **Important:** A customer with only one observed order is not automatically considered a true one-time customer. The analysis only shows that no additional order is observed within the available Olist dataset.

---

### 3.2 Customer Experience

**Which factors have the strongest relationship with customer satisfaction?**

A central focus will be the relationship between:

**Delivery Performance → Customer Experience → Review Score**

The analysis will include factors such as:

- Actual delivery time
- Estimated delivery time
- Delivery delays
- Freight value
- Product category
- Seller
- Customer region
- Order value

The objective is to identify the factors that are most strongly associated with positive or negative customer experiences.

---

### 3.3 Problem Identification

**Which regions, product categories, and sellers show the largest customer experience problems?**

The analysis will investigate:

- Which sellers have high delivery delay rates?
- Which product categories receive lower review scores?
- Which regions have particularly long delivery times?
- Where are freight costs unusually high?
- Which combinations of seller, product, and region perform poorly?

The goal is to identify specific and actionable problem areas rather than relying only on overall averages.

---

### 3.4 Seller Performance

**Which sellers are the strongest partners for Olist within each product category?**

The best seller will not be determined by revenue alone.

Instead, sellers will be evaluated using several dimensions, including:

- Average review score
- On-time delivery rate
- Average delivery time
- Revenue
- Number of orders
- Freight cost
- Reliability

A **Seller Performance Score** will be developed to combine relevant performance indicators.

Seller performance will be evaluated within product categories because a seller may perform very well in one category but less effectively in another.

The number of orders will also be considered to avoid overvaluing sellers with very small sample sizes.

---

### 3.5 Predictive Analytics

**Can negative customer experiences be predicted before they occur?**

Based on the previous analysis, we will investigate whether machine learning can be used to predict the risk of a negative customer experience.

One possible definition is:

**Negative Customer Experience = Review Score <= 2**

Potential predictive features include:

- Delivery time
- Delivery delay
- Freight value
- Order value
- Product category
- Seller
- Customer region
- Product characteristics
- Payment information

The objective is to determine whether problematic orders can be identified before the customer submits a negative review.

---

# 4. Project Approach

The project follows an end-to-end data analytics process:

```text
Raw Data
   ↓
Data Understanding
   ↓
Data Quality Assessment
   ↓
Data Cleaning
   ↓
Data Modeling
   ↓
Exploratory Data Analysis
   ↓
Customer Analysis
   ↓
Delivery & Customer Experience Analysis
   ↓
Seller Performance Analysis
   ↓
Feature Engineering
   ↓
Machine Learning
   ↓
Business Recommendations
   ↓
Power BI Dashboard / Streamlit Application




Part David:

## Customer, Order & Review Data Processing

My contribution focused on the preparation and analysis of the **customer, order and review datasets**. The goal was to create a reliable analytical foundation for investigating customer satisfaction in relation to the order and delivery experience.

### 1. Data Quality & Structural Validation

The three datasets were initially assessed for:

- data types and dataset structure
- missing values
- duplicate records
- primary and foreign key integrity
- timestamp consistency
- completeness of review information

The relational structure between the datasets was preserved throughout the preprocessing:

**Customer → Order → Review**

`customer_id` was used to connect customers with their orders, while `order_id` connected orders with their corresponding reviews.

---

### 2. Customer Data Preparation

The customer dataset required comparatively little preprocessing. The main focus was on preserving the customer identifiers and their relational structure.

Both `customer_id` and `customer_unique_id` were retained because they serve different analytical purposes:

- `customer_id` identifies the customer record associated with an order.
- `customer_unique_id` allows customer-level behavior to be analyzed across multiple orders.

This distinction was important when switching between order-level and customer-level analyses.

---

### 3. Order Lifecycle Preprocessing

The order dataset contains several timestamps describing the order lifecycle:

**Purchase → Approval → Carrier Handover → Customer Delivery**

The timestamp columns were converted into appropriate datetime formats to enable time-based analysis and delivery-related calculations.

Missing timestamps were **not automatically imputed or removed**, as missingness can indicate an incomplete order lifecycle rather than a technical data error.

The order data was therefore validated for chronological consistency, and potentially problematic records were identified through validation checks. Records were only excluded from specific analyses when the required timestamps were unavailable.

This approach prevented artificial values from distorting operational metrics such as delivery duration.

---

### 4. Review Data & Text Preparation

Review data was separated into two analytical components:

- **Structured feedback:** `review_score`
- **Unstructured feedback:** `review_comment_title` and `review_comment_message`

The numerical review score was retained as the primary quantitative measure of customer satisfaction.

Missing review comments were not interpreted as missing reviews, since customers can provide a score without writing a comment. Text-based analysis was therefore restricted to reviews containing usable written feedback.

The available Portuguese review comments were translated into English while retaining the original review information for traceability.

---

### 5. Review Comment Classification

To complement the numerical review scores, the written comments were analyzed to identify recurring customer-reported issues.

The process consisted of:

1. **Identifying relevant comments** containing usable customer feedback.
2. **Defining analytical categories** based on recurring themes in the comments.
3. **Mapping comments to categories** according to their content.
4. **Creating a keyword dictionary** linking relevant expressions to the respective categories.
5. **Validating the classification** using manually reviewed examples.
6. **Refining the dictionary** based on misclassifications, missing keywords and ambiguous expressions.
7. **Applying the validated classification** to the relevant review population.

This transformed unstructured customer feedback into structured analytical variables that could be combined with review scores and order-related information.

---

### 6. Integrated Customer Satisfaction Analysis

After preprocessing and validation, the customer, order and review datasets were integrated to analyze customer satisfaction in the context of the underlying order experience.

The analysis combined:

- customer behavior
- order characteristics
- delivery performance
- numerical review scores
- customer-reported issues from review comments

This enabled the analysis to move beyond simply measuring **how satisfied customers were** and investigate **which operational and customer-reported patterns were associated with different satisfaction levels**.

The analysis was interpreted as **associational rather than causal**, since the Olist dataset is observational.

---

### 7. Key Data Decisions

Several preprocessing decisions were made to avoid unnecessary data loss or artificial information:

| Data Issue | Decision | Reason |
|---|---|---|
| Missing order timestamps | Preserved | Missingness can represent an incomplete order lifecycle |
| Missing review comments | Preserved | A customer can submit a score without written feedback |
| Different customer IDs | Both retained | Required for order-level and customer-level analysis |
| Invalid/inconsistent timestamps | Flagged and validated | Prevents distorted delivery metrics |
| Review text | Analyzed separately | Text is only available for a subset of reviews |
| Text categories | Validated before full application | Reduces classification errors |

---

### 8. Limitations

The analysis has several limitations that need to be considered when interpreting the results:

- Not every customer submits a review, creating potential review selection bias.
- A large share of reviews contains a score without written comments, limiting the scope of text analysis.
- Some orders have incomplete lifecycle timestamps, restricting delivery-related calculations.
- Keyword-based comment classification may not fully capture context, ambiguity or previously unseen expressions.
- The dataset is observational; identified relationships should therefore not be interpreted as causal effects.