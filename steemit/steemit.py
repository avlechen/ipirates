import steem

s = steem.Steem(keys=['5KXSnDWzHzgopzpYuNBecTMdvrwzBTZNDi5xY24CLUsdzfQj8L4', '5K9okhCRC9Gz86X54UbGCw26p6emAAoibBzxvRgqq3K6mTf8vGh'])
profile_name = 'magnustest'
post_link = 'blockchain-hackathon-ipfs-hashes'


def get_last_hash_comment():
    comments = get_post_comments(post_link)

    for comment in comments[::-1]:
        if comment['author'] != profile_name:
            continue
        return comment['body']
    return 'no comments'

def get_post_comments(post_link):
    comments = s.get_content_replies(profile_name, post_link)
    return comments

def send_new_hash_comment(hash):
    p = steem.post.Post('https://steemit.com/ipfs/@magnustest/blockchain-hackathon-ipfs-hashes')
    p.reply(hash, author=profile_name)

if __name__ == "__main__":
    send_new_hash_comment('testhashfromtest')
    print(get_last_hash_comment())
