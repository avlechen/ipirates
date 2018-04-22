import steem

import time

""" Use to communicate with steemit API:

    get_last_hash_comment() -> str
    send_new_hash_comment(new_hash: str, prev_hash: str) -> None
"""

# post variables
platform_url = 'steemit.com'
url_tag = 'ipfs'
profile_name = 'magnustest'
post_link = 'blockchain-hackathon-ipfs-hashes'

# account keys
prv_posting_key = '5KXSnDWzHzgopzpYuNBecTMdvrwzBTZNDi5xY24CLUsdzfQj8L4'
prv_active_key = '5K9okhCRC9Gz86X54UbGCw26p6emAAoibBzxvRgqq3K6mTf8vGh'

# Authorization from test account
s = steem.Steem(keys=[prv_posting_key, prv_active_key])


# Finds last added reply with hash
def get_last_hash_comment():
    comments = get_post_comments(post_link)

    # iterate of comments list in reverse order
    for comment in comments[::-1]:
        if comment['author'] != profile_name:
            continue
        return comment['body'].split()[-1]
    # if no replies in topic from account's author
    return None


# return array of all comments from the platform
def get_post_comments(post_link):
    comments = s.get_content_replies(profile_name, post_link)
    return comments


# Post new hash data into the blockchain replies
def send_new_hash_comment(new_hash, prev_hash=None):
    post_url = 'https://{}/{}/@{}/{}'.format(platform_url, url_tag, profile_name, post_link)
    p = steem.post.Post(post_url)

    body = body_string(new_hash, prev_hash)
    p.reply(body, author=profile_name)


# Return body string with hashes data
def body_string(new_hash, prev_hash=None):
    prev_hash = prev_hash or get_last_hash_comment()

    body = 'previous hash: {}\nnew hash: {}'.format(prev_hash, new_hash)
    return body


if __name__ == "__main__":
    first = '745294623649NEW'
    send_new_hash_comment(first)
    resp = get_last_hash_comment().split()[-1]
    print(first)
    print(resp)
    assert first == resp

    time.sleep(20)

    second = '745294623649SUPANEW'
    send_new_hash_comment(second, prev_hash=first)
    resp = get_last_hash_comment()
    print(second)
    print(resp)
    assert second == resp
