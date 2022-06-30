import pickle

from ya360 import __path__
__path__ = __path__[0]


def load_token():
	with open(__path__+'/token.pickle','rb') as f:
		token = pickle.load(f)
	
	return token

	
def load_orgID():
	with open(__path__+'/orgid.pickle','rb') as f:
		orgID = pickle.load(f)
	
	return orgID

	
def save_token(token):
	with open(__path__+'/token.pickle','wb') as f:
		pickle.dump(token, f)

		
def save_orgID(orgID):
	with open(__path__+'/orgid.pickle','wb') as f:
		pickle.dump(orgID, f)
		
