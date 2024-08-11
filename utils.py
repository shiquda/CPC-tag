import base64
import urllib.parse
import json
import re


def base64_encode(text):
    return base64.encodebytes(text.encode()).decode()


def base64_decode(text):
    return base64.decodebytes(text.encode()).decode()

def parse_js(text):
    text = urllib.parse.unquote(text)
    # text = re.sub(r"(?<=\{|,)\s*'([^']+)'\s*:", r'"\1":', text)

    json_object = json.loads(text)
    return json_object
    
