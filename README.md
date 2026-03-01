# E-Commerce Data Pipeline
An End-to-End data pipeline that ingests raw event logs from an e-commerce website, organizes them into a medallion‑layer data lake, and then models them into a dimensional warehouse by progressively refining structure, quality, and business meaning.

## Synopsis
This project was intended to showcase a production ready End-to-End pipeline that is maintainable, interopable, and scalable by leveraging cloud services from AWS such as Step Functions, DynamoDB, Glue, Redshift, S3.

<!--#### Developer's Note-->

## Data & Data Models
### Datasets and API's
* [E-Commerce Dataset](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/data)

### Database Schemas
* [Bronze Schema](https://github.com/Phileodontist/E-Commerce_Data_Pipeline/blob/master/images/bronze_schema.png)
* [Silver Schema](https://github.com/Phileodontist/E-Commerce_Data_Pipeline/blob/master/images/silver_schema.png)
* [Gold Schema](https://github.com/Phileodontist/E-Commerce_Data_Pipeline/blob/master/images/gold_schema.png)
* [Job Metadata Schema](https://github.com/Phileodontist/E-Commerce_Data_Pipeline/blob/master/images/job_metadata_schema.png)

## Pipeline Architecture Diagram

<!--[[Specification Write Up]](https://github.com/Phileodontist/PoliceShootingsDashboard/blob/master/EMR/Police_Shootings_Dashboard_Specification.ipynb)-->
![Police Shootings ETL Pipeline (EMR)](https://github.com/Phileodontist/E-Commerce_Data_Pipeline/blob/master/images/Data_Architecture_Diagram.png)
