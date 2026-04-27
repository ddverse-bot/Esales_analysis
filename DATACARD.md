## 1. Original Dataset Source

**Dataset Name:** Brazilian E-Commerce Public Dataset by Olist  
**Source Platform:** Kaggle  
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

**Provider:** Olist

**Description:**  
This dataset contains real commercial order data from a Brazilian e-commerce marketplace, including information on orders, customers, products, sellers, payments, freight charges, and delivery timelines.

**Scale:**  
- ~100,000 orders  
- Multiple relational tables  
- Real transactions from 2016 to 2018

## 2. Raw Dataset Files Available

The Brazilian E-Commerce Public Dataset by Olist contains the following raw files:

| File Name | Description |
|-----------|-------------|
| `olist_orders_dataset.csv` | Main order records, timestamps, status |
| `olist_order_items_dataset.csv` | Products included in each order |
| `olist_order_payments_dataset.csv` | Payment type, installments, amount |
| `olist_order_reviews_dataset.csv` | Customer review scores and comments |
| `olist_products_dataset.csv` | Product metadata, dimensions, weight |
| `olist_customers_dataset.csv` | Customer location data |
| `olist_sellers_dataset.csv` | Seller location data |
| `olist_geolocation_dataset.csv` | Geographic zip code coordinates |
| `product_category_name_translation.csv` | Portuguese to English category mapping |

## 3. Files Used in This Project

The following files were directly used for preprocessing and model development:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_products_dataset.csv`
- `olist_customers_dataset.csv`
- `product_category_name_translation.csv`

## 4. Raw Dataset Schema Overview

The Olist dataset is composed of multiple relational tables connected through shared keys such as `order_id`, `customer_id`, `product_id`, and `seller_id`.

| File Name | Primary Key / Important Keys | Key Columns / Attributes | Purpose |
|-----------|------------------------------|--------------------------|---------|
| `olist_orders_dataset.csv` | `order_id`, `customer_id` | order_status, order_purchase_timestamp, order_approved_at, delivered dates, estimated delivery date | Core order lifecycle data |
| `olist_order_items_dataset.csv` | `order_id`, `order_item_id`, `product_id`, `seller_id` | shipping_limit_date, price, freight_value | Order line items and logistics cost |
| `olist_order_payments_dataset.csv` | `order_id` | payment_type, payment_installments, payment_value | Payment behavior and transaction value |
| `olist_order_reviews_dataset.csv` | `review_id`, `order_id` | review_score, review_comment_title, review_comment_message | Customer satisfaction data |
| `olist_products_dataset.csv` | `product_id` | product_category_name, product_name_length, product_description_length, product_photos_qty, dimensions, weight | Product metadata |
| `olist_customers_dataset.csv` | `customer_id`, `customer_unique_id` | customer_zip_code_prefix, customer_city, customer_state | Customer geography |
| `olist_sellers_dataset.csv` | `seller_id` | seller_zip_code_prefix, seller_city, seller_state | Seller geography |
| `olist_geolocation_dataset.csv` | zip prefix (non-unique) | latitude, longitude, city, state | Geographic coordinates |
| `product_category_name_translation.csv` | `product_category_name` | product_category_name_english | Category translation mapping |

## 5. Table Relationships


This diagram represents the relational structure of the Olist Brazilian E-Commerce dataset used in our project for delivery delay prediction.

<img width="930" height="605" alt="image" src="https://github.com/user-attachments/assets/4279720c-c8a7-4804-95e0-ee5a739952b1" />

# Modified Dataset Card: E-Sales Delivery Delay Prediction

## 1. Objective

The original Olist dataset was distributed across multiple normalized relational tables.  
It was transformed into a clean, feature-rich tabular dataset suitable for machine learning classification.

Goal:

Predict whether a customer order will be delivered later than the promised estimated delivery date.

---

## 2. Source Tables Integrated

The following raw files were merged:

| File Name | Role |
|-----------|------|
| `olist_orders_dataset.csv` | Core order timestamps and status |
| `olist_order_items_dataset.csv` | Product item price and freight |
| `olist_order_payments_dataset.csv` | Installments and payment amount |
| `olist_products_dataset.csv` | Product dimensions and weight |
| `olist_customers_dataset.csv` | Customer metadata |
| `product_category_name_translation.csv` | Category names in English |

---

## 3. Join Keys Used

| Key | Purpose |
|-----|---------|
| `order_id` | Orders ↔ Items ↔ Payments |
| `customer_id` | Orders ↔ Customers |
| `product_id` | Items ↔ Products |
| `product_category_name` | Products ↔ Translation |

---

## 4. Target Variable Created

```python
delivery_delay = 1 if delivered_customer_date > estimated_delivery_date
delivery_delay = 0 otherwise

