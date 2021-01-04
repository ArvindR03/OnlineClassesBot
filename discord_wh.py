import requests
from discord_webhooks import DiscordWebhooks

def post_to_server(message):
    whurl = 'discord webhook url here'
    Message = {
        'content': 'na'
    }
    Message['content'] = str(message)
    requests.post(whurl, data=Message)

def post_report_server(classname, entered, timeoutquery):
    whurl = 'discord webhook url here'
    webhook = DiscordWebhooks(whurl)
    webhook.set_content(title='WA Report', description='Hello, here is the current Teams Bot status:')
    webhook.add_field(name='Class', value=classname)
    webhook.add_field(name='Entered', value=str(entered))
    webhook.add_field(name='Timeout', value=str(timeoutquery))
    webhook.send()