import requests

class Session:

	def __init__(self,server,username,password):
		self.server = server
		response = requests.post(server+'/user/',auth=(username,password))
		if response.status_code != 200:
			raise Exception('Issue with authentication '+str(response.status_code))
		self.token = response.json()['data']['token']