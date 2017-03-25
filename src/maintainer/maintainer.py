from flask import Flask, send_from_directory, request
from src.utils import *
from src.combine_diff import *

import os

app = Flask(__name__, static_url_path='')

PAGE_STORAGE = "pages"
ABS_PATH = os.path.dirname(os.path.realpath('__file__'))
DIFF_SUFFIX = ".diff"

@app.route('/get_page', methods=['GET'])
def get_page( ):
    page_id = request.args.get('page_id')
    version = request.args.get('version')

    ## TODO: Perform range check on page_id
    ## TODO: Perform range check on version number

    if version is None:
        # Return the current version of the page
        path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
        return send_from_directory(path, page_id)
    else:
        # Return the diff from the version passed
        path = os.path.join(ABS_PATH, "..", PAGE_STORAGE, page_id)
        curr_version = get_page_current_version(page_id)
        if curr_version == int(version):
            return send_from_directory(path, page_id)
        else:
            diff = Diff()
            diff_url = diff.combine_diffs(version, curr_version, page_id)
            return send_from_directory(diff_url, "comb_diff_" + page_id + "_" + version + "_" + str(curr_version)
                                       + DIFF_SUFFIX)


@app.route('/update_page', methods=['GET'])
def update_page():
    page_id = request.args.get('page_id')
    entry = request.args.get('SHA256')
    a_record = request.args.get('ARecord')

    path = os.path.join(ABS_PATH, "..", PAGE_STORAGE, page_id)
