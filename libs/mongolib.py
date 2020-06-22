from pymongo import MongoClient
import urllib
import json
from datetime import datetime
from bson.objectid import ObjectId
import config

class mongoLib():
	"""
		This class contains method for connection and performing
		data storage and manipulation in mongo db
	"""
	mongoconn = None
	mongoconndb = None
	DB_NAME = ''

	def __init__(self, host=config.MONGO_HOST, port=config.MONGO_PORT, user=config.MONGO_USER, password=config.MONGO_PASSWD, database_name=config.MONGO_DATABASE):
		try:
			if user == '' and password == '':
				self.mongoconn = MongoClient('mongodb://'+ host +':'+ port+ '/')
			else:
				password = urllib.quote_plus(password)
				self.mongoconn = MongoClient('mongodb://'+ user +':' + password + '@'+ host +':'+ port)

			if database_name != '':
				self.mongoconndb = self.mongoconn['{0}'.format(database_name)]
				self.DB_NAME = database_name
		except Exception as e:
			raise e


	def getDB_NAME(self):
		"""
		This Returns Database Name
		Parameters: VOID
		Returns: String DB_NAME
		"""
		return self.DB_NAME


	def getInstance(self):
		"""
		This Returns created DB connection instance
		Parameters: VOID
		Returns: MongoClient Connection Object
		"""
		return self.mongoconn


	def getDbInstance(self):
		"""
		This Returns created DB connection object
		Parameters: VOID
		Returns: MongoClient Connection Object to a database
		"""
		return self.mongoconndb



	def insert_doc(self, collection_name,data, data_id=''):
		"""
		This function insert a document into a mongodb.
		Parameters: collection_name => String(Name of the collection)
					data  => Dictionary(key is table field name, value is the value to insert)
					data_id => String(Custom _id for the document)
		Returns: Boolean(True for success and False for failure)
		"""
		try:
			if data_id != '':
				data["_id"] = data_id

			print(data)
			if type(data) == type({}):
				result = self.mongoconndb['{0}'.format(collection_name)].insert_one(data)
				if result.acknowledged == True:
					print(result.inserted_id)
					return True
				else:
					return False
			else:
			 	print("Wrong document format.")
			 	return False
			pass
		except Exception as e:
			return False
			#raise e


	def find_all_doc(self, collection_name, query={}, fields=[], limit=50, skip=0):
		"""
		This function insert a document into a mongodb.
		Parameters: collection_name => String(Name of the collection)
					query  => Dictionary(key is field name, value is the value to insert)
					fields => List(fields to return)
					limit => int(Number of documents to return)
					skip => int(Page value)
		Returns: Boolean(True for success and False for failure)
		"""
		try:
			select_fields = {}
			print(query)
			if len(fields) > 0:
				for field in fields:
					select_fields['{0}'.format(field)] =  1

			skip *= limit

			res = []

			if type(query) == type({}):
				if len(select_fields) > 0:
					results = self.mongoconndb['{0}'.format(collection_name)].find(query, select_fields)
				else:
					results = self.mongoconndb['{0}'.format(collection_name)].find(query).skip(skip).limit(limit)

				for result in results:
					result['datePaid'] = str(result['datePaid'])
					res.append(JSONEncoder().encode(result))
				return res
			else:
			 	print("Wrong document format.")
			 	return False
		except Exception as e:
			raise e


	def update_doc(self, collection_name, data={}, query={}):
		"""
		This function insert a document into a mongodb.
		Parameters: collection_name => String(Name of the collection)
					query  => Dictionary(key is field name, value is the value for query)
					data => Dictionary(key is field name, value is the value to Update)
		Returns: Boolean(True for success and False for failure)
		"""
		try:
			print(data)
			if type(data) == type({}):
				data = {"$set": data}
				print(query)
				result = self.mongoconndb['{0}'.format(collection_name)].update_many(query, data)
				return True
			else:
			 	print("Wrong document format.")
			 	return False
			pass
		except Exception as e:
			raise e


	def delete_doc(self, collection_name, query={}, del_all=False):
		"""
		This function insert a document into a mongodb.
		Parameters: collection_name => String(Name of the collection)
					query  => Dictionary(key is field name, value is the value for query)
					del_all => Boolean(Set to true to delete all document, with an empty query)
		Returns: Boolean(True for success and False for failure)
		"""
		try:
			#print(query)
			if query != {} and (del_all==False or del_all==True):
				print(query)
				result = self.mongoconndb['{0}'.format(collection_name)].delete_many(query)
				return True
			elif query == {} and del_all==True:
				result = self.mongoconndb['{0}'.format(collection_name)].delete_many({})
				return True
			else:
			 	print("Please provide a query or Set del_all to 'True' to remove all documents.")
			 	return False
			pass
		except Exception as e:
			raise e


	def drop_collection(self, collection_name):
		"""
		This function insert a document into a mongodb.
		Parameters: collection_name => String(Name of the collection)
		Returns: Boolean(True for success and False for failure)
		"""
		try:
			#print(query)
			if collection_name != '':
				print(collection_name)
				result = self.mongoconndb['{0}'.format(collection_name)].drop()
				return True
			else:
			 	print("Please provide a Collection.")
			 	return False
			pass
		except Exception as e:
			raise e


class JSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
        return str(o)
    return json.JSONEncoder.default(self, o)

# if __name__ == '__main__':
# 	conn = mongoLib(database_name='groupInns')
# 	print(conn.getInstance())
# 	print(conn.getDbInstance())
# 	print(conn.getDB_NAME())

	# res = conn.insert_doc("restaurants", {
	# 				"address": { \
	# 							"street": "2 Avenue", \
	# 							"zipcode": "10075", \
	# 							"building": "1480", \
	# 							"coord": [-73.9557413, 40.7720266] \
	# 							}, \
	# 				"borough": "Manhattan", \
	# 				"cuisine": "Italian", \
	# 				"grades": [ \
	# 							{ \
	# 							"date": datetime.strptime("2014-10-01", "%Y-%m-%d"), \
	# 							"grade": "A", \
	# 							"score": 11 \
	# 							}, \
	# 							{ \
	# 							"date": datetime.strptime("2014-01-16", "%Y-%m-%d"), \
	# 							"grade": "C", \
	# 							"score": 7 \
	# 							} \
	# 						], \
	# 				"name": "Vella", \
	# 				"restaurant_id": "41704623" \
	# 				}, "25")

	# print(res)
	# '''
	# For Finding documents
	# '''
	# res = conn.find_all_doc("contributions", query={},limit=5)
	# print(res)
	# '''
	# For Updating documents
	# '''
	#res = conn.update_doc("restaurants", query={"_id":"25"}, data={"cuisine": "American", "address.street":"Avenue"})

	# '''
	# For Deleting documents
	# '''
	#res = conn.delete_doc("restaurants", query={"_id":"25"})

	# '''
	# For Drop documents
	# '''
	#res = conn.dorp_collection("companies")

