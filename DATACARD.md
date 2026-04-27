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



