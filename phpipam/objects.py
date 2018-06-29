import requests
import json
from exceptions import *

class BaseIPAMObject:
	_fields = []
	endpoint = ''

	def __init__(self, session):
		self.session = session
		self.endpoint = endpoint
		self.__build_class__()

	def create_object(self):
		data = self.__get__parms()
		response = requests.post(session.server+endpoint,params=json.dumps(data),headers={'phpipam-token':session.token})

	def get_object(self,id):
		response = requests.get(session.server+self.endpoint+self.id,headers={'phpipam-token':session.token})
		self.__set__params(response.json()['data'])

	def update_object(self,endpoint):
		response = requests.patch(session.server+endpoint,params=json.dumps(data),headers={'phpipam-token':session.token})

	def delete_object(self,endpoint):
		response = requests.delete(session.server+endpoint,headers={'phpipam-token':session.token})

	def __get__parms(self):
		data = {}
		for attr in self._fields:
			if(getattr(self,attr) == True):
				data[attr] = "1"
			elif(getattr(self,attr) == False):
				data[attr] = "0"
			else:
				data[attr] = getattr(self,attr)
		return data

	def __set__params(self,data):
		for attr in data.keys():
			setattr(self,attr,data[attr])

	def __build_class__(self):
		for attribute in self._fields:
			setattr(self,attribute,'')

	def __convert_permissions_(self,permissions):
		return permissions.split(':')

	def __set_permissions(self,permissions):
		return ':'.join(permissions)


class Subnet(BaseIPAMObject):
	_fields = ['id','subnet','mask','sectionID','description','linked_subnet','firewallAddressObject','vrfId',
	'masterSubnetID','allowRequests','vlanId','showName','device','permissions','pingSubnet','discoverSubnet','resolveDNS',
	'DNSrecrusive','DNSrecords','nameserverId','scanAgent','isFolder','isFull','tag','threshold','location','_editDate',
	'lastScan','lastDiscovery']
	endpoint = '/subnets/'

	def __init__(self,session):
		super().__init__()

class Address(BaseIPAMObject):
	pass

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