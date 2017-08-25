import logging
import json
import decimal
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dynamodb = boto3.resource('dynamodb')
logger.info('environ: {}'.format(os.environ))
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get(event, context):
    logger.info('got event: {}'.format(event))
    resource_id = event['pathParameters']['resourceId']
    dynamo_item = table.get_item(
        Key={
            'id': resource_id
        }
    )
    response_body = json.dumps(dynamo_item['Item'], cls=DecimalEncoder)
    logger.info(response_body)
    json_response = {
            'statusCode': 200,
            'body': response_body
           }
    return json_response
