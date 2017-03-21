import os
import tempfile

PAGE_STORAGE = "pages"
DIFF_SUFFIX = ".diff"
TMP_DIR = tempfile.gettempdir()

class CombineDiff:

	def init(self):
		
	
	def combine_diffs(self, start_version, end_version, page_id):
		curr_file_name = os.path.join(PAGE_STORAGE, str(page_id))
		copy_file_url = os.path.join(TMP_DIR, str(page_id)+"_diff")
		os.system("cp "+ curr_file_name + " " + copy_file_url)
		while(end_version > start_version):
			diff_file_path = os.path.join(PAGE_STORAGE, str(page_id)+str(end_version)+DIFF_SUFFIX)
			# diff syntax diff -u new old > .diff
			# create copy of original version
			command = "patch " + copy_file_url + " " + diff_file_path
			os.system(command)
			end_version -= 1
		
	def generate_diffs(self, new_version, page_id):
		curr_file_name = os.path.join(PAGE_STORAGE, str(page_id))
		copy_file_url = os.path.join(TMP_DIR, str(page_id)+"_diff")
		os.system("cp "+ curr_file_name + " " + copy_file_url)
		new_diff_file = os.path.join(PAGE_STORAGE, str(page_id)+str(new_version)+DIFF_SUFFIX)
		command = "diff -u " + copy_file_url + " " + curr_file_name + " > " new_diff_file
		os.system(command)