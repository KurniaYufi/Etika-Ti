import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# Daftar stopwords untuk normalisasi (tanpa simbol '@')
stopwords = {
    'gw', 'gue', 'gua', 'yang', 'di', 'ini', 'itu', 'dan', 'atau', 'ke', 'dengan',
    'kamu', 'saya', 'aku', 'nya', 'yg', 'ga', 'gak', 'tidak', 'aja', 'loh', 'deh',
    'kok', 'nih', 'dong', 'kayak', 'juga', 'buat', 'kalo', 'kalau', 'udah', 'belum',
    'bisa', 'karena', 'hanya', 'lebih', 'masih', 'bukan', 'ada', 'mau', 'sama', 'ya', 'apa', 'bang', 'gitu', 'tapi', 'gk', 'kek', '😭', 'lagi', 'untung',
    'lu', 'tau', 'bg', 'abdi', 'jadi', 'ku', 'geda', 'jir', 'makan', 'gini', 'sih', 'bgt', 'mana', 'dia', 'the', 'suka', 'banget', 'kata',
    'ngerti','bintang'
}

# Fungsi untuk menghapus emotikon dari teks
def remove_emoticons(text):
    # Regex untuk mendeteksi emotikon
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

# Load komentar dari file output.json
with open('Skibidi/output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hitung kemunculan kata "skibidi" per URL video
skibidi_count_per_url = {}
all_words = []

for idx, entry in enumerate(data):
    if isinstance(entry, dict):  # Memastikan ini adalah metadata URL
        current_url = entry.get('post_url', f'Video {idx + 1}')
        skibidi_count_per_url[current_url] = 0  # Inisialisasi
    elif isinstance(entry, str):  # Komentar aktual
        # Hitung jumlah kemunculan kata 'skibidi' (case insensitive)
        count = entry.lower().count('skibidi')
        skibidi_count_per_url[current_url] += count
        
        # Tambahkan semua kata kecuali 'skibidi' dan stopwords untuk analisis WordCloud
        words = entry.lower().split()
        for word in words:
            if word != 'skibidi' and word not in stopwords:
                cleaned_word = remove_emoticons(word)  # Bersihkan emotikon
                if cleaned_word:  # Hanya tambahkan jika kata tidak kosong
                    all_words.append(cleaned_word)

# Visualisasi jumlah kemunculan 'skibidi' per URL
plt.figure(figsize=(10, 5))
bars = plt.bar(
    range(len(skibidi_count_per_url)),
    skibidi_count_per_url.values(),
    color=['#4c72b0'] * len(skibidi_count_per_url),  # Warna biru gradien terang
    edgecolor='black'
)

# Menambahkan label pada sumbu x sebagai "Video 1, Video 2, ..."
plt.xticks(
    range(len(skibidi_count_per_url)),
    [f"Video {i + 1}" for i in range(len(skibidi_count_per_url))],
    rotation=45,
    ha='right',
    fontsize=10
)

# Label untuk grafik
plt.title("Jumlah Kemunculan Kata 'Skibidi' pada tiap video", fontsize=14)
plt.xlabel("Video", fontsize=12)
plt.ylabel("Jumlah Kemunculan", fontsize=12)

# Menyesuaikan grid untuk sumbu y
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Simpan grafik
plt.savefig('Skibidi/skibidi_count_per_url.png', dpi=300)  # Kualitas gambar tinggi
plt.show()

# Hitung 20 kata yang paling sering muncul (selain 'skibidi' dan stopwords)
word_counts = Counter(all_words).most_common(20)

# Print word counts
print("20 Most Common Words (excluding 'skibidi' and stopwords):")
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
plt.savefig('Skibidi/wordcloud_top20_excluding_skibidi.png', dpi=300)  # Kualitas gambar tinggi
plt.show()
