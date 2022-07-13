import requests, json, time, random

def jreq(mode, url, token, body=None, try_number=1):
	try:
		if mode == 'post': response = requests.post(url, data=json.dumps(body), headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'get': response = requests.get(url, headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'patch': response = requests.patch(url, data=json.dumps(body), headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'delete': response = requests.delete(url, headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()

	except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
		time.sleep(2**try_number + random.random()*0.01)
		print('Попытка: '+str(try_number+1))
		return jreq(mode, url, token, body, try_number=try_number+1)

	else:
		return response