import os

from flask import Flask, request, json, jsonify, url_for
from werkzeug.utils import secure_filename

from pirate_client.paper_client import PaperClient

app = Flask(__name__)
paper_client = PaperClient()


@app.route("/article/<string:article_hash>", methods=['GET'])
def get_article(article_hash):  # TODO: add IPFS calls?
    ipfs_prefix = 'https://ipfs.io/ipfs/'
    # TODO: add validation (check article exists) or even return the article itself
    return jsonify(
        {"message": "Here's your article",
         "link": "{}{}".format(ipfs_prefix, article_hash)})


@app.route("/article", methods=['POST'])
def add_article():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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

    return jsonify({"message": "Article inserted! (no)"})


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

    return jsonify({"message": "Here's what we found for your request"})


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
