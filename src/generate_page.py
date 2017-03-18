import get_name_server
import hashlib
import os
import time

INPUT_FILE_NAME = "top_1m.txt"
PAGE_INDEX = 1
PAGE_STORAGE = "pages"

def generate_page():
	f = open(INPUT_FILE_NAME, 'r')
	f_iter = iter(f)
	page = []
	for line in f_iter:
		temp = line.split()
		temp = temp[2][1:-1]
		fqdn_hash = hashlib.sha256(str(temp).encode('utf-8')).hexdigest()
		ns_ipv4 = get_name_server.find_nameserver(temp)
		page.append([fqdn_hash, list(ns_ipv4)[0:4], time.strftime("%c")])
	page.sort(key=lambda x: x[0])

	i = 0
	page_len = len(page)
	while(i < page_len):
		curr_page = page[i][0:PAGE_INDEX]
		f = open(os.path(PAGE_STORAGE, curr_page), 'a')
		f.write("Page Version 1\n")
		while(curr_page == page[i][0:PAGE_INDEX]):
			f.write(page[i])
			f.write("\n")
			i+=1
		f.close()


def main():
	generate_page()

if __name__ == "__main__":
	main()