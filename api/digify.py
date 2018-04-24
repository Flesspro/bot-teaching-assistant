import json
import requests
from requests.auth import HTTPBasicAuth

import urllib.request, urllib.parse, urllib.error
import config
import re
import systemtools
from sender import sender
import re, sys
from datetime import datetime

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def create_link ():
    """
    Creates a secure link to share with students

    """
    data = {'FileSettings':"""{"Permission":"Public","Watermark":"True","Watermark_text":"VICTOR ROGULENKO","Watermark_size":"Small","Watermark_color":"Red","Expiry":"Fixeddate","ExpiryDate": "2018-03-23T12:18:00.000+03:00"}"""}
    # Digify File Modal https://digify.com/s/J9i2lg
    # API Overview https://help.digify.com/digify-file-api-overview

    url = 'https://svc.digify.com/v1/file/upload'

    auth = HTTPBasicAuth(config.api_digify_app_id, config.api_digify_app_secret)
    files = {'file': ('test2.pdf', open('test.pdf', 'rb'), 'application/pdf')}

    req = requests.post(
            url = url,
            auth = auth,
            data = data,
            files = files,
            headers = {
                'Host': 'svc.digify.com'
                }
            )

    pretty_print_POST (req.request)
    return (req)

def create_link_url (file_addr):
    """
    Creates a secure link to share with students

    """
    data = {
      'FileName': "secret.pdf",
      'URL': file_addr,
      'Permission': "Restrict",
      'Recipients': "[{\"email\":\"rogulenko@gmail.com\"}]",
      'Watermark': "True",
      'Watermark_text': "Confidential",
      'Expiry': "Fixeddate",
      'ExpiryDate': "2018-05-01T12:00:00.000Z"
    }
    url = 'https://svc.digify.com/v1/file/share'
    auth = HTTPBasicAuth(config.api_digify_app_id, config.api_digify_app_secret)
    resp = requests.post(
            url,
            auth = auth,
            data = data,
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'svc.digify.com'
                }
            )

    return (resp)
