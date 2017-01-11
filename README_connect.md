# connection MongoDB Python 

import pymongo

client = pymongo.MongoClient("mongodb://strublereau:azerty@35.167.94.87/election")

print(client.election.test.find())

curs = client.election.test.find()

for i in curs :

	print(i)

print(type(curs))

print(client.election.test.count())

#### autres IP (esclave mongodb) : 35.167.81.39 , 35.164.243.142
