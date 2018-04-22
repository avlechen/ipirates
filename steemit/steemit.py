import steem

# post variables
platform_url = 'steemit.com'
url_tag = 'ipfs'
profile_name = 'magnustest'
post_link = 'blockchain-hackathon-ipfs-hashes'

# account keys
prv_posting_key = '5KXSnDWzHzgopzpYuNBecTMdvrwzBTZNDi5xY24CLUsdzfQj8L4'
prv_active_key = '5K9okhCRC9Gz86X54UbGCw26p6emAAoibBzxvRgqq3K6mTf8vGh'

# Authorization from test account
s = steem.Steem(keys=[prv_posting_key, prv_active_key ])


# Finds last added reply with hash
def get_last_hash_comment():
    comments = get_post_comments(post_link)

    # iterate of comments list in reverse order
    for comment in comments[::-1]:
        if comment['author'] != profile_name:
            continue
        return comment['body']
    # if no replies in topic from account's author
    return 'no comments'

# return array of all comments from the platform
def get_post_comments(post_link):
    comments = s.get_content_replies(profile_name, post_link)
    return comments

# Post new hash data into the blockchain replies
def send_new_hash_comment(hash):
    post_url = 'https://{}/{}/@{}/{}'.format(platform_url, url_tag, profile_name, post_link)
    p = steem.post.Post(post_url)
    p.reply(hash, author=profile_name)

if __name__ == "__main__":
    send_new_hash_comment('testhashfromtest')
    print(get_last_hash_comment())
