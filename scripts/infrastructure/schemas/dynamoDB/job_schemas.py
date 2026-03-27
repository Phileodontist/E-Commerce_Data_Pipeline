ingestion_job = {
    "PK": "JOB#INGESTION",
    "SK": "META",
    "type": "job",
    "description": "Converts csv files to parquet format, basic parsing, and captures ingestion metadata",
    "is_active": True
}

bronzetransformation_job = {
    "PK": "JOB#BRONZETRANSFORM",
    "SK": "META",
    "type": "job",
    "description": "Applies basic transformations (type casting, renaming columns, etc), detects schema drift.)",
    "is_active": True
}

silvertransformation_job = {
    "PK": "JOB#SILVERTRANSFORM",
    "SK": "META",
    "type": "job",
    "description": "Conforms data into a normalized schema & applies business logic",
    "is_active": True
}

goldtransformation_job = {
    "PK": "JOB#GOLDTRANSFORM",
    "SK": "META",
    "type": "job",
    "description": "Conforms data into a dimensional schema",
    "is_active": True
}

copy2redshift_job = {
    "PK": "JOB#COPYTOREDSHIFT",
    "SK": "META",
    "type": "job",
    "description": "Migrates data into Redshift",
    "is_active": True
}

job_schemas = [ingestion_job, bronzetransformation_job, silvertransformation_job, goldtransformation_job, copy2redshift_job]