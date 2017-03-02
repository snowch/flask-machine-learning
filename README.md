
### Deploy to Bluemix

Deploy to bluemix is currently broken. See: https://github.com/snowch/flask-machine-learning/blob/master/hello.py#L20

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/snowch/flask-machine-learning.git)

### Manual setup

- Create a Watson Machine Learning instance
- Upload NextBestOfferDepl.str to your Watson Machine Learning instance
- Copy vcap-local.json-template to vcap-local.json
- Edit vcap-local.json with your credentials
- cf login
- cf push ...
- Access the provided URL and enter the values


