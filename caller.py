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

client_id = "2eaf78be-97f7-44ee-8590-0adf91febc72"
client_secret = "LI48Q~Q5tDBJCN~CrgKpH79uwqmNQ2M~-M4UHbj6"
tenant_id = "72250571-2bdd-409c-9171-b48c97ee5d74"
authority = "https://login.microsoftonline.com/" + tenant_id
scope_str = "api://" + client_id + "/.default"
scope = [scope_str]

token = acquire_token(client_id, client_secret, authority, scope)

headers = {
    'Authorization': f'Bearer {token}',
}

#response1 = requests.get('http://localhost:5000/api1/', headers=headers)
#response1 = requests.get('http://localhost:5000/api1/', headers=headers)
#response2 = requests.get('http://localhost:5000/api2/')

# Using the self-signed certificate for verification
#response1 = requests.get('https://localhost:5000/api1', headers=headers, verify='/home/wo/code/b2b-api/cert.pem')

# OR disabling SSL verification (not recommended in production)
response1 = requests.get('https://localhost:5000/api1', headers=headers, verify=False)
response2 = requests.get('http://localhost:5001/api2')

print(response1.text)
print(response2.text)