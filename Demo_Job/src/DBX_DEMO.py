# Databricks notebook source
import os

# COMMAND ----------

def main():
    secret_val = dbutils.secrets.get('dev', 'data')
    df = spark.createDataFrame([(1, 'yajith', 100), (2, 'vishwa', 200)], schema='id int, name string, mark int')
    display(df)

# COMMAND ----------

if os.getenv('RUN_MODE', 'dbx') == 'dbx':
    main()