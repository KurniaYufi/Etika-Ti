import requests
import json
import os

post_urls = [
    'https://www.tiktok.com/@ryyourmood/video/7270029735432867077',  
    'https://www.tiktok.com/@jbrc97/video/7037099593686895898',  
    'https://www.tiktok.com/@htsjaya46/video/7204066725870980379',  
    'https://www.tiktok.com/@jennifer_laurenth/video/7270873253395107077',  
    'https://www.tiktok.com/@zelynafah/video/7240035561040334086'   
]

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.tiktok.com/explore',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def req(post_id, curs):
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&count=20&cursor={curs}&aweme_id={post_id}'
    response = requests.get(url=url, headers=headers)
    raw_data = json.loads(response.text)
    print(f'Fetching cursor: {curs} for post ID: {post_id}')
    return raw_data

def parser(data, comments):
    try:
        comment_list = data.get('comments', [])
        for cm in comment_list:
            com = cm.get('share_info', {}).get('desc', '') or cm.get('text', '')
            com = com.split('’s comment:')[-1].strip() 
            comments.append(com)
    except Exception as e:
        print(f"Error parsing data: {e}")

all_comments = []

for post_url in post_urls:
    post_id = post_url.split('/')[-1]
    comments = [{'post_url': post_url}]
    curs = 0
    
    while True:
        raw_data = req(post_id, curs)
        parser(raw_data, comments)

        if raw_data.get('has_more', 0):
            curs += 20
            print('Moving to the next cursor...')
        else:
            print(f'No more comments available for post: {post_url}')
            break
    
    all_comments.extend(comments)


with open('output1.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("\nData from all videos has been saved... good job!")
