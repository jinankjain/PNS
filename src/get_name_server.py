import dns.resolver

def check_if_root_domain(url):
	ans = [False, []]
	try:
		# TODO: Find other way to construct the array (Need help dns.resolver documentation)
		for rdata in dns.resolver.query(url, 'NS'):
			ans[0] = True
			ans[1].append(rdata)
	except dns.resolver.NoAnswer:
		ans = ans
	except dns.resolver.NXDOMAIN:
		ans = ans
	except dns.resolver.NoNameservers:
		ans = ans
	except dns.resolver.NotAbsolute:
		ans = ans
	except dns.resolver.YXDOMAIN:
		ans = ans
	except dns.exception.Timeout:
		ans = ans
	except dns.exception.NoRootSOA:
		ans = ans
	except dns.exception.NotAbsolute:
		ans = ans
	return ans

def get_A_record_for_ns(url):
	ans = []
	try:
		for rdata in dns.resolver.query(url, 'A'):
			ans.append(rdata)
	except dns.resolver.NoAnswer:
		ans = ans
	return ans

def find_nameserver(url):
	temp = url.split('.')
	A_records = set()
	for i in range(0, len(temp)):
		check = check_if_root_domain(".".join(temp[i:]))
		if check[0]:
			for ns in check[1]:
				A_records |= set(get_A_record_for_ns(url))
	
	return A_records