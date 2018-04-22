import os

import requests


def run_wrapped_test(test_to_run, *extraArgs, **extraKwArgs):
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
    req = requests.Request(method='POST',
                           url='http://0.0.0.0:5000/article',
                           files={'file': open(test_file_path, 'rb')})
    prepared = req.prepare()
    session = requests.Session()
    response = session.send(prepared)
    print(response.status_code)
    print(str(response.json()))
    return


if __name__ == "__main__":
    run_wrapped_test(test_get_article_by_hash)
    run_wrapped_test(test_add_article_file_with_metadata)
