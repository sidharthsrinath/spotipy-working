import base64
import requests
from requests import post
import datetime

client_id = '99562b17e8964b2fb7da569cf0c2da1b'
client_secret = '5de3883fb0e3412c9b732301aab01b0e'


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        #returns a base64 encoded STRING

        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            raise Exception('Please set client credentials')

        client_cred = '{}:{}'.format(client_id, client_secret)
        client_cred_b64 = base64.b64encode(client_cred.encode())

        return client_cred_b64.decode()
    
    def get_token_header(self):
        client_cred_b64 = self.get_client_credentials()
        return {
            'Authorization' : f'Basic {client_cred_b64}'
        }

    def get_token_data(self):
        return {
            'grant_type' : 'client_credentials'
        }
    def auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()

        r = post(token_url, data = token_data, headers = token_header)
        valid_request = r.status_code in range(200,299)

        if valid_request:
            token_response_data = r.json()
            now = datetime.datetime.now()
            access_token = token_response_data['access_token']
            self.access_token = access_token
            expires_in = token_response_data['expires_in']
            expires = now + datetime.timedelta(seconds = expires_in)
            self.access_token_expires = expires
            self.access_token_did = expires < now
            return True
        else:
            return False


# client = SpotifyAPI(client_id,client_secret)
# a = client.auth()
# print(a)

# print(client.access_token)
