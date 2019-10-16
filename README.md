# LogonLabs Python

The official LogonLabs Python library.
## Download
- First time install
```
    pip install logonlabs-python
```
- If you have installed the package already, please upgrade it.
```
    pip install --upgrade logonlabs-python
```
## LogonLabs API

- Prior to coding, some configuration is required at https://app.logonlabs.com/app/#app-settings

- For the full Developer Documentation please visit: https://app.logonlabs.com/api/

---
### Instantiating a new client

- Your `APP_ID` can be found in [App Settings](https://app.logonlabs.com/app/#/app-settings).
- `APP_SECRETS` are configured [here](https://app.logonlabs.com/app/#/app-secrets).
- The `LOGONLABS_API_ENDPOINT` should be set to `https://api.logonlabs.com`.

Create a new instance of `LogonClient`.  
```python
from logonlabs.client import Logonlabs

logonClient = Logonlabs('{APP_ID}', '{APP_SECRETS}', '{LOGONLABS_API_ENDPOINT}')

```
---
### SSO Login QuickStart
The StartLogin function in the JS library begins the LogonLabs managed SSO process.
>Further documentation on starting the login process via our JavaScript client can be found at our GitHub page [here](https://github.com/logonlabs/logonlabs-js). 
The following example demonstrates what to do once the `callback Url` has been used by our system to redirect the user back to your page:
```python
request_headers = self.headers
token = request_headers["token"]
response = logonClient.validateLogin(token)
data = response.json()
if data['event_success']:
    #authentication and validation succeeded. proceed with post-auth workflows (ie, create a user session token for your system).
```
---
### Python Only Workflow
The following workflow is required if you're using Python to process all transaction requests.  If this does not apply to you, please refer to the SSO Login QuickStart section.
#### Step 1 - StartLogin
This call begins the LogonLabs managed SSO process.  The `client_data` property is optional and is used to pass any data that is required after validating the request. The `tags` property is an Array of type Tag which is a simple object representing a key/value pair.
```python

identity_provider = '{string}' # one of the following ['microsoft','google','facebook','linkedin','slack','twitter','github','quickbooks','onelogin','okta','apple','basecamp','dropbox','fitbit','planningcenter','twitch']
identity_provider_id = '{string}' # require identity_provider or identity_provider_id
client_data = '{string}'
tags = [{'example-key': 'example-value'}]
redirect = False
callback_url = 'https://example.com'
destination_url = 'https://example.com'
response = logonClient.startLogin(identity_provider, identity_provider_id, "example@emailaddress.com", client_data, callback_url, destination_url, tags)
redirect_url = response.url
```

The `redirect_url` property returned should be redirected to by the application.  Upon submitting their credentials, users will be redirected to the `callback_url` set within the application settings at https://logonlabs.com/app/#/app-settings.
&nbsp;
#### Step 2 - ValidateLogin
This method is used to validate the results of the login attempt.  `query_token` corresponds to the query parameter with the name `token` appended to the callback url specified for your app.
The response contains all details of the login and the user has now completed the SSO workflow.  If there is any additional information to add, UpdateEvent can be called on the `event_id` returned.
```python

response = logonClient.validateLogin('{token}')
data = response.json()
if data['event_success']:
    #success
else:
    validation_details = data['validation_details']
    if validation_details['domain_validation'] == 'Fail':
        #provider used was not enabled for the domain of the user that was authenticated

    if validation_details['ip_validation'] == 'Fail' or validation_details['geo_validation'] == 'Fail' or validation_details['time_validation'] == 'Fail':
        #validation failed via restriction settings for the app
```
---
### CreateEvent
The CreateEvent method allows one to create events that are outside of our SSO workflows.
```python

local_validation = '{string}' # one of the following ['Pass', 'Fail', 'NotApplicable']
tags = [{'example-key': 'example-value'}]
event_type = '{string}' # one of the following ['LocalLogin', 'LocalLogout']

response = logonClient.createEvent(event_type, True, local_validation, "{EMAIL_ADDRESS}", "{IP_ADDRESS}", "{USER_AGENT}", "{FIRST_NAME}", "{LAST_NAME}", tags)
```
---
### Helper Methods
#### GetProviders
This method is used to retrieve a list of all providers enabled for the application.
If an email address is passed to the method, it will return the list of providers available for that email domain.
```python
response = logonClient.getProviders("example@emailaddress.com")
data = response.json()
social_identity_providers = data['social_identity_providers']
for provider in social_identity_providers:
    #each individual providers available for this email address

enterprise_identity_providers = data['enterprise_identity_providers']
for enterpriseProvider in enterprise_identity_providers:
    #each enterprise providers available for this email address
```