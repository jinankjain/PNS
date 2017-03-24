from flask import Flask, send_from_directory
from flask import request
import os

app = Flask(__name__, static_url_path='')

PAGE_STORAGE = "pages"
ABS_PATH = os.path.dirname(os.path.realpath('__file__'))


@app.route('/get_page', methods=['GET'])
def get_page( ):
    page_id = request.args.get('page_id')
    version = request.args.get('version')

    ## TODO: Perform range check on page_id
    ## TODO: Perform range check on version number

    if version is None:
        # Return the current version of the page
        path = os.path.join(ABS_PATH, "..", PAGE_STORAGE)
        print(path)
        return send_from_directory(path, page_id)
    else:
        # Return the diff from the version passed
        path = os.path.join(ABS_PATH, "..", PAGE_STORAGE, page_id)
        return app.send_static_file(path)
