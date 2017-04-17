from flask import Flask, send_from_directory, request, json
from src.update_page import *
from src.maintainer.config import huey
import os

app = Flask(__name__)

PAGE_STORAGE = "pages"
TEST_PAGE_STORAGE = "../../test/pages"
ABS_PATH = os.path.dirname(os.path.realpath('__file__'))
DIFF_SUFFIX = ".diff"


@huey.task()
@app.route('/get_page', methods=['GET'])
def get_page_api():
    page_id = request.args.get('page_id')
    version = request.args.get('version')

    # TODO: Perform range check on page_id
    # TODO: Perform range check on version number
    if version is None:
        # Return the current version of the page
        path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
        return send_from_directory(path, page_id)
    else:
        # Return the diff from the version passed
        page_path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
        curr_version = get_page_current_version(page_path, page_id)

        if curr_version == version:
            response = app.response_class(
                response=json.dumps(str("Updated")),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            diff = Diff()
            page_path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
            diff_url = diff.combine_diffs(int(version), int(curr_version), page_id, page_path)
            return send_from_directory(diff_url, "comb_diff_" + page_id + "_" + version + "_" + str(curr_version)
                                       + DIFF_SUFFIX)


@app.route('/update_page', methods=['GET'])
def update_page_api():
    # GET Parameters
    page_id = request.args.get('page_id')
    entry = request.args.get('SHA256')
    a_record = request.args.get('ARecord')

    # Sanitize parameters according to function params
    a_record = a_record.split(",")
    a_record = ' '.join(a_record)

    # Find page path which needs to passed via function
    page_path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)

    update_page(page_id, entry, a_record, page_path)

    response = app.response_class(
        response=json.dumps(str("Updated")),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/get_signature', methods=['GET'])
def compute_signature_api():
    # GET Parameters
    page_id = request.args.get('page_id')
    page_path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
    return send_from_directory(page_path, page_id+".sig")
