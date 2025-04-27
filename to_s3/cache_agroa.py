import boto3
import json
import uuid

# 初始化 Bedrock Runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

def lambda_handler(event, context):
    try:
        # 從 Agora 傳進來的 event body 取出文字
        body = json.loads(event['body'])
        input_text = body['inputText']

        # 呼叫 Bedrock Flow
        response = bedrock_runtime.invoke_flow(
            flowId='1HG9UISL35',
            flowVersion='1',  # 預設是1
            input={
                "role":""
                "content": input_text
            },
            sessionId=str(uuid.uuid4())  # 建議每次用新的 Session
        )

        # Flow回傳的結果
        output = response['output']

        return {
            'statusCode': 200,
            'body': json.dumps({
                'text': "+++"+output  # 回傳 Flow 回應給前端
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }