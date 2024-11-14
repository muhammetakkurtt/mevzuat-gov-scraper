# Mevzuat-Gov Scraper

Bu proje, belirlediğiniz yıllar arasında yayımlanan mevzuatlar/kanunlar için [mevzuat.gov](https://mevzuat.gov.tr) tarayıp içeriklerini almanızı sağlayan bir web scraping uygulamasıdır. Scrapy ve Selenium teknolojilerini kullanarak mevzuat verilerini toplar ve JSON formatında çıktı üretir.

## İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
  - [GUI Arayüzü Verileri Kazıma](#gui-arayüzü-verileri-kazıma)
  - [Mevzuat Verilerini Ayrıştırma](#mevzuat-verilerini-ayrıştırma)
- [Dosyalar](#dosyalar)
- [Mevzuat Verileri](#mevzuat-verileri)
- [Kullanılan Teknolojiler ve Atıf](#kullanılan-teknolojiler-ve-atıf)
- [Hatalar ve Geliştirme Alanları](#hatalar-ve-geliştirme-alanları)
- [Meta](#meta)

## Özellikler

- Belirli yıllar arasında yayımlanan mevzuatları tarar.
- İki farklı veri çekme yöntemi sunar:
  - Tam Metin: Mevzuatın tam içeriğini çeker (Selenium kullanır)
  - Meta Veri: Sadece özet bilgileri çeker 
- Mevzuat türü seçimi (Kanun, Tüzük, Yönetmelik vb.)
- Mevzuatın tam metnini web sitesinden çeker ve JSON formatında kaydeder.
- Selenium ile tarayıcıyı kontrol eder, Scrapy ile sayfaları kazır.
- Başlangıç ve bitiş yıllarını Tkinter tabanlı GUI ile girebilirsiniz.
- Tek bir yıl ya da tüm yıllar arasındaki mevzuatı seçebilirsiniz.
- Toplanan mevzuatların metinlerini regex ve doğal dil işleme (NLP) ile ayrıştırır.
- Kanun adı, kanun numarası, kabul tarihi, resmi gazete bilgileri ve kanun maddelerini çıkarır.
- Çıktıyı JSON formatında sunar.

## Kurulum

### Adım 1: Gerekli Paketlerin Yüklenmesi
Proje Python 3.11.9 sürümü ile test edilmiştir.
Projeyi çalıştırmadan önce, gerekli Python paketlerini yüklemeniz gerekmektedir. Aşağıdaki komut ile gerekli paketleri yükleyebilirsiniz:

```bash
pip install -r requirements.txt
```

Gerekli paketler:
- `Scrapy`
- `Selenium`
- `BeautifulSoup4`
- `CustomTkinter`
- `webdriver_manager`
- `spacy`
- `tqdm`
- `git-lfs`
- `requests`
- `numpy`

### Adım 2: Selenium WebDriver

Selenium'un çalışması için tarayıcı sürücüsüne ihtiyacınız olacak. Chrome kullanıyorsanız, `webdriver_manager` paketi otomatik olarak en uygun sürücüyü indirecektir. Proje, bu işlemi otomatik hale getirmek için gerekli ayarları içerir.

## Kullanım
1. Clone this repository
2. Move to the `mevzuat-gov-scraper` directory
### GUI Arayüzü Verileri Kazıma

Proje, kullanıcının başlangıç ve bitiş yılını girerek kolayca Scrapy örümceğini başlatabileceği bir GUI arayüzü sunar. GUI'yi başlatmak için şu komutu çalıştırabilirsiniz:

```bash
python main.py
```
GUI üzerinden iki tür veri çekebilirsiniz:
1. **Tam Metin**: Mevzuatın tam içeriğini çeker (Selenium kullanır)
2. **Meta Veri**: Sadece özet bilgileri çeker

Her iki seçenek için de:
- Belirli yıllar arasındaki verileri çekebilir
- Tüm yılların verilerini çekebilirsiniz

Meta veri çekimi için mevzuat türünü seçebilirsiniz:
- Kanun
- Cumhurbaşkanlığı Kararnamesi
- Tüzük
- Yönetmelik
- ve diğerleri...

### Mevzuat Verilerini Ayrıştırma
Toplanan mevzuat verilerini ayrıştırmak için mevzuat_parser.py dosyası kullanılır. JSON dosyasındaki ham verileri işler, regex ve doğal dil işleme (NLP) yöntemleriyle kanun adı, kanun numarası, kabul tarihi, resmi gazete bilgileri ve kanun maddelerini çıkarır. Ayrıştırma işlemini başlatmak için şu komutu çalıştırabilirsiniz:
```bash
python data_processing/mevzuat_parser.py
```
Dil modeli olarak [tr_core_news_lg](https://huggingface.co/turkish-nlp-suite/tr_core_news_lg) tercih edilmiştir. Betiği çalıştırdığınızda eğer kurulu değilse bulunduğu dizine indirmek için izin isteyecektir.

## Dosyalar

- `main.py`: Projenin ana dosyasıdır. Kullanıcı arayüzünü başlatır ve Scrapy örümceğini çalıştırır.
- `mevzuat_parser.py`: JSON dosyasındaki ham veriyi parse eden ve ayrıştıran Python betiğidir.
- `mevzuat_spider.py`: Scrapy framework'ü ile web sitesinden mevzuatları kazıyan örümceği içerir.
## Mevzuat Verileri
Bu projede kullanılan mevzuat verilerine Hugging Face üzerinde ulaşabilirsiniz:

### Mevzuat-Gov Dataset
[Mevzuat-Gov Dataset on Hugging Face](https://huggingface.co/datasets/muhammetakkurt/mevzuat-gov-dataset)

Bu veri kümesini kullanarak, 2024 Eylül ayına kadar yayımlanan mevzuatları inceleyebilirsiniz. Veri kümesi, JSON formatında mevzuat metinlerini içermekte olup, kanun adı, kanun numarası, kabul tarihi ve diğer yasal bilgileri içermektedir. Hatalı veya eksik kanun başlıkları ve bazı kısımlar manuel olarak düzeltilmiştir.
## Kullanılan Teknolojiler ve Atıf
Bu proje, doğal dil işleme (NLP) süreçlerinde, Google Developer Experts Programı tarafından desteklenen Duygu 2022 Fall-Winter koleksiyonunun bir parçası olan "Turkish NLP with Duygu" modellerini kullanmaktadır.
### Makale Referansı:
Altinok, Duygu. (2023). A Diverse Set of Freely Available Linguistic Resources for Turkish. Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 13739–13750. Toronto, Canada: Association for Computational Linguistics.
https://aclanthology.org/2023.acl-long.768
## Hatalar ve Geliştirme Alanları

### Bilinen Hatalar
- **Tarayıcı Uyumsuzluğu**: Selenium yalnızca Chrome tarayıcısı ile test edilmiştir. Farklı tarayıcılar için ek ayarlamalar gerekebilir.

### Geliştirme Alanları
- **Veri Temizliği**: Mevzuat metinlerinin bazı bölümlerinde ekstra karakterler ve hatalı biçimlendirmeler olabilir. Regex ve NLP işlemleri daha iyi sonuçlar verecek şekilde geliştirilebilir.
- **Gelişmiş NLP**: NLP modelinin, çıkarılan kanun maddelerindeki daha karmaşık yapıların anlaşılması için geliştirilebilmesi.

## Meta
Yazar: Muhammet Akkurt  
Email: muhammetakkurtt@icloud.com

MIT lisansı altında dağıtılır. Daha fazla bilgi için [LICENSE](./LICENSE) bölümüne bakınız.
