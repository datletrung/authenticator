from flask import Flask, request
import re
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def result():
    url = request.args.get('url')
    is_url = (re.match(regex, url) is not None)
    if is_url:
        return "true"
    else:
        return "false"

    
app.run('localhost', 7491, True)
