import requests
from msal import ConfidentialClientApplication

def acquire_token(client_id, client_secret, authority, scope):
	app = ConfidentialClientApplication(client_id, client_secret, authority)
	result = app.acquire_token_for_client(scope)

	if 'access_token' in result:
		return result['access_token']
	else:
		print(result.get('error'))
		print(result.get('error_description'))
		print(result.get('correlation_id'))
	exit(1)

client_id = "c0755607-fa42-48ac-a94a-9bf563253f61"
client_secret = "G8~8Q~tqLNLrM_XVhsQEbN3QhoOnadEwjHU_gc_i"
tenant_id = "6124334a-1ce1-4f5f-9446-cf095fa3d52c"
authority = "https://login.microsoftonline.com/" + tenant_id
scope_str = "api://" + client_id + "/.default"
scope = [scope_str]

token = acquire_token(client_id, client_secret, authority, scope)

headers = {
	'Authorization': f'Bearer {token}',
}

response1 = requests.get('https://lims-hub-test1.azurewebsites.net/api1/', headers=headers)
response2 = requests.get('http://lims-hub-test1.azurewebsites.net/api2/')


print(response1.text)
print(response2.text)
