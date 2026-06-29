# Dataset Notes

## Public Source

Dataset: Brazilian E-Commerce Public Dataset by Olist  
Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

This is a public marketplace dataset containing Brazilian e-commerce orders from 2016 to 2018. It is commonly used for analytics, BI, and machine-learning portfolio projects.

## Expected CSV Files

The Kaggle download usually contains:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

## Publication Notes

- Do not commit raw downloaded data into this repository.
- Keep raw files in a Databricks Volume or local ignored folder.
- Attribute Olist and the Kaggle dataset page in the GitHub README and LinkedIn post.
- Re-check the Kaggle license before publishing screenshots, transformed extracts, or packaged sample files.

## Why This Dataset Fits Genie

The dataset has a strong natural-language analytics shape:

- Time: purchase date, delivery date, estimated delivery date
- Measures: order value, freight value, payment value, item count, review score
- Dimensions: product category, customer geography, seller geography, order status
- Diagnostics: late delivery, review score, delivery duration, freight concentration

