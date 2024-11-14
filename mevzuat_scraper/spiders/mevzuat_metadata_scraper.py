import requests
import json
from time import sleep
from tqdm import tqdm

class MevzuatMetadataScraper:
    MEVZUAT_TURLERI = {
        "Kanun": {"MevzuatTur": "Kanun", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Cumhurbaşkanlığı Kararnamesi": {"MevzuatTur": "CumhurbaskaniKararnameleri", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Cumhurbaşkanlığı ve Bakanlar Kurulu Yönetmeliği": {"MevzuatTur": "CumhurbaskanligiVeBakanlarKuruluYonetmelik", "YonetmelikMevzuatTur": "CumhurbaskanligiVeBakanlarKuruluYonetmelik"},
        "Cumhurbaşkanı Kararları": {"MevzuatTur": "CumhurbaskaniKararlari", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Cumhurbaşkanlığı Genelgeleri": {"MevzuatTur": "CumhurbaskanligiGenelgeleri", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Kanun Hükmünde Kararname": {"MevzuatTur": "KHK", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Tüzük": {"MevzuatTur": "Tuzuk", "YonetmelikMevzuatTur": "OsmanliKanunu"},
        "Kurum ve Kuruluş Yönetmeliği": {"MevzuatTur": "KurumVeKurulusYonetmeligi", "YonetmelikMevzuatTur": "KurumKurulusVeUniversiteYonetmelik"},
        "Tebliğ": {"MevzuatTur": "Teblig", "YonetmelikMevzuatTur": "OsmanliKanunu"}
    }

    def __init__(self):
        self.base_url = 'https://mevzuat.gov.tr/Anasayfa/MevzuatDatatable'
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_data(self, start_year=None, end_year=None, mevzuat_turu="Kanun", page_size=20, max_retries=3):
        all_data = []
        current_page = 0
        retry_count = 0
        
        # Mevzuat türü bilgilerini al
        mevzuat_bilgisi = self.MEVZUAT_TURLERI.get(mevzuat_turu, self.MEVZUAT_TURLERI["Kanun"])
        
        initial_payload = {
            "draw": 1,
            "order": [],
            "start": 0,
            "length": page_size,
            "search": {"value": "", "regex": False},
            "parameters": {
                "MevzuatTur": mevzuat_bilgisi["MevzuatTur"],
                "YonetmelikMevzuatTur": mevzuat_bilgisi["YonetmelikMevzuatTur"],
                "AranacakIfade": "",
                "AranacakYer": "2",
                "MevzuatNo": "",
                "BaslangicTarihi": str(start_year) if start_year else "",
                "BitisTarihi": str(end_year) if end_year else ""
            }
        }
        
        try:
            response = self.session.post(self.base_url, headers=self.headers, json=initial_payload)
            response.raise_for_status()
            total_records = response.json().get('recordsTotal', 0)
            print(f"\nToplam {total_records} kayıt bulundu.")
            
            # İlerleme çubuğunu oluştur
            progress_bar = tqdm(total=total_records, desc="Veriler çekiliyor")
            
            while True:
                payload = initial_payload.copy()
                payload["start"] = current_page * page_size
                payload["draw"] = current_page + 1
                
                try:
                    response = self.session.post(self.base_url, headers=self.headers, json=payload)
                    response.raise_for_status()
                    
                    try:
                        data = response.json()
                    except json.JSONDecodeError as e:
                        if retry_count < max_retries:
                            print(f"\nJSON çözümleme hatası, yeniden deneniyor ({retry_count + 1}/{max_retries})...")
                            retry_count += 1
                            sleep(2)  # Yeniden denemeden önce biraz bekle
                            continue
                        else:
                            print(f"\nJSON çözümleme hatası: {e}")
                            break
                    
                    retry_count = 0  # Başarılı istek sonrası sayacı sıfırla
                    
                    if not data.get('data'):
                        break
                    
                    new_records = data['data']
                    all_data.extend(new_records)
                    
                    # İlerleme çubuğunu güncelle
                    progress_bar.update(len(new_records))
                    
                    if (current_page + 1) * page_size >= total_records:
                        break
                    
                    current_page += 1
                    sleep(1)  # Sunucuyu yormamak için bekleme
                    
                except requests.RequestException as e:
                    if retry_count < max_retries:
                        print(f"\nBağlantı hatası, yeniden deneniyor ({retry_count + 1}/{max_retries})...")
                        retry_count += 1
                        sleep(2)
                        continue
                    else:
                        print(f"\nBağlantı hatası: {e}")
                        break
            
            progress_bar.close()
            print(f"\nToplam {len(all_data)} kayıt başarıyla alındı.")
            
        except requests.RequestException as e:
            print(f"İlk istek başarısız oldu: {e}")
        
        return all_data

    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
