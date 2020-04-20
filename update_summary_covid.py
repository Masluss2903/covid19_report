import json
import requests
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('summary')
    covid_summary = requests.get('https://api.covid19api.com/summary').json()
    covid_summary['Global_information'] = covid_summary['Global']
    del covid_summary['Global']
    table.put_item(Item = covid_summary)
    print('success')
    Date = 'latest'
    response = table.update_item(
                                Key = {'Date': Date},
                                UpdateExpression = 'set Global_information = :g, Countries = :c',
                                ExpressionAttributeValues = {
                                                            ':g': covid_summary['Global_information'],
                                                            ':c': covid_summary['Countries']},
                                ReturnValues = "UPDATED_NEW" )
    print('Update item')
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
