import json
import boto3
from urllib.parse import parse_qs



def get_global_summary(covid_summary):
    global_data = covid_summary['Item']['Global_information']
    answer = 'Right now there are {:,} new confirmed cases, {:,} total confirmed, {:,} new deaths, {:,} total deaths and {:,} total recovered.'.format(
        global_data['NewConfirmed'],
        global_data['TotalConfirmed'],
        global_data['NewDeaths'],
        global_data['TotalDeaths' ],
        global_data['TotalRecovered'])
    return answer

def get_data_by_country(covid_summary, search):
    countries = covid_summary['Item']['Countries']
    try:
        country = next(c for c in countries if c['Country'].lower() == search)
    except:
        return 'Try again, we do not have what you are looking for'

    answer = 'In {} there are {:,} new confirmed cases, {:,} total confirmed, {:,} new deaths, {:,} total deaths and {:,} total recovered.'.format(
        country['Country'],
        country['NewConfirmed'],
        country['TotalConfirmed'],
        country['NewDeaths'],
        country['TotalDeaths' ],
        country['TotalRecovered'])

    return answer

def get_connection_database():
    dynamodb = boto3.resource("dynamodb")
    tables = dynamodb.Table('summary')
    covid_summary = tables.get_item(Key = {'Date' : 'latest'})
    return covid_summary

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    covid_summary = get_connection_database()
    message_from_slack = parse_qs(event["body"])
    search = str(message_from_slack['text'][0])
    search = search.lower()
    if search == 'global':
        info = get_global_summary(covid_summary)
    else:
        info = get_data_by_country(covid_summary, search)

    return respond(None, {
       'response_type': 'in_channel',
        'text': info
    })
