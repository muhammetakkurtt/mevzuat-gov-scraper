import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 'spiders' klasörünü Python'un modül arama yoluna ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'mevzuat_scraper', 'spiders'))

# mevzuat_spider modülünü içe aktar
from mevzuat_spider import MevzuatSeleniumSpider

# Scrapy örümceğini başlatan fonksiyon
def run_spider(start_year=None, end_year=None):
    settings = get_project_settings()

    # Çıktıyı formatını kaydetmek için FEEDS ayarını belirle
    settings.set('FEEDS', {
        'mevzuat.json': {
            'format': 'json',
            'encoding': 'utf8',
            'overwrite': True
        }
    })

    # Scrapy örümceğini başlat
    process = CrawlerProcess(settings)
    process.crawl(MevzuatSeleniumSpider, start_year=start_year, end_year=end_year)
    process.start()

# Başlangıç ve bitiş yılı girişlerini almak için Tkinter GUI
def start_gui():
    def on_submit():
        start_year = entry_start_year.get()
        end_year = entry_end_year.get()

        current_year = datetime.now().year  # İçinde bulunduğumuz yılı al

       
        if not start_year or not end_year:
            messagebox.showerror("Hata", "Başlangıç ve Bitiş yılı boş bırakılamaz.")
            return

       
        if not start_year.isdigit() or not end_year.isdigit():
            messagebox.showerror("Hata", "Yıllar sayısal olmalı.")
            return

        start_year = int(start_year)
        end_year = int(end_year)

        
        if start_year < 1900:
            messagebox.showerror("Hata", "Başlangıç yılı en az 1900 olmalıdır.")
            return

        
        if end_year > current_year:
            messagebox.showerror("Hata", f"Bitiş yılı en fazla {current_year} olabilir.")
            return

        if start_year > end_year:
            messagebox.showerror("Hata", "Başlangıç yılı, bitiş yılından büyük olamaz.")
            return

        # GUI'yi kapatıp Scrapy botunu çalıştır
        root.destroy()
        run_spider(start_year, end_year)

    def fetch_all():
        
        root.destroy()
        run_spider()

    # CustomTkinter ayarları
    ctk.set_appearance_mode("System")  # "System", "Dark" or "Light"
    ctk.set_default_color_theme("blue")  # Temayı belirleyin

    root = ctk.CTk()  # Tk() yerine CTk() kullanıyoruz
    root.title("Mevzuat Scraper")
    root.geometry("450x300")

    # Başlangıç Yılı Girişi
    label_start_year = ctk.CTkLabel(root, text="Başlangıç Yılı (min: 1900):",font=("Arial", 18))
    label_start_year.grid(row=0, column=0, padx=20, pady=20)
    entry_start_year = ctk.CTkEntry(root)
    entry_start_year.grid(row=0, column=1, padx=20, pady=20)

    # Bitiş Yılı Girişi
    label_end_year = ctk.CTkLabel(root, text=f"Bitiş Yılı (max: {datetime.now().year}):",font=("Arial", 18))
    label_end_year.grid(row=1, column=0, padx=20, pady=20)
    entry_end_year = ctk.CTkEntry(root)
    entry_end_year.grid(row=1, column=1, padx=20, pady=20)

    # Yıl aralığını kullanarak arama butonu
    submit_button = ctk.CTkButton(root, text="Yıl Aralığına Göre Ara", command=on_submit, width=200, height=50,font=("Arial", 18))
    submit_button.grid(row=2, column=0, columnspan=21, padx=10, pady=10)

    # Tüm kanunları çekmek için buton
    all_button = ctk.CTkButton(root, text="Tüm Kanunları Çek", command=fetch_all, width=200, height=50,font=("Arial", 18))
    all_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    start_gui()
