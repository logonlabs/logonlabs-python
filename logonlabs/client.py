"""Logonlabs
"""

DEFAULT_BASE_URL = "https://api.logonlabs.com/"

from logonlabs.api import ping,\
    getProviders,\
    startLogin,\
    validateLogin,\
    redirectLogin,\
    createEvent,\
    updateEvent

from logonlabs.allowableValues import identityProviders,\
    eventTypes,\
    localVallidationValues

from logonlabs.util import encrypt, decrypt

class Logonlabs(object):
    def __init__(self, app_id, app_secret, api_path=DEFAULT_BASE_URL):
        self.app_id = app_id
        self.api_path = api_path
        self.app_secret = app_secret

    def ping(self):
        return ping(self.api_path)

    def getProviders(self, email_address):
        params = {
            'app_id': self.app_id
        }
        if email_address is not None:
            params['email_address'] = email_address

        return getProviders(self.api_path, params)

    def startLogin(self,
        identity_provider=None,
        identity_provider_id=None,
        email_address=None,
        client_data=None,
        client_encryption_key=None,
        tags=None):
        params = {
            'app_id': self.app_id
        }

        if identity_provider is not None:
            if identity_provider in identityProviders:
                params['identity_provider'] = identity_provider
            else:
                raise Exception('{} is not one of the allowable identity providers'.format(identity_provider))

        if identity_provider_id is not None:
            params['identity_provider_id'] = identity_provider_id

        if email_address is not None:
            params['email_address'] = email_address

        if client_data is not None:
            params['client_data'] = client_data

        if client_encryption_key is not None:
            params['client_encryption_key'] = client_encryption_key

        if tags is not None:
            params['tags'] = tags

        response = startLogin(self.api_path, params)
        responseObject = response.json()
        if responseObject is None or responseObject['token'] is None:
            return response
        params = {
            'token': responseObject['token']
        }
        response = redirectLogin(self.api_path, params)
        return response

    def validateLogin(self, token):
        params = {
            'app_id': self.app_id
        }
        if token is not None:
            params['token'] = token

        headers = {
            'x-app-secret': self.app_secret
        }

        return validateLogin(self.api_path, params, headers)

    def createEvent(self,
        eventType,
        validate=None,
        local_validation=None,
        email_address=None,
        ip_address=None,
        user_agent=None,
        first_name=None,
        last_name=None,
        tags=None):
        params = {
            'app_id': self.app_id
        }
        headers = {
            'x-app-secret': self.app_secret
        }

        if eventType is not None:
            if eventType in eventTypes:
                params['type'] = eventType
            else:
                raise Exception('{} is not one of the allowable event types'.format(eventType))

        if validate is not None:
            params['validate'] = validate

        if local_validation is not None:
            if local_validation in localVallidationValues:
                params['local_validation'] = local_validation
            else:
                raise Exception('{} is not one of the allowable local validation value'.format(local_validation))

        if email_address is not None:
            params['email_address'] = email_address

        if ip_address is not None:
            params['ip_address'] = ip_address

        if user_agent is not None:
            params['user_agent'] = user_agent

        if first_name is not None:
            params['first_name'] = first_name

        if last_name is not None:
            params['last_name'] = last_name

        if tags is not None:
            params['tags'] = tags

        return createEvent(self.api_path, params, headers)

    def updateEvent(self,
            event_id,
            local_validation=None,
            tags=None):
        params = {
            'app_id': self.app_id
        }
        headers = {
            'x-app-secret': self.app_secret
        }

        if event_id is not None:
            params['event_id'] = event_id
        else:
            raise Exception('event_id cannot be empty')

        if local_validation is not None:
            if local_validation in localVallidationValues:
                params['local_validation'] = local_validation
            else:
                raise Exception('{} is not one of the allowable local validation value'.format(local_validation))

        if tags is not None:
            params['tags'] = tags

        return updateEvent(self.api_path, params, headers)

    @staticmethod
    def encrypt(msg, password):
        return encrypt(msg, password)

    @staticmethod
    def decrypt(enc, password):
        return decrypt(enc, password)
