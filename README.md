# LogonLabs Python

The official LogonLabs Python library.
## Download

    pip install -i logonlabs-python
## LogonLabs API

- Prior to coding, some configuration is required at https://app.logonlabs.com/app/#app-settings

- For the full Developer Documentation please visit: https://app.logonlabs.com/docs/api/

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
    #success
```
---
### Python Only Workflow
The following workflow is required if you're using Python to process all transaction requests.  If this does not apply to you, please refer to the SSO Login QuickStart section.
#### Step 1 - StartLogin
This call begins the LogonLabs managed SSO process.  The `client_data` property is optional and is used to pass any data that is required after validating the request.  The `client_encryption_key` property is optionally passed if the application requires encrypting any data that is passed between the front and back ends of its infrastructure. The `tags` property is an Array of type Tag which is a simple object representing a key/value pair.
```python

identity_provider = '{string}' # one of the following ['microsoft','google','facebook','linkedin','slack','github','quickbooks','onelogin']
identity_provider_id = '{string}' # require identity_provider or identity_provider_id
client_data = '{string}'
client_encryption_key = "qbTRzCvUju"
tags = [{'example-key': 'example-value'}]
redirect = False
response = logonClient.startLogin(identity_provider, identity_provider_id, "emailAddress", client_data, client_encryption_key, tags)
redirect_url = response.url
```

The `redirect_url` property returned should be redirected to by the application.  Upon submitting their credentials, users will be redirected to the `callback_url` set within the application settings at https://app.logonlabs.com/app/#/app-settings.
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
    if validation_details['auth_validation'] == 'Fail':
        #authentication with identity provider failed

    if validation_details['email_match_validation'] == 'Fail':
        #email didn't match the one provided to StartLogin

    if validation_details['ip_validation'] == 'Fail' or validation_details['geo_validation'] == 'Fail' or validation_details['time_validation'] == 'Fail':
        #validation failed via restriction settings for the app
```
---
### Events
The CreateEvent method can be used to create events that are outside of our SSO workflows.  UpdateEvent can be used to update any events made either by CreateEvent or by our SSO login.
```python

local_validation = '{string}' # one of the following ['Pass', 'Fail', 'NotApplicable']
tags = [{'example-key': 'example-value'}]
event_type = '{string}' # one of the following ['LocalLogin', 'LocalLogout']

response = logonClient.createEvent(event_type, True, local_validation, "email_address", "ip_address", "user_agent", "first_name", "last_name", tags)
data = response.json()
event_id = data['event_id']

local_validation = 'Fail'
tags = [{'failure-field': 'detailed reason for failure'}]
response = logonClient.updateEvent(event_id, local_validation, tags)
```
---
### Helper Methods
#### GetProviders
This method is used to retrieve a list of all providers enabled for the application.
If an email address is passed to the method, it will return the list of providers available for that email domain.
```python
response = logonClient.getProviders("emailAddress")
data = response.json()
identity_providers = data['identity_providers']
for provider in identity_providers:
    #each individual providers available for this email address

```
#### Encrypt / Decrypt
The Python SDK has built in methods for encrypting strings using AES encryption.  Use a value for your encryption key that only your client will know how to decrypt 
```python

client_encryption_key = "qbTRzCvUju"
value = "string to be encrypted"
encrypted_string = logonClient.encrypt(value, client_encryption_key)

decrypted_string = logonClient.decrypt(encrypted_string, client_encryption_key)
```
