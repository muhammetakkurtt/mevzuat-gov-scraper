# Mevzuat-Gov Scraper

Bu proje, belirlediğiniz yıllar arasında yayımlanan mevzuatlar/kanunlar için [mevzuat.gov](https://mevzuat.gov.tr) tarayıp içeriklerini almanızı sağlayan bir web scraping uygulamasıdır. Scrapy ve Selenium teknolojilerini kullanarak mevzuat verilerini toplar ve JSON formatında çıktı üretir.

## İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
  - [GUI Arayüzü ile Kullanım](#gui-arayüzü-ile-kullanım)
  - [Mevzuat Verilerini Ayrıştırma](#mevzuat-verilerini-ayrıştırma)
- [Dosyalar](#dosyalar)
- [Gereksinimler](#gereksinimler)
- [İletişim](#iletişim)

## Özellikler

- Belirli yıllar arasında yayımlanan mevzuatları tarar.
- Mevzuatın tam metnini web sitesinden çeker ve JSON formatında kaydeder.
- Selenium ile tarayıcıyı kontrol eder, Scrapy ile sayfaları kazır.
- Başlangıç ve bitiş yıllarını Tkinter tabanlı GUI ile girebilirsiniz.
- Tek bir yıl ya da tüm yıllar arasındaki mevzuatı seçebilirsiniz.
- Toplanan mevzuatların metinlerini regex ve doğal dil işleme (NLP) ile ayrıştırır.
- Kanun adı, kanun numarası, kabul tarihi, resmi gazete bilgileri ve kanun maddelerini çıkarır.
- Çıktıyı JSON formatında sunar.

## Kurulum

### Adım 1: Gerekli Paketlerin Yüklenmesi

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
Başlatıldığında, açılan pencerede başlangıç ve bitiş yıllarını girin. Program girilen yıllar arasındaki tüm mevzuatları tarayıp kaydedecektir. Eğer tüm mevzuatları çekmek istiyorsanız "Tüm Kanunları Çek" butonuna basınız.
### Mevzuat Verilerini Ayrıştırma
Toplanan mevzuat verilerini ayrıştırmak için mevzuat_parser.py dosyası kullanılır. JSON dosyasındaki ham verileri işler, regex ve doğal dil işleme (NLP) yöntemleriyle kanun adı, kanun numarası, kabul tarihi, resmi gazete bilgileri ve kanun maddelerini çıkarır. Ayrıştırma işlemini başlatmak için şu komutu çalıştırabilirsiniz:
```bash
python data_processing/mevzuat_parser.py
```
## Dosyalar

- `main.py`: Projenin ana dosyasıdır. Kullanıcı arayüzünü başlatır ve Scrapy örümceğini çalıştırır.
- `mevzuat_parser.py`: JSON dosyasındaki ham veriyi parse eden ve ayrıştıran Python betiğidir.
- `mevzuat_spider.py`: Scrapy framework'ü ile web sitesinden mevzuatları kazıyan örümceği içerir.

## Hatalar ve Geliştirme Alanları

### Bilinen Hatalar
- **Tarayıcı Uyumsuzluğu**: Selenium yalnızca Chrome tarayıcısı ile test edilmiştir. Farklı tarayıcılar için ek ayarlamalar gerekebilir.

### Geliştirme Alanları
- **Veri Temizliği**: Mevzuat metinlerinin bazı bölümlerinde ekstra karakterler ve hatalı biçimlendirmeler olabilir. Regex ve NLP işlemleri daha iyi sonuçlar verecek şekilde geliştirilebilir.
- **Gelişmiş NLP**: NLP modelinin, çıkarılan kanun maddelerindeki daha karmaşık yapıların anlaşılması için geliştirilebilmesi.