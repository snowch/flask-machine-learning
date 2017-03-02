import os
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request

app = Flask(__name__)

#if 'VCAP_SERVICES' in os.environ:
#    vcap = json.loads(os.getenv('VCAP_SERVICES'))
#    print('Found VCAP_SERVICES')
#else:
#    # see vcap-local.json-template for example file structure
#    with open('vcap-local.json') as f:
#        vcap = json.load(f)

# FIXME: Incorrect values are being passed in by VCAP_SERVICES
#        so always read from vcap-local.json.  However, this 
#        will break "Deploy To Bluemix"

# see vcap-local.json-template for example file structure
with open('vcap-local.json') as f:
    vcap = json.load(f)

creds = vcap['pm-20'][0]['credentials']

# Store the global configuration variables
app.config.update(
    URL = creds['url'],
    ACCESSKEY = creds['access_key']
)

@app.route('/')
def runit():
    return '''
        <html>
            <body>
                <form action="/getscore">
                    <label for="context">Context</label>
                    <input type="text" name="context" id="context"><br>
                    <label for="age">Age</label>
                    <input type="age" name="age" id="age"><br>
                    <input type="submit" value="Submit">
                </form>
            <body>
        </html>
    '''

@app.route("/getscore")
def hello():

    age = int(request.args.get('age', None))
    context = request.args.get('context', None)

    data = {
      "tablename":"InputData", 
      "header":["Customer ID","Offer1","Offer2","Offer3","Offer4","Offer5","Offer6","Offer7","Offer8","Offer9","Offer10","Offer11"], 
      "data":[[age, "F", "F", "T", "T", "F", "T", "F", "F", "T", "T", "T"]]
    }
    url = "{0}/score/{1}?accesskey={2}".format(
                                            app.config['URL'], 
                                            context, 
                                            app.config['ACCESSKEY'])

    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    return response.text

port = int(os.getenv('PORT', 8080))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)

