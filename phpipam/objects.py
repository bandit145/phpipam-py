import requests
from .exceptions import *

#update_excluded is for excluding certain values from being used in object creations/updates
# if one is a dict that's a conditional exclusion based off the kawrgs as the value (the key being the property to ignore)

class BaseIPAMObject:
	_fields = []
	_update_excluded = []
	_endpoint = ''

	def __init__(self, session):
		self.session = session
		self.__build_class__()

	def create(self,**kwargs):
		data = self.__get_params__(**kwargs)
		#no id needed for creating stuff
		del data['id']
		response = requests.post(self.session.server+self._endpoint,json=data,headers={'phpipam-token':self.session.token})
		if response.status_code != 201:
			raise Exception('failed: '+response.json()['message'])

	def __get_object__(self,obj_id):
		response = requests.get(self.session.server+self._endpoint+obj_id+'/',headers={'phpipam-token':self.session.token})
		if response.status_code != 200:
			raise Exception('failed: '+response.json()['message'])
		data = response.json()['data']
		#if list take the first response
		if type(data) == list:
			self.__set_params__(response.json()['data'][0])
		else:
			self.__set_params__(response.json()['data'])

	def update(self,**kwargs):
		data = self.__get_params__(**kwargs)
		response = requests.patch(self.session.server+self._endpoint+self.id+'/',json=data,headers={'phpipam-token':self.session.token})
		if response.status_code != 200:
			raise Exception('failed: '+response.json()['message'])

	def delete(self):
		response = requests.delete(self.session.server+self._endpoint+self.id+'/',headers={'phpipam-token':self.session.token})

	def __get_info__(self,uri, success_code):
		response = requests.get(session.server+self._endpoint+self.id+'/'+uri+'/',headers={'phpipam-token':self.session.token})
		#if response.status_code != 200:
		#	raise someexception()
		return response.json()

	def __get_params__(self,**kwargs):
		data = {}
		for attr in self._fields:
			if attr in self._update_excluded:
				pass
			elif(getattr(self,attr) == True):
				data[attr] = "1"
			elif(getattr(self,attr) == False):
				data[attr] = "0"
			else:
				data[attr] = getattr(self,attr)

		for attr in self._update_excluded:
			if type(attr) == dict:
				if list(attr.values())[0] in kwargs and not kwargs[list(attr.values())[0]]:
					del data[list(attr.keys())[0]]
		return data

	def __set_params__(self,data):
		if 'calculation' in data.keys():
			del data['calculation']
		for attr in data.keys():
			setattr(self,attr,data[attr])

	def __build_class__(self):
		for attribute in self._fields:
			setattr(self,attribute,None)

	def __convert_permissions__(self,permissions):
		return permissions.split(':')

	def __set_permissions__(self,permissions):
		return ':'.join(permissions)


class Subnet(BaseIPAMObject):
	_fields = ['id','subnet','mask','sectionId','description','linked_subnet','firewallAddressObject','vrfId',
	'masterSubnetID','allowRequests','vlanId','showName','device','permissions','pingSubnet','discoverSubnet','resolveDNS',
	'DNSrecursive','DNSrecords','nameserverId','scanAgent','isFolder','isFull','tag','threshold','location','editDate',
	'lastScan','lastDiscovery']
	_update_excluded = ['editDate','isFolder','subnet','mask','masterSubnetID','tag',{'vrfId':'vrf_tagged'},{'vlanId':'vlan_tagged'}]
	_endpoint = '/subnets/'

	def __init__(self,session):
		super().__init__(session)

	def get_by_cidr(self,cidr):
		response = requests.get(self.session.server+self._endpoint+'cidr/'+cidr+'/',headers={'phpipam-token':self.session.token})
		#if response.status_code != 200:
		#	raise someexception()
		self.__get_object__(response.json()['data'][0]['id'])

	def get_next_ip(self):
		#have this create a new address and return the Address object
		info = self.__get_info__('first_free')
		if 'data' not in info.keys():
			raise Exception('Subnet out of Addresses')
		return info['data']

class Address(BaseIPAMObject):
	_fields = ['id','subnetId','ip','is_gateway','description','hostname','mac','owner','tag','deviceId','location','port','note',
	'lastSeen','excludePing','PTRignore','PTR','firewallAddressObject','editDate']
	_update_excluded = ['firewallAddressObject','editDate']
	_endpoint = '/addresses/'

	def __init__(self, session):
		super().__init__(session)

	def ping(self):
		response = self.__get_info__('ping')
		if response.status_code != 200:
			if 'message' in response.keys():
				raise Exception(response['message'])
			else:
				raise Exception('Uknown error')
		return info['data']['result_code']


class VRF(BaseIPAMObject):
	pass

class VLAN(BaseIPAMObject):
	pass

class L2Domain(BaseIPAMObject):
	pass

class Device(BaseIPAMObject):
	pass

class NameServer(BaseIPAMObject):
	pass

class ScanAgent(BaseIPAMObject):
	pass

class NAT(BaseIPAMObject):
	pass

class Location(BaseIPAMObject):
	pass

class Rack(BaseIPAMObject):
	pass