## Design Documentation for a PNS Page

- Deciding upon the length of prefix which is gonna be used to identify the page.
	- By looking at paper this part is not really clear
	- Running a small test how prefixes would look like collecting all top 1 million Alexa sites generate SHA256 of those FQDN and sort the result.
	- Looking at results it is not very clear how we should partition the page prefixes 

- Solution:
	- <b> Ideal Case (No Replication): </b>
		- Consitent Hashing looks a tempting idea.
		- Some mathematical ideas:
		- Each hash is 32 bytes: 32*8 = 256 bits
		- So the total range is 2^256
	- <b> Replication Strategy </b>
		- Not really sure about the replication strategy.

Big Problems:

- Python does not have a good library to resolve DNS. So I might have to switch to GO.
- I tried experimenting with GO but I ran into few troubles:
	- Domains like detail.tmall.com does not have NS records because some other domain is responsible for that part. How to handle this case?

Solution:

- We can have a simple algorithm: it's on my paper right now need to write in documentation

## Page Structure

Otherwise the page structure would be something like this

Page Information: Version 1

Hash [NS address] [NS IPv4] [NS IPv6 (Optional)] Date of creation
99464a1c6b08896a33745b78b6aa4dfd88857073f33e9a9dea8a16b9445386a0 [ns4.google.com, ns3.google.com, ns2.google.com, ns1.google.com] [216.239.38.10, 216.239.36.10, 216.239.34.10, 216.239.32.10]		
### Note: Keep in mind about hash collisions