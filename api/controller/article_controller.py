import os

import ipfsapi
from flask import Flask, request, json, jsonify, url_for
from werkzeug.utils import secure_filename

from pirate_client.multi_index import MultiIndex
from pirate_client.paper_client import PaperClient
from pirate_client.root_holder import DebugRootHolder

app = Flask(__name__)

api = ipfsapi.connect('127.0.0.1', 5001)
index = MultiIndex(api, DebugRootHolder(api))
paper_client = PaperClient(api, index)


@app.route("/article/<string:article_hash>", methods=['GET'])
def get_article(article_hash):
    #ipfs_prefix = 'https://ipfs.io/ipfs/'
    res = paper_client.get_file(article_hash)
    print('get_file result: ' + str(res))
    return jsonify(
        {"message": "Here's your article",
         "article": res})


@app.route("/article", methods=['POST'])
def add_article():
    file = request.files['file']
    filepath=""
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    metadata = request.form.get('metadata')
    print('metadata string: ' + metadata)
    metadata_dict = json.loads(metadata)
    print('metadata metadata_dict: ' + str(metadata_dict))

    if metadata_dict.get('doi'):
        print('DOI: ' + metadata_dict.get('doi'))

    if metadata_dict.get('title'):
        print('Title: ' + metadata_dict.get('title'))

    if metadata_dict.get('authors'):
        print('Authors: ' + ", ".join(metadata_dict.get('authors')))

    if metadata_dict.get('keywords'):
        print('Keywords: ' + ", ".join(metadata_dict.get('keywords')))

    res = paper_client.add_file(file=filepath, metadata=metadata_dict, is_tmp=True)
    print("Result: ")
    print(res)

    return jsonify({
        "message": "Article inserted!",
        "article": res
    })


# TODO: add search criteria/metadata model
@app.route("/article/find", methods=['POST'])
def find_articles():
    print("============ FIND ==============")
    print(request.json)
    print("Received JSON Message: " + str(request.json))
    query_dict = request.json

    if query_dict.get('doi'):
        print('DOI: ' + query_dict.get('doi'))

    if query_dict.get('title'):
        print('Title: ' + query_dict.get('title'))

    if query_dict.get('authors'):
        print('Authors: ' + ", ".join(query_dict.get('authors')))

    if query_dict.get('keywords'):
        print('Keywords: ' + ", ".join(query_dict.get('keywords')))

    res = paper_client.find_file(query=query_dict)
    print("Result: ")
    print(res)

    return jsonify({
        "message": "Here's what we found for your request",
        "articles": res
    })


@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'message': 'Bad request',
        'reason': str(error)
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
