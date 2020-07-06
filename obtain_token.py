# -*- coding: utf-8 -*-
import json

from urllib.parse import urljoin, urlencode, urlparse, parse_qs
from requests_oauthlib import OAuth1Session
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT


# ------ STEP 1 - INITATION (GET REQUEST TOKEN)------

BASE_URL = 'http://test.skichic.zeus.advox.pl'
CALLBACK_URI = 'http://example.com'
REQUEST_TOKEN_ENDPOINT = '/fr/oauth/initiate?' + urlencode({'oauth_callback': CALLBACK_URI})
REQUEST_TOKEN_URL = urljoin(BASE_URL, REQUEST_TOKEN_ENDPOINT)

with open('consumer_key', 'r') as f:
    CONSUMER_KEY = f.read().rstrip()

with open('consumer_secret', 'r') as f:
    CONSUMER_SECRET = f.read().rstrip()

print(f'Request token url: {REQUEST_TOKEN_URL}')
print(f'Consumer key: {CONSUMER_KEY}')
print(f'Consumer secret: {CONSUMER_SECRET}\n')

magentoAuthSession = OAuth1Session(client_key=CONSUMER_KEY,
                                   client_secret=CONSUMER_SECRET,
                                   callback_uri=CALLBACK_URI,
                                   signature_method=SIGNATURE_PLAINTEXT)
response = magentoAuthSession.fetch_request_token(REQUEST_TOKEN_URL)

oauth_token = response.get('oauth_token')
oauth_token_secret = response.get('oauth_token_secret')

print(f'oauth_token: {oauth_token}\noauth_token_secret: {oauth_token_secret}\n')


# ------ STEP 2 - USER AUTHORIZATION ------
AUTHORIZATION_ENDPOINT = '/fr/admin/oauth_authorize?' + urlencode({'oauth_token': oauth_token})
AUTHORIZATION_URI = urljoin(BASE_URL, AUTHORIZATION_ENDPOINT)

print(f'To authorize the skichic_api application to access the magento instance at {BASE_URL}, please visit the following url and grant access (you may be asked for your credentials):\n{AUTHORIZATION_URI}\n')
redirect_uri = input('Please copy/paste the url your browser redirected you to: ')
parsed_uri = urlparse(redirect_uri)
oauth_verifier = parse_qs(parsed_uri.query).get('oauth_verifier')[0]
print(f'\noauth_token: {oauth_token}\noauth_verifier: {oauth_verifier}\n')

# ------ STEP 2 - RETRIEVE ACCESS TOKEN ------
ACCESS_TOKEN_ENDPOINT = '/fr/oauth/token'
ACCESS_TOKEN_URI = urljoin(BASE_URL, ACCESS_TOKEN_ENDPOINT)
magentoAuthSession = OAuth1Session(client_key=CONSUMER_KEY,
                                   client_secret=CONSUMER_SECRET,
                                   resource_owner_key=oauth_token,
                                   resource_owner_secret=oauth_token_secret,
                                   verifier=oauth_verifier)
tokens = magentoAuthSession.fetch_access_token(ACCESS_TOKEN_URI)

access_token = tokens.get('oauth_token')
token_secret = tokens.get('oauth_token_secret')

print(f'Access token: {access_token}\nToken secret: {token_secret}')
