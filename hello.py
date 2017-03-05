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
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container-fluid">
                    <h2>Predictive Scoring Inputs:</h2>
                    <p>Enter the values for your context and the age</p>
                    <div class="row">
                        <form action="/getscore">
                            <div class="col-sm-4">
                                <div class="row">
                                    <div class="col-xs-6">
                                        <label for="context">Context</label>
                                        <input type="text" name="context" id="context" class="form-control">
                                    </div>
                                </div>
                                <br/>
                                <div class="row">
                                    <div class="col-xs-6">
                                        <label for="context">Customer ID</label>
                                        <input type="text" value="10451" name="customer_id" id="customer_id" class="form-control">
                                    </div>
                                </div>
                                <br/>
                                <div class="row">
                                    <div class="col-xs-6">
                                        <input type="submit" value="Submit" class="form-control">
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            <body>
        </html>
    '''

@app.route("/getscore")
def hello():

    customer_id = int(request.args.get('customer_id', None))
    context = request.args.get('context', None)

    data = {
      "tablename":"InputData", 
      "header":["Customer ID","Offer1","Offer2","Offer3","Offer4","Offer5","Offer6","Offer7","Offer8","Offer9","Offer10","Offer11"], 
      "data":[[customer_id, "F", "F", "T", "T", "F", "T", "F", "F", "T", "T", "T"]]
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

