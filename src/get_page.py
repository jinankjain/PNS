def get_page(id, version=None):
	if version == None:
		## Return the page directly with specific page id
		return page
	else:
		## Generate diffs
		## This one is tricky