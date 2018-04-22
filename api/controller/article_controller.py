import os

from flask import Flask, request, json, jsonify, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/article/<string:article_hash>", methods=['GET'])
def get_article(article_hash):  # TODO: add IPFS calls
    return jsonify(
        {"message": "Here's your article",
         "article_hash": article_hash})


@app.route("/article", methods=['POST'])
def add_article():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    metadata = request.form.get('metadata')
    print('metadata string: ' + metadata)
    dict = json.loads(metadata)
    print('metadata dict: ' + str(dict))

    if dict.get('title'):
        print('Title: ' + dict.get('title'))

    if dict.get('authors'):
        print('Authors: ' + ", ".join(dict.get('authors')))

    if dict.get('tags'):
        print('Tags: ' + ", ".join(dict.get('tags')))

    return jsonify({"msg": "Article inserted! (no)"})


# TODO: add search criteria/metadata model
@app.route("/article/find", methods=['POST'])
def find_articles():
    if request.headers['Content-Type'] == 'application/json':
        print("JSON Message: " + json.dumps(request.json))
        return jsonify({"message": "Here's what we found for your request"})
    else:
        return url_for(bad_request)


@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'Bad request',
        'reason': str(error)
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
