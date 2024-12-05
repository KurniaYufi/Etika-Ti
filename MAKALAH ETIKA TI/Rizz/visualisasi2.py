import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

stopwords = {
    'gw', 'gue', 'gua', 'yang', 'di', 'ini', 'itu', 'dan', 'atau', 'ke', 'dengan',
    'kamu', 'saya', 'aku', 'nya', 'yg', 'ga', 'gak', 'tidak', 'aja', 'loh', 'deh',
    'kok', 'nih', 'dong', 'kayak', 'juga', 'buat', 'kalo', 'kalau', 'udah', 'belum',
    'bisa', 'karena', 'hanya', 'lebih', 'masih', 'bukan', 'ada', 'mau', 'sama', 'ya', 'apa', 'bang', 'gitu', 'tapi', 'gk', 'kek', '😭', 'lagi', 'untung',
    'lu', 'tau', 'bg', 'abdi', 'jadi', 'ku', 'geda', 'jir', 'makan', 'gini', 'sih', 'bgt', 'mana', 'dia', 'the', 'suka', 'banget', 'kata',
    'me', 'i', 'you', 'are', 'a', 'is', 'to', 'and', 'be', ':', '.', '!', '?', ',', 'the', 'of', 'for', 'on', 'at', 'by', 'with', 'as', 'this', 'that', 
    'it', 'in', 'an', 'from', 'up', 'down', 'out', 'all', 'some', 'more', 'no', 'so', 'much', 'than', 'its', 'have', 'had', 'having','gw:','dia:','if','kenapa','my','u','your',
    'do','ngerti','cuz','see','can','but','know','just','apa?','not','because','cause','im','without','kak','can','one','only','when','aku:'
}

def remove_emoticons(text):
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Emotikon wajah
        "\U0001F300-\U0001F5FF"  # Simbol & ikon
        "\U0001F680-\U0001F6FF"  # Transportasi & simbol terkait
        "\U0001F700-\U0001F77F"  # Simbol tambahan
        "\U0001F780-\U0001F7FF"  # Geometris tambahan
        "\U0001F800-\U0001F8FF"  # Suplemen tambahan
        "\U0001F900-\U0001F9FF"  # Suplemen wajah
        "\U0001FA00-\U0001FA6F"  # Ikon objek tambahan
        "\U0001FA70-\U0001FAFF"  # Ikon lain
        "\U00002700-\U000027BF"  # Simbol tambahan (seperti tanda centang)
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

with open('Rizz/output1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rizz_count_per_url = {}
all_words = []

for idx, entry in enumerate(data):
    if isinstance(entry, dict):  
        current_url = entry.get('post_url', f'Video {idx + 1}')
        rizz_count_per_url[current_url] = 0  
    elif isinstance(entry, str):  
        count = entry.lower().count('rizz')
        rizz_count_per_url[current_url] += count
        
        words = entry.lower().split()
        for word in words:
            if word != 'rizz' and word not in stopwords:
                cleaned_word = remove_emoticons(word)  
                if cleaned_word: 
                    all_words.append(cleaned_word)

plt.figure(figsize=(10, 5))
bars = plt.bar(
    range(len(rizz_count_per_url)),
    rizz_count_per_url.values(),
    color=['#4c72b0'] * len(rizz_count_per_url),  
    edgecolor='black'
)

plt.xticks(
    range(len(rizz_count_per_url)),
    [f"Video {i + 1}" for i in range(len(rizz_count_per_url))],
    rotation=45,
    ha='right',
    fontsize=10
)

# Label untuk grafik
plt.title("Jumlah Kemunculan Kata 'Rizz' pada tiap video", fontsize=14)
plt.xlabel("Video", fontsize=12)
plt.ylabel("Jumlah Kemunculan", fontsize=12)

# Menyesuaikan grid untuk sumbu y
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Simpan grafik
plt.savefig('Rizz/rizz_count_per_url.png', dpi=300)  # Kualitas gambar tinggi
plt.show()

# Hitung 20 kata yang paling sering muncul (selain 'rizz' dan stopwords)
word_counts = Counter(all_words).most_common(20)

# Print word counts
print("20 Most Common Words (excluding 'rizz' and stopwords):")
for word, count in word_counts:
    print(f"{word}: {count}")

# Membuat WordCloud dari 20 kata terbanyak
wordcloud_data = {word: count for word, count in word_counts}
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("20 Kata Terbanyak yang relevan", fontsize=14)

# Simpan WordCloud
plt.savefig('Rizz/wordcloud_top20_excluding_rizz_and_stopwords_no_emoji.png', dpi=300)  # Kualitas gambar tinggi
plt.show()
