import os

class SecureTransport():

    def enable(self):
        if 'OAUTHLIB_INSECURE_TRANSPORT' in os.environ:
            del os.environ['OAUTHLIB_INSECURE_TRANSPORT']

    def disable(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def __del__(self):
        if 'OAUTHLIB_INSECURE_TRANSPORT' in os.environ:
            del os.environ['OAUTHLIB_INSECURE_TRANSPORT']