import json
import requests
import os

API_KEY = os.environ['api_key']
STATUS_PAGE_URL = os.environ['status_page_url']


def lambda_handler(event, context):
    # TODO implement

    url = "https://api.uptimerobot.com/v2/getMonitors"

    querystring = {"format": "json",
                   "api_key": API_KEY}

    response = requests.post(url, params=querystring)

    print(response.json())
    body_text = ""
    up_monitors = 0
    down_monitors = 0
    down_monitor_objects = list()
    all_monitors = len(response.json().get('monitors'))
    for monitor in response.json().get('monitors'):
        name = monitor.get('friendly_name')
        url = monitor.get('url')
        status = monitor.get('status')
        if 0 <= status <= 2:
            up_monitors += 1
        elif 8 <= status <= 9:
            down_monitors += 1
            down_monitor_objects.append(monitor.copy())

    if down_monitors == 0:
        title = "All Good"
        style = "is-success"
    else:
        title = "Uh Oh"
        style = "is-danger"

    message = f'{up_monitors}/{all_monitors} services are showing as online.' \
              f' <a href="{STATUS_PAGE_URL}">Click for more details</a>'

    if down_monitors > 0:
        message += '<br><br>' \
                   'Here are the services showing as offline:'
        for monitor in down_monitor_objects:
            message += f'<br><a href="{monitor.get("url")}">{monitor.get("friendly_name")}</a>'

    returnBody = {
        "title": title,
        "message": message,
        "style": style
    }
    returnHeaders = {
        'Access-Control-Allow-Origin': '*'
    }

    print(returnBody)
    return {
        'statusCode': 200,
        'body': json.dumps(returnBody),
        'headers': returnHeaders
    }


lambda_handler(None, None)
