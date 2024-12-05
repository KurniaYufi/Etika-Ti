import requests
import json
import os

# List URL TikTok posts
post_urls = [
    'https://www.tiktok.com/@mrci.tv/video/7379185769686027526',  # Ganti dengan URL video pertama
    'https://www.tiktok.com/@mrci.tv/video/7395142693183212805',  # Ganti dengan URL video kedua
    'https://www.tiktok.com/@geraldvincentt/video/7389982680789650693',  # Ganti dengan URL video ketiga
    'https://www.tiktok.com/@thejokels/video/7366140715606265093',  # Ganti dengan URL video keempat
    'https://www.tiktok.com/@_dimzsukameme_/video/7265326827999382790'   # Ganti dengan URL video kelima
]

# Headers untuk request
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.tiktok.com/explore',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

# Fungsi untuk request data komentar
def req(post_id, curs):
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&count=20&cursor={curs}&aweme_id={post_id}'
    response = requests.get(url=url, headers=headers)
    raw_data = json.loads(response.text)
    print(f'Fetching cursor: {curs} for post ID: {post_id}')
    return raw_data

# Fungsi untuk parsing data komentar
def parser(data, comments):
    try:
        comment_list = data.get('comments', [])
        for cm in comment_list:
            # Mengambil komentar dan membersihkan teks 'comment:'
            com = cm.get('share_info', {}).get('desc', '') or cm.get('text', '')
            com = com.split('’s comment:')[-1].strip()  # Menghapus bagian 's comment:' dan spasi ekstra
            comments.append(com)
    except Exception as e:
        print(f"Error parsing data: {e}")

# Proses pengambilan komentar untuk setiap URL
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

# Save comments to a JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("\nData from all videos has been saved... good job!")
