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