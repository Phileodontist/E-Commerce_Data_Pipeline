from pyspark.sql.types import *

# Bronze Layer Schema
bronze_schema = StructType([
    StructField("event_time", StringType()),
    StructField("event_type", StringType()),
    StructField("product_id", StringType()),
    StructField("category_id", StringType()),
    StructField("category_code", StringType()),
    StructField("brand", StringType()),
    StructField("price", StringType()),
    StructField("user_id", StringType()),
    StructField("user_session", StringType()),
    StructField("name", StringType()),
    StructField("username", StringType()),
    StructField("email", StringType()),
    StructField("address", StringType()),
    StructField("city", StringType()),
    StructField("country", StringType()),
    StructField("state_code", StringType()),
    StructField("zip_code", StringType()),
    StructField("sex", StringType()),
    StructField("product_name", StringType()),
    StructField("product_description", StringType())
])

# Silver Layer Schema
product_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
    StructField("brand", StringType()),    
    StructField("product_description", StringType()),
    StructField("primary_category", StringType()),
    StructField("secondary_category", StringType()),
    StructField("tertiary_category", StringType()),
    StructField("is_current", BooleanType()),
    StructField("effective_start_ts", TimestampType()),
    StructField("effective_end_ts", TimestampType()),
    StructField("hash_diff", StringType())
])

event_schema = StructType([
    StructField("event_time", TimestampType()),
    StructField("event_type", StringType()),
    StructField("product_id", IntegerType()),
    StructField("price", FloatType()),    
    StructField("user_id", LongType()),
    StructField("user_session", StringType())
])

user_schema = StructType([
    StructField("user_id", LongType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),    
    StructField("user_name", StringType()),
    StructField("email", StringType()),
    StructField("sex", StringType()),    
    StructField("address", StringType()),
    StructField("country", StringType()),
    StructField("state_code", StringType()),
    StructField("city", StringType()),    
    StructField("zip_code", StringType()),
    StructField("is_current", BooleanType()),
    StructField("effective_start_ts", TimestampType()),
    StructField("effective_end_ts", TimestampType()),
    StructField("hash_diff", StringType())    
])

# Gold Layer Schema
fact_view_schema = StructType([
    StructField("event_id", TimestampType()),
    StructField("user_id", LongType()),    
    StructField("product_id", IntegerType()),
    StructField("date_id", IntegerType()),
    StructField("year", StringType()),
    StructField("month", StringType()),
    StructField("day_of_week", StringType()),
    StructField("primary_category", StringType()),
    StructField("country", StringType()),
    StructField("state", StringType()),
    StructField("city", StringType()),
    StructField("event_type", StringType()),  
    StructField("user_session", StringType()),
    StructField("price_at_event", FloatType())
])

fact_engagement_schema = StructType([
    StructField("event_id", TimestampType()),
    StructField("user_id", LongType()),    
    StructField("product_id", IntegerType()),
    StructField("date_id", IntegerType()),
    StructField("year", StringType()),
    StructField("month", StringType()),
    StructField("day_of_week", StringType()),
    StructField("primary_category", StringType()),
    StructField("country", StringType()),
    StructField("state", StringType()),
    StructField("city", StringType()),
    StructField("event_type", StringType()),  
    StructField("user_session", StringType()),
    StructField("price_at_event", FloatType())
])

dim_product_schema = StructType([
    StructField("id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("name", StringType()),
    StructField("brand", StringType()),    
    StructField("description", StringType()),
    StructField("primary_category", StringType()),
    StructField("secondary_category", StringType()),
    StructField("tertiary_category", StringType()),
    StructField("is_current", BooleanType()),
    StructField("effective_start_ts", TimestampType()),
    StructField("effective_end_ts", TimestampType()),
    StructField("hash_diff", StringType())
])

dim_user_schema = StructType([
    StructField("id", LongType()),
    StructField("user_id", LongType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),    
    StructField("user_name", StringType()),
    StructField("sex", StringType()),    
    StructField("email", StringType()),
    StructField("address", StringType()),
    StructField("city", StringType()),
    StructField("country", StringType()),
    StructField("state_code", StringType()),
    StructField("zip_code", StringType()),
    StructField("is_current", BooleanType()),
    StructField("effective_start_ts", TimestampType()),
    StructField("effective_end_ts", TimestampType()),
    StructField("hash_diff", StringType())    
])

dim_date_schema = StructType([
    StructField("id", IntegerType()),
    StructField("date", DateType()),    
    StructField("day_number_in_month", IntegerType()),
    StructField("day_number_in_year", IntegerType()),
    StructField("day_of_week", StringType()),    
    StructField("calendar_month", StringType()),
    StructField("calendar_month_number", IntegerType()),
    StructField("calendar_year_month", StringType()),
    StructField("calendar_quarter", StringType()),
    StructField("calendar_year", StringType())
])

bronze_schemas = {"bronze": bronze_schema}
silver_schemas = {"product": product_schema, "event": event_schema, "user": user_schema}
gold_schemas = {"fact_view": fact_view_schema, "fact_engagement": fact_engagement_schema,
                "dim_product": dim_product_schema, "dim_user": dim_user_schema, "dim_date": dim_date_schema}