```
## 5. Cleaning Performed

    -Converted timestamps into datetime format
    -Removed rows missing delivery timestamps
    -Median imputation for missing product dimensions
    -Removed duplicate rows
    -Removed zero-price records
    -Removed negative freight values
    -Removed remaining null rows

# 6. Feature Schema  
## E-Sales Delivery Delay Prediction Dataset

The final working dataset used for model training contains **15 total columns**:

- **14 Input Features** (predictors)
- **1 Target Label**

---

# Input Features Used for Machine Learning (14)

| Sl. No. | Feature Name | Type | Description |
|--------|--------------|------|-------------|
| 1 | `price` | Numeric | Selling price of the product |
| 2 | `freight_value` | Numeric | Shipping / freight charge |
| 3 | `product_weight_g` | Numeric | Product weight in grams |
| 4 | `product_length_cm` | Numeric | Product length |
| 5 | `product_width_cm` | Numeric | Product width |
| 6 | `purchase_hour` | Numeric | Hour when order was placed |
| 7 | `purchase_dayofweek` | Numeric | Day of week of purchase |
| 8 | `estimated_delivery_days` | Numeric | Promised delivery duration |
| 9 | `payment_installments` | Numeric | Number of payment installments |
| 10 | `approval_delay_hours` | Numeric | Time taken for payment/order approval |
| 11 | `order_total` | Numeric | Total order payment amount |
| 12 | `items_per_order` | Numeric | Number of products in same order |
| 13 | `freight_price_ratio` | Engineered | Freight cost relative to product price |
| 14 | `slow_approval` | Engineered | Flag for approval delay > 24 hours |

---

#  Target Variable (1)

| Feature Name | Type | Description |
|-------------|------|-------------|
| `delivery_delay` | Binary | 1 = Late Delivery, 0 = On-Time Delivery |

---

#  Total Dataset Structure

| Category | Count |
|---------|------|
| Base Features | 12 |
| Engineered Features | 2 |
| Target Label | 1 |
| **Total Columns** | **15** |

---

#  Why These Features Matter

The selected variables capture multiple real-world dimensions:

###  Financial Signals
- `price`
- `freight_value`
- `order_total`

###  Product Logistics
- `product_weight_g`
- `product_length_cm`
- `product_width_cm`

###  Time Behavior
- `purchase_hour`
- `purchase_dayofweek`
- `estimated_delivery_days`
- `approval_delay_hours`

###  Order Complexity
- `items_per_order`

###  Engineered Risk Signals
- `freight_price_ratio`
- `slow_approval`

---

#  Summary

The final feature set was carefully designed to combine:

- transactional information  
- logistics constraints  
- customer ordering patterns  
- payment processing behavior  
- engineered business intelligence signals  

This creates a balanced predictive dataset for delivery delay classification.
The modified dataset is not simply a cleaned version of Olist data. It is a purpose-built predictive intelligence dataset engineered from raw commerce records to support delivery risk forecasting through machine learning.

#  Modified Dataset Relationship Diagram  
## E-Sales Delivery Delay Prediction Dataset (Final Engineered Schema)

This diagram shows how the **final processed features** are derived from the original Olist tables and transformed into the machine learning dataset.

<img width="8191" height="1335" alt="Olist E-Sales Dataset-2026-04-27-171913" src="https://github.com/user-attachments/assets/ce475240-68ff-4441-8e26-05351a3d722c" />

K --> N[Ensemble Model]
K --> O[Streamlit Dashboard]
