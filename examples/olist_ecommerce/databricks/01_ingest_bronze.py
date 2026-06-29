# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Ingest Olist CSVs To Bronze
# MAGIC
# MAGIC Upload Olist CSV files to a Unity Catalog Volume, then run this notebook.
# MAGIC It creates one bronze Delta table per CSV file.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "olist_ecommerce")
dbutils.widgets.text("raw_volume", "/Volumes/workspace/olist_ecommerce/olist_raw")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
raw_volume = dbutils.widgets.get("raw_volume").rstrip("/")

if "{{" in catalog or "{{" in schema or "{{" in raw_volume:
    raise ValueError("Replace widget placeholders before running this notebook.")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

print(f"Catalog/schema: {catalog}.{schema}")
print(f"Raw volume: {raw_volume}")

# COMMAND ----------

csv_to_table = {
    "olist_customers_dataset.csv": "bronze_olist_customers",
    "olist_geolocation_dataset.csv": "bronze_olist_geolocation",
    "olist_order_items_dataset.csv": "bronze_olist_order_items",
    "olist_order_payments_dataset.csv": "bronze_olist_order_payments",
    "olist_order_reviews_dataset.csv": "bronze_olist_order_reviews",
    "olist_orders_dataset.csv": "bronze_olist_orders",
    "olist_products_dataset.csv": "bronze_olist_products",
    "olist_sellers_dataset.csv": "bronze_olist_sellers",
    "product_category_name_translation.csv": "bronze_product_category_translation",
}

for csv_name, table_name in csv_to_table.items():
    path = f"{raw_volume}/{csv_name}"
    full_table = f"{catalog}.{schema}.{table_name}"

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .option("multiLine", True)
        .option("escape", '"')
        .csv(path)
    )

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", True)
        .saveAsTable(full_table)
    )

    print(f"Wrote {full_table}: {df.count():,} rows")

# COMMAND ----------

display(spark.sql(f"""
SELECT table_name
FROM {catalog}.information_schema.tables
WHERE table_schema = '{schema}'
  AND table_name LIKE 'bronze_olist_%'
ORDER BY table_name
"""))

