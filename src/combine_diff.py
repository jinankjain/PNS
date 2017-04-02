import os
import tempfile

PAGE_STORAGE = "pages"
DIFF_SUFFIX = ".diff"
TMP_DIR = tempfile.gettempdir()


class Diff:
    def init(self):
        pass

    def combine_diffs(self, start_version, end_version, page_id, page_path):
        curr_file_name = os.path.join(page_path, page_id)
        print("Current File is: ", curr_file_name)
        copy_file_url = os.path.join(TMP_DIR, page_id + "_diff")
        print("Copy File URL is: ", copy_file_url)
        command = "cp " + curr_file_name + " " + copy_file_url
        os.system(command)
        end_version_copy = end_version
        while end_version > start_version:
            diff_file_path = os.path.join(page_path, page_id + "_" + str(end_version) + DIFF_SUFFIX)
            print("Diff file path is: ", diff_file_path)
            # diff syntax diff -u new old > .diff
            # create copy of original version
            command = "patch " + copy_file_url + " " + diff_file_path
            os.system(command)
            end_version -= 1
        new_diff_file = os.path.join(TMP_DIR, "comb_diff_" + str(page_id) + "_" + str(start_version) + "_" + str(
            end_version_copy) + DIFF_SUFFIX)
        print("New diff file is: ", new_diff_file)
        command = "diff -u " + curr_file_name + " " + copy_file_url + " > " + new_diff_file
        os.system(command)
        return TMP_DIR

    def generate_diffs(self, new_version, page_id, page_path):
        curr_file_name = os.path.join(page_path, str(page_id))
        update_file_name = os.path.join(page_path, str(page_id) + "_" + str(new_version))
        new_diff_file = os.path.join(page_path, str(page_id) + "_" + str(new_version) + DIFF_SUFFIX)
        # Generate diffs
        command = "diff -u " + update_file_name + " " + curr_file_name + " > " + new_diff_file
        os.system(command)
        # Replace old copy with new copy
        command = "cp " + update_file_name + " " + curr_file_name
        os.system(command)
        # Remove _diff file
        command = "rm " + update_file_name
        os.system(command)
