#Route 53 DDNS script.
#Christopher Gannon
#https://twitter.com/gannoc
#This code is public domain

import boto
import boto.route53
import requests
import sys
from boto.route53.record import ResourceRecordSets

#Change these to the appropriate domains
HOSTED_ZONE = 'mydomain.com'
DOMAIN_NAME = 'www.mydomain.com'

#I found dnsomatic.com a very easy solution, but there are others that can be
#substitued here. You could also make a simple web service of your own onm a free 
#Amazon server.
try:
	new_ip_request = requests.request('GET', 'http://myip.dnsomatic.com')
except:
	print "Failed to get current IP address"
	sys.exit(1)
current_ip = new_ip_request.text

#Connect to Route 53 and check current IP address
conn = boto.route53.connect_to_region('us-west-2')
try:
	hostedzone = conn.get_zone(HOSTED_ZONE)
except:
	print "Failed to get zone " + HOSTED_ZONE
	sys.exit(1)

if not hostedzone:
	print "Hosted Zone " + HOSTED_ZONE + " not found."
	sys.exit(1)

#There is no way to get a single record set for a zone, so all record sets are retreieved.
response = conn.get_all_rrsets(hostedzone.id, 'A', DOMAIN_NAME, maxitems=1)


#Iterate through all DNS records, and update the DOMAIN_NAME ip address if different
for record in response:
	if DOMAIN_NAME+'.'==record.name:
		if current_ip not in record.resource_records:
			
			changes = ResourceRecordSets(conn, hostedzone.id)
			DDNS_changes = changes.add_change("UPSERT", DOMAIN_NAME, type="A", ttl=3600)
			DDNS_changes.add_value(current_ip)
			try:
				changes.commit()
			except:
				print "Error making changes to route53"
				sys.exit(1)
			print "Domain updated"
			sys.exit(0)
		else:
			print "No Update needed"
			sys.exit(0)


print "Domain name " + DOMAIN_NAME + " not found."



