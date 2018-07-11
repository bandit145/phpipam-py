from phpipam.objects import *
from phpipam.session import Session
import unittest


class TestSession(unittest.TestCase):
	def test_create_session(self):
		session = Session('http://127.0.0.1/api/phpipam','admin','testpass')
		self.assertEqual(session.server,'http://127.0.0.1/api/phpipam')
		self.assertTrue(len(session.token)>0)

class TestBaseObject(unittest.TestCase):

	def test_param_building(self):
		session = Session('http://127.0.0.1/api/phpipam','admin','testpass')
		ipam_object = BaseIPAMObject(session)
		ipam_object._fields = ['test1','test2','test3','editDate']
		ipam_object.__build_class__()
		ipam_object.__set_params__({'test1':True,'test2':True,'test3':True,'editDate':False})
		self.assertTrue(ipam_object.test1)
		self.assertTrue(ipam_object.test2)
		self.assertTrue(ipam_object.test3)
		self.assertFalse(ipam_object.editDate)

	def test_get_params(self):
		session = Session('http://127.0.0.1/api/phpipam','admin','testpass')
		ipam_object = BaseIPAMObject(session)
		ipam_object.__set_params__({'test1':True,'test2':True,'test3':True,'editDate':False})
		self.assertTrue(ipam_object.test1)
		#wow, this took like an hour to figure out I forgot
		ipam_object._fields = ['test1','test2','test3','editDate']
		ipam_object._update_excluded = ['editDate']
		data = ipam_object.__get_params__()
		self.assertDictEqual(data,{'test1':'1','test2':'1','test3':'1'})

class TestSubnetObject(unittest.TestCase):

	def test_subnet(self):
		session = Session('http://127.0.0.1/api/phpipam','admin','testpass')
		subnet = Subnet(session)
		subnet.get_by_cidr('10.10.1.0/24')
		self.assertEqual(subnet.id,"3")
		subnet.description = "edited"
		subnet.update(vlan_tagged=False,vrf_tagged=False)
		#verify update
		subnet = Subnet(session)
		subnet.get_by_cidr('10.10.1.0/24')
		self.assertEqual(subnet.description,"edited")

class TestAddressObject(unittest.TestCase):

	def test_address(self):
		session = Session('http://127.0.0.1/api/phpipam','admin','testpass')
		address = Address(session)
		address.__get_object__("1")
		self.assertEqual(address.ip,"10.10.1.3")
		address.delete()
		#create object
		address.create()
		#verify that it is recreated
		address = Address(session)
		address.__get_object__("11")
		self.assertEqual(address.ip,"10.10.1.3")


if __name__ == '__main__':
	unittest.main()