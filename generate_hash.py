import hashlib
import dns.resolver

INPUT_FILE_NAME = "top_1m.txt"
OUTPUT_FILE_NAME = "hash_1m.txt"

def generate_hash():
	f = open(INPUT_FILE_NAME, 'r')
	f_iter = iter(f)
	sol = []

	for line in f_iter:
		temp = line.split()
		print(temp)
		print(hashlib.sha256(str(temp[2][1:-1]).encode('utf-8')).hexdigest())
		# rdata = dns.resolver.query(temp[2][1:-1], 'NS'):
		for rdata in dns.resolver.query(temp[2][1:-1], 'NS'):
			print(rdata)
		sol.append(hashlib.sha256(str(temp[2][1:-1]).encode('utf-8')).hexdigest())

	# sol.sort()

	# for s in sol:
	# 	for rdata in dns.resolver.query(s, 'NS'):
	# 		print(rdata)


generate_hash()