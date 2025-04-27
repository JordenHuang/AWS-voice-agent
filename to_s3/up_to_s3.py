#輸出aws語音轉文字的資料轉乘json存入s3中
# 這段程式碼是用來將 AWS 語音轉文字的結果轉換成 JSON 格式，並存入 S3 中。它使用了 boto3 庫來與 AWS 服務進行互動。

import json
import boto3
import os
import logging
from datetime import datetime, timedelta
logger = logging.getLogger()
logger.setLevel("INFO")
client  = boto3.client('s3')
def upload_receipt_to_s3(bucket_name, key, receipt_content):
    """Helper function to upload receipt to S3"""
    
    try:
        client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=receipt_content
        )
    except Exception as e:
        logger.error(f"Failed to upload receipt to S3: {str(e)}")
        raise

def lambda_handler(event, context):
    """
    Main Lambda handler function
    Parameters:
        event: Dict containing the Lambda function event data
        context: Lambda runtime context
    Returns:
        Dict containing status message
    """
    try:
        # Parse the input event"
        role = event.get("role",'assistant')
        content = event.get("content",[])
        print(role)
        print(content)
        # if not isinstance(content, list):
        #     raise ValueError("'content' must be a list")
        
        # Access environment variables
        bucket_name = 'old-text'
        if not bucket_name:
            raise ValueError("Missing required environment variable RECEIPT_BUCKET")
        # combined_text = "\n".join([item.get("text", "") for item in content])
        # Create the receipt content and key destination
        receipt_content = (
            f"role: {role}\n"
            f"content: ${content}"
            
        )
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        key = f"receipts/{timestamp}.txt"

        # Upload the receipt to S3
        upload_receipt_to_s3(bucket_name, key, receipt_content)

        logger.info(f"Successfully processed order {role} and stored receipt in S3 bucket {bucket_name}")
        
        # return {
        #     "statusCode": 200,
        #     "message": "Receipt processed successfully"
        # }

    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        raise