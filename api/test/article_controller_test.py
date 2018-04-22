import json
import os

import requests
from flask import jsonify
from requests_toolbelt import MultipartEncoder


def run_wrapped_test(test_to_run, *extraArgs, **extraKwArgs):
    print("**********************************************************************************************************")
    test_to_run()
    print("**********************************************************************************************************")


def pretty_req(req):
    return '{} {}'.format(req.method, req.url)


def test_get_article_by_hash():
    req = requests.Request(
        method='GET',
        url='http://0.0.0.0:5000/article/QmYQCPRgyFiH2AweHFg9MVUjhA9av1oe1w3EMrui6Ri4bi')
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
            'metadata': json.dumps({
                "doi": "10.1000/xyz123",
                "title": "Structured computer organization",
                "authors": ["Andrew S. Tanenbaum", "Todd Austin"],
                "keywords": ["hardware", "bible", "bsuir"]
            }),
            'file': (test_file_name, open(test_file_path, 'rb'))}
    )  # it's possible to add 'text/plain'
    print('request content type: ' + m.content_type)

    # TODO: send prepared request with logging
    response = requests.post('http://0.0.0.0:5000/article', data=m, headers={'Content-Type': m.content_type})

    print("response.status_code: " + str(response.status_code))
    print("response itself: " + str(response.json()))
    return


def test_find_article():

    json_query = json.dumps({
                "doi": "10.1000/xyz123",
                "title": "Structured computer organization",
                "authors": ["Andrew S. Tanenbaum", "Todd Austin"],
                "keywords": ["hardware", "bible", "bsuir"]})

    response = requests.post('http://0.0.0.0:5000/article/find',
                             data=json_query, headers= {'Content-Type': 'application/json'})

    print("response.status_code: " + str(response.status_code))
    print("response itself: " + str(response.json()))
    return


if __name__ == "__main__":
    #run_wrapped_test(test_get_article_by_hash)
    #run_wrapped_test(test_add_article_file_with_metadata)
    run_wrapped_test(test_find_article)
