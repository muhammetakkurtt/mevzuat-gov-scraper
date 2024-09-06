import os
import subprocess
import spacy
from pathlib import Path
import json
import re
from tqdm import tqdm

def install_git_lfs():
    """Git LFS'in kurulu olup olmadığını kontrol eder, yoksa kurulum talimatı verir."""
    try:
        # git lfs komutunun mevcut olup olmadığını kontrol et
        subprocess.run(["git", "lfs", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Git LFS zaten kurulu.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git LFS kurulu değil.")
        
        # Kullanıcıdan onay al
        user_input = input("Git LFS'i yüklemek ister misiniz? (Y/N): ").strip().lower()
        if user_input == 'Y' or user_input == 'y':
            print("Git LFS yükleniyor...")
            try:
                # Sistem türüne göre kurulum komutu
                if os.name == 'nt':
                    # Windows'ta Chocolatey ile kurulum
                    subprocess.run(["choco", "install", "git-lfs"], check=True)
                else:
                    # Linux/MacOS için kurulum
                    subprocess.run(["sudo", "apt-get", "install", "git-lfs"], check=True)
                
                # Git LFS'i kurduktan sonra etkinleştir
                subprocess.run(["git", "lfs", "install"], check=True)
                print("Git LFS başarıyla kuruldu.")
            except subprocess.CalledProcessError:
                print("Git LFS kurulurken bir hata oluştu. Lütfen manuel olarak kurun.")
                print("Kurulum için: https://git-lfs.github.com/")
                exit(1)
        else:
            print("Git LFS kurulmadan çıkılıyor.")
            exit(1)

def clone_model():
    """Hugging Face'den modeli git-lfs ile klonlar."""
    model_dir = "tr_core_news_lg"
    if not os.path.exists(model_dir):
        print("Model klonlanıyor...")
        try:
            subprocess.run(["git", "clone", "https://huggingface.co/turkish-nlp-suite/tr_core_news_lg"], check=True, env=dict(os.environ, GIT_CLONE_PROTECTION_ACTIVE="false"))
            print("Model başarıyla klonlandı.")
        except subprocess.CalledProcessError:
            print("Model klonlanırken bir hata oluştu. Lütfen git ve git-lfs'i<n doğru kurulduğundan emin olun.")
            exit(1)
    else:
        print("Model zaten mevcut.")

def load_model():
    """Spacy modeli yükler."""
    try:
        model_path = Path("tr_core_news_lg")
        if model_path.exists():
            nlp = spacy.load(model_path)
            print("Model başarıyla yüklendi.")
            return nlp
        else:
            print(f"Model dizini bulunamadı: {model_path}")
            return None
    except OSError:
        print("Model yüklenemedi. Lütfen modelin doğru yüklendiğinden emin olun.")
        exit(1)

# Git LFS'in kurulu olup olmadığını kontrol ediyoruz
install_git_lfs()

# Modeli klonluyoruz
clone_model()

# Modeli yüklüyoruz
nlp = load_model()


def clean_text(text):
    # Fazla boşlukları ve \n karakterlerini temizle
    text = re.sub(r'\s+', ' ', text)  # Birden fazla boşluk ve newline karakterlerini tek boşluk ile değiştir
    text = text.strip()  # Metnin başındaki ve sonundaki boşlukları temizle
    return text

# JSON dosyasını oku
with open('mevzuat.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Ayrıştırılmış veriyi saklamak için bir liste oluştur
parsed_data = []

for entry in tqdm(data, desc="Kanunları işleme", unit="kanun"):
    # Metni temizle
    text = clean_text(entry['full_text'])
    
    # Kanun adını yakalamak için regex desenleri
    kanun_adi_pattern = r'((?:\d{1,2}/\d{1,2}/\d{4}\s+)?[\w\s,()/\dÎîÛûÂâÊêÔô\'’\-\"“”\.\,\;]+(?:KANUNU|DAİR KANUN|HAKKINDA KANUN|MAHSUS KANUN|MUADDİL KANUN|BUYURAN KANUN|İLİŞKİN KANUN|DÜZENLEYEN KANUN|İLGİLİ KANUN|KANUNA EK KANUN))'

    # Kanun adını regex ile yakalıyoruz
    kanun_adi_matches = re.findall(kanun_adi_pattern, text)

    if kanun_adi_matches:
        # Eğer re.findall sonuç döndürdüyse, bu sonucu birleştiriyoruz
        kanun_adi = ' '.join(kanun_adi_matches) if kanun_adi_matches else None
    elif not kanun_adi_matches:
        istisna_pattern = r'(TÜRKİYE CUMHURİYETİ ANAYASASI|MUHTAR ÖDENEK VE SOSYAL GÜVENLİK YASASI|BAZI KANUNLARLA TANINMlŞ OLAN GÜMRÜK MUAFiYETLERİNİN KALDIRILMASI HAKKlNDA KANUN|ATATÜRK ORMAN ÇİFTLİĞİ ARAZİSİNİN 8070 DEKARININ SATILMASI HAKKINDA)'
        kanun_adi_match = re.search(istisna_pattern, text)
        
        # Eğer istisna bulunduysa, match object'ten group(1)'i alıyoruz ve büyük harfe çeviriyoruz
        if kanun_adi_match:
            # Eğer istisna bulunduysa, büyük harfe çeviriyoruz
            kanun_adi = kanun_adi_match.group(1)
        else:
            kanun_adi_pattern_small = r'((?:\d{1,2}/\d{1,2}/\d{4}\s+)?[\w\s,()\dÎîÛûÂâÊêÔô\'’\-\"“”]+(?:Kanunu|Hakkında Kanun|İlişkin Kanun))'
            kanun_adi_match = re.search(kanun_adi_pattern_small, text, re.IGNORECASE)
            # Eğer bir eşleşme bulunduysa, match object'ten group(1)'i alıyoruz
            kanun_adi = kanun_adi_match.group(1).upper() if kanun_adi_match else None
  
    
    kanun_numarasi_patterns = [
    r'(?:K)anun (?:N)umarası\s*:?\s*(\d+)',  # Standart "Kanun Numarası"
    r'Kanun\s*Maddesi\s*:?\s*(\d+)',         # "Kanun Maddesi"
    r'Kanunun\s*Numarası\s*:?\s*(\d+)',      # "Kanunun Numarası"
    r'Kabul\s*Numarası\s*:?\s*(\d+)',        # "Kabul Numarası"
    r'Kanunu\s*Numarası\s*:?\s*(\d+)',       # "Kanunu Numarası"
    r'Kanun\s*numarası\s*:?\s*(\d+)',        # "kanun numarası" (küçük harf)
    r'Numarası\s*:?\s*(\d+)'                 # Sadece "Numarası"
    ]

    # Kanun numarasını yakalamak için regex desenlerini sırayla deniyoruz
    kanun_numarasi = None
    for pattern in kanun_numarasi_patterns:
        kanun_numarasi_match = re.search(pattern, text)
        if kanun_numarasi_match:
            kanun_numarasi = kanun_numarasi_match
            break  # Eşleşme bulunduğunda döngüyü sonlandırıyoruz


    kabul_tarihi = re.search(r'(?:K)abul (?:T)arihi\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})', text)
    if not kabul_tarihi:
        kabul_tarihi = re.search(r'(?:K)abul\s*(?:T|t)arih\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})', text)
    if not kabul_tarihi:
        kabul_tarihi = re.search(r'(?:K)abul\s*(?:t)arihi\s*:?\s*([\d\s/]+)', text)
        
        # Eğer küçük "t" ile yazılmış ise, kabul_tarihi'ni güncelleyip fazla boşlukları kaldırıyoruz
        if kabul_tarihi:
            kabul_tarihi = re.sub(r'\s+', '', kabul_tarihi.group(1))  # Tarihteki fazla boşlukları kaldırıyoruz
    else:
        # Eğer büyük "T" ile yazılmış bir tarih bulduysak, doğrudan group(1) ile kabul_tarihi'ni alıyoruz
        kabul_tarihi = kabul_tarihi.group(1)
    

    resmi_gazete_tarihi_patterns = [
    r'Yayımlandığı\s*Resmî Gazete\s*:?\s*(?:Tarih|Tarihi)?\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',     # Standart format (gün/ay/yıl)
    r'Yayımlandığı\s*Resmî\s*Gazede\s*:?\s*(?:Tarih|Tarihi)?\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',  # Resmî Gazede (tipografi hatası)
    r'Yayımlandğı\s*Resmî\s*Gazete\s*:?\s*Tarih\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',              # Yayımlandğı Resmî Gazete
    r'Yayımlandığı\s*R\.\s*Gazete\s*:?\s*Tarih\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',              # R. Gazete formatı
    r'Yayınlandığı\s*Resmî\s*Gazete\s*:?\s*Tarih\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',            # Yayınlandığı Resmî Gazete
    r'Yayımladığı\s*Resmî\s*Gazete\s*:?\s*Tarih\s*:?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',             # Yayımladığı Resmî Gazete
     # İstisna 1: Birden fazla tarih aralığı içeren durum (örneğin: "Tarih: 29, 30, 31/7/1964-1/8/1964")
    r'Tarih\s*:\s*(\d{1,2},\s*\d{1,2},\s*\d{1,2}/\d{1,2}/\d{4}-\d{1,2}/\d{1,2}/\d{4})',

    # İstisna 2: Çift eğik çizgi içeren durum (örneğin: "Tarih : 22/11//2008")
    r'Tarih\s*:\s*(\d{1,2}/\d{1,2}//\d{4})'
    ]

    # Resmî Gazete tarihini yakalamak için regex desenlerini sırayla deniyoruz
    resmi_gazete_tarihi = None
    for pattern in resmi_gazete_tarihi_patterns:
        resmi_gazete_tarihi_match = re.search(pattern, text)
        if resmi_gazete_tarihi_match:
            resmi_gazete_tarihi = resmi_gazete_tarihi_match  # Eşleşen tüm tarihi alıyoruz
            break  # Eşleşme bulunduğunda döngüyü sonlandırıyoruz

    
    resmi_gazete_sayisi = re.search(r'(?:S)ayı\s*:?\s*(\d+)', text)

    if not resmi_gazete_sayisi:
        resmi_gazete_sayisi = re.search(r'(?:S)ayısı\s*:?\s*(\d+)', text)
    if not resmi_gazete_sayisi:
        resmi_gazete_sayisi = re.search(r'Tarih\s*:\s*[\d/]+\s*Sayfa\s*:?\s*(\d+)', text)
    if not resmi_gazete_sayisi:
        resmi_gazete_sayisi = re.search(r'(?:S)ayı\s*:?\s*\w+,?\s*(\d+)', text)

    dustur_info = re.search(r'Yayımlandığı\s*Düstur\s*:?\s*Tertip\s*:\s*(\d+)\s*Cilt\s*:\s*(\d+)\s*(?:Sayfa|Sh\.)\s*:\s*(\d+)', text)

    # İlk olarak "Tertip" bilgisini kontrol ediyoruz
    tertip_info = re.search(r'Tertip\s*:\s*(\d+)', text)
    if not tertip_info:
        tertip_info = re.search(r'Tertibi\s*:\s*(\d+)', text)
    # "Cilt" bilgisini kontrol ediyoruz
    cilt_info = re.search(r'Cilt\s*:\s*(\d+)', text)

    # "Sayfa" ya da "Sh." bilgisini kontrol ediyoruz
    sayfa_info = re.search(r'(?:Sayfa|Sh\.)\s*:\s*(\d+)', text)

    # Eğer her biri bulunmuşsa, ilgili bilgileri alıyoruz
    tertip = tertip_info.group(1) if tertip_info else None
    cilt = cilt_info.group(1) if cilt_info else None
    sayfa = sayfa_info.group(1) if sayfa_info else None
    
    # Madde ve Geçiçi Maddeleri Yakalıyoruz
    maddeler = re.findall(r"((?:MADDE|Madde|GEÇİCİ MADDE|Geçici Madde)\s*\d+.*?)(?=\s*(?:MADDE|Madde|GEÇİCİ MADDE|Geçici Madde)\s*\d+|$)", text, re.DOTALL)


    # Ayrıştırılmış veriyi ekle
    parsed_entry = {
        "url": entry["url"],
        "Kanun Adı": kanun_adi.strip() if kanun_adi else None,
        "kanun_numarasi": kanun_numarasi.group(1) if kanun_numarasi else None,
        "kabul_tarihi": kabul_tarihi,
        "resmi_gazete": {
            "tarih": resmi_gazete_tarihi.group(1) if resmi_gazete_tarihi else None,
            "sayi": resmi_gazete_sayisi.group(1) if resmi_gazete_sayisi else None
        },
        "dustur": {
            "tertip": tertip,
            "cilt": cilt,
            "sayfa": sayfa
        },
        "maddeler": []
    }

    for madde in maddeler:
         doc = nlp(madde)
         madde_numarasi = re.search(r"((?:MADDE|Madde|GEÇİCİ MADDE|Geçici Madde)\s*\d+)", madde)
         madde_text = madde[madde_numarasi.end():].strip() if madde_numarasi else madde.strip()
         
         # Madde numarasından sonraki "-" işaretini ve başındaki boşlukları kaldır
         madde_numarasi_text = madde_numarasi.group(1).replace("-", "").strip() if madde_numarasi else None
         madde_text = re.sub(r'^\s*-\s*', '', madde_text)
         
         parsed_entry["maddeler"].append({
             "madde_numarasi": madde_numarasi_text,
             "text": madde_text
         })

    # Ayrıştırılmış veriyi listeye ekle
    parsed_data.append(parsed_entry)

# Ayrıştırılmış veriyi yeni bir JSON dosyasına yaz
output_file = 'parsed_output.json'  # Çıktı dosyasının adı
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(parsed_data, outfile, ensure_ascii=False, indent=4)

print(f"Ayrıştırılmış veri '{output_file}' dosyasına kaydedildi.")