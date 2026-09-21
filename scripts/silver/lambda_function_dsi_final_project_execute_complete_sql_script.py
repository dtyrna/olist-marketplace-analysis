import os
import boto3
import time
import re

# AWS Clients initialisieren
athena_client = boto3.client('athena')
s3_client = boto3.client('s3')

def clean_sql_script(script_content):
    """Delete SQL comments to avoid mistakes in splitting."""
    content = re.sub(re.compile(r"--.*?\n"), "", script_content)
    content = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", content)
    return content

def get_script_from_s3(bucket, key):
    """Load sql queries from script as String."""
    try:
        print(f"Load SQL-Script from s3: s3://{bucket}/{key}")
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        raise Exception(f"Error in Loading file from s3: {str(e)}")

def execute_athena_query(sql_query, database, s3_output):
    """Execute every single query from script an wait for result."""
    response = athena_client.start_query_execution(
        QueryString=sql_query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': s3_output}
    )
    query_id = response['QueryExecutionId']
    
    while True:
        execution = athena_client.get_query_execution(QueryExecutionId=query_id)
        status = execution['QueryExecution']['Status']['State']
        
        if status == 'SUCCEEDED':
            print(f"Query successful. (Query ID: {query_id})")
            break
        elif status in ['FAILED', 'CANCELLED']:
            reason = execution['QueryExecution']['Status'].get('StateChangeReason', 'Unknown Error')
            raise Exception(f"❌ Query failed {query_id} ! Reason: {reason}")
            
        time.sleep(2)

def lambda_handler(event, context):
    # Konfiguration aus Umgebungsvariablen laden
    database = os.environ['ATHENA_DATABASE']
    s3_output = os.environ['S3_OUTPUT']
    script_bucket = os.environ['SCRIPT_S3_BUCKET']
    script_key = os.environ['SCRIPT_S3_KEY']
    
    print("Lambda-Script started.")
    
    # 1. Call SQL-Script from S3
    try:
        raw_sql_script = get_script_from_s3(script_bucket, script_key)
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
    
    # 2. Clean script and split ";"
    clean_content = clean_sql_script(raw_sql_script)

    try:
            clean_content = clean_content.format(
                DB_NAME=database,
                BUCKET_NAME=script_bucket
            )
            print("Environment variables loaded into SQL-Script.")
    except KeyError as e:
            print(f"Warning when replacing: placeholder {e} not been found in SQL Script, Code continues...")

    statements = [s.strip() for s in clean_content.split(';') if s.strip()]
    
    print(f"Found SQL-queries in s3-script: {len(statements)}")
    
    # 3. Execute queries one after another in Athena
    for i, statement in enumerate(statements, 1):
        print(f"[{i}/{len(statements)}] Execute: {statement[:80]}...")
        try:
            execute_athena_query(statement, database, s3_output)
        except Exception as e:
            print(f"Termination due to an error: {e}")
            return {
                'statusCode': 500,
                'body': f"Error with query {i}: {str(e)}"
            }
            
    print("All commands from s3 succeeded!")
    return {
        'statusCode': 200,
        'body': 'SQL-Script ran completely.'
    }
