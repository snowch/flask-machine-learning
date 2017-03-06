import os
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, session

app = Flask(__name__)

app.secret_key = 'make_this_secret_in_production_environements'

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
    
    if 'context' in session:
        context = session['context']
    else:
        context = ""

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
                                        <label for="context">Context ID</label>
                                        <input type="text" value="{0}" name="context" id="context" class="form-control">
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
    '''.format(context)

@app.route("/getscore")
def hello():

    customer_id = int(request.args.get('customer_id', None))
    context = request.args.get('context', None)

    # save the context in the session so users don't have to keep typing it in
    # when they run the example lots of times

    session['context'] = context

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

    head = response.json()[0]['header']
    data = response.json()[0]['data'][0]

    tr = ''
    for item in zip(head, data):
        tr += '<tr><td style="font-weight:bold;">{0}</td><td>{1}</td></tr>'.format(item[0], item[1])

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
                    <h2>Predictive Scoring Output</h2>
                    <p>The output from the machine learning service:</p>
                    <div class="row">
                        <div class="col-sm-4">
                          <table class="table">
                            <tbody>
                                {0}
                            </tbody>
                          </table>
                        </div>
                    </div>
                    <a class="btn btn-info" href="/">Try again</a>
                </div>
            <body>
        </html>
    '''.format(tr)

port = int(os.getenv('PORT', 8080))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
