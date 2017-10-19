# JIRAconn.py
import sys
import json
import re
import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA

def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()

# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.
CONSUMER_KEY = 'eadp_jirabot'
CONSUMER_SECRET = 'dont_care'
VERIFIER = 'jira_verifier'

# The contents of the rsa.pem file generated (the private RSA key)
#RSA_KEY = read('/jira.pem')
RSA_KEY = read('/Users/ctote/.ssh/jira.pem')

# The URLs for the JIRA instance
JIRA_SERVER = 'https://*'
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'


if (len(sys.argv) > 1 and sys.argv[1].lower() == 'oauth'):
    # Step 1: Get a request token

    oauth = OAuth1Session(CONSUMER_KEY, signature_type='auth_header',
                          signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)
    request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    resource_owner_key = request_token['oauth_token']
    resource_owner_secret = request_token['oauth_token_secret']

    print("STEP 1: GET REQUEST TOKEN")
    print("  oauth_token={}".format(request_token['oauth_token']))
    print("  oauth_token_secret={}".format(request_token['oauth_token_secret']))
    print("\n")


    # Step 2: Get the end-user's authorization

    print("STEP2: AUTHORIZATION")
    print("  Visit to the following URL to provide authorization:")
    print("  {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
    print("\n")

    while raw_input("Press any key to continue..."):
        pass


    oauth = OAuth1Session(CONSUMER_KEY, client_secret= CONSUMER_SECRET, resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret, verifier=VERIFIER, signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)


    # Step 3: Get the access token

    access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)

    print("STEP2: GET ACCESS TOKEN")
    print("  oauth_token={}".format(access_token['oauth_token']))
    print("  oauth_token_secret={}".format(access_token['oauth_token_secret']))
    print("\n")


    # Now you can use the access tokens with the JIRA client. Hooray!

    JIRA_CONN = JIRA(options={'server': JIRA_SERVER}, oauth={
        'access_token': access_token['oauth_token'],
        'access_token_secret': access_token['oauth_token_secret'],
        'consumer_key': CONSUMER_KEY,
        'key_cert': RSA_KEY
    })
else:
    JIRA_CONN = JIRA(options={'server': JIRA_SERVER, 'rest_api_version': 'latest'}, basic_auth=('*','*'))

