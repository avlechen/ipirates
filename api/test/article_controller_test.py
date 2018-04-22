import os

import requests
from requests_toolbelt import MultipartEncoder
from flask import Flask, current_app, jsonify

app = Flask(__name__)


def run_wrapped_test(test_to_run, *extraArgs, **extraKwArgs):
    with app.app_context():
        print("**********************************************************************************************************")
        test_to_run()
        print("**********************************************************************************************************")


def pretty_req(req):
    return '{} {}'.format(req.method, req.url)


def test_get_article_by_hash():
    req = requests.Request(
        method='GET',
        url='http://0.0.0.0:5000/article/QmPWdakDDBsRXNioLzmPQa45b1zYgoU5jMQo4gfTPcr7o4')
    prepared = req.prepare()
    print("Request:  " + pretty_req(prepared))

    session = requests.Session()
    resp = session.send(prepared)

    if resp.ok:
        print("Response: " + str(resp.json()))
    else:
        print("ERROR! Response: " + str(resp))


def test_add_article_file_with_metadata():
    test_file_name = 'hello_ipfs.txt'
    test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_file_name)

    m = MultipartEncoder(
        fields={
            'metadata': str({
                "title": "Structured computer organization",
                "authors": ["Andrew S. Tanenbaum", "Todd Austin"],
                "tags": ["hardware", "bible", "bsuir"]
            }).replace("'", "\""),
            'file': (test_file_name, open(test_file_path, 'rb'))}
    )  # it's possible to add 'text/plain'
    print(m.content_type)

    r = requests.post('http://0.0.0.0:5000/article', data=m,
                      headers={'Content-Type': m.content_type})

    # req = requests.Request(method='POST',
    #                        url='http://0.0.0.0:5000/article',
    #                        files={'file': open(test_file_path, 'rb')},
    #                        data={'a': 'bbb', 'c': 'ddd'})
    # prepared = req.prepare()
    # session = requests.Session()
    # response = session.send(prepared)
    response = r
    print(response.status_code)
    print(str(response.json()))
    return


if __name__ == "__main__":
    run_wrapped_test(test_get_article_by_hash)
    run_wrapped_test(test_add_article_file_with_metadata)
