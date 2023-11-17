import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import json
from difflib import get_close_matches

class GelistirilmisYapayZeka:
    def __init__(self):
        # Veritabanı dosya adı
        self.veritabani_dosya = 'answers.json'
        # Veritabanını yükle
        self.veritabani = self.yukle_veritabani()

    def yukle_veritabani(self):
        try:
            with open(self.veritabani_dosya, 'r', encoding='utf-8') as dosya:
                return json.load(dosya)
        except FileNotFoundError:
            return {}

    def kaydet_veritabani(self):
        # Veritabanını kaydet
        with open(self.veritabani_dosya, 'w', encoding='utf-8') as dosya:
            json.dump(self.veritabani, dosya, ensure_ascii=False, indent=2)

    def cevap_ver(self, soru):
        soru = soru.lower()

        # Soru doğrudan veritabanında var mı kontrol et
        cevaplar = self.veritabani.get(soru, None)
        if cevaplar:
            secilen_cevap = random.choice(cevaplar)
            return secilen_cevap

        # Eğer doğrudan eşleşme yoksa benzer soruları kontrol et
        benzer_sorular = get_close_matches(soru, self.veritabani.keys(), n=1, cutoff=0.7)
        if benzer_sorular:
            benzer_soru = benzer_sorular[0]
            cevaplar = self.veritabani.get(benzer_soru, ["Bunu bilmiyorum. Lütfen başka bir soru sorun."])
            secilen_cevap = random.choice(cevaplar)
            return secilen_cevap

        return "Bunu bilmiyorum. Lütfen başka bir soru sorun."

    def egit(self, soru, cevaplar):
        # Soruyu ve cevapları öğren
        cevaplar = [cevap.strip() for cevap in cevaplar if cevap.strip()]
        if cevaplar:
            self.veritabani[soru.lower()] = cevaplar
            print("Yeni bilgi öğrenildi!")
            self.kaydet_veritabani()
        else:
            print("Boş cevaplar eğitilmedi.")

class YapayZekaArayuzu:
    def __init__(self, master):
        # Ana pencereyi başlat
        self.master = master
        self.master.title("Yapay Zeka Arayüzü")

        # Yapay zeka nesnesini başlat
        self.yapay_zeka = GelistirilmisYapayZeka()

        # Giriş frame'i
        self.input_frame = tk.Frame(self.master, bg='gray', padx=10, pady=10, bd=2, relief=tk.GROOVE)
        self.input_frame.pack(pady=10)

        # Giriş etiketi ve giriş kutusu
        self.input_label = tk.Label(self.input_frame, text="Siz:", font=('Arial', 12), bg='gray', fg='white')
        self.input_label.grid(row=0, column=0, padx=(0, 10))

        self.input_entry = tk.Entry(self.input_frame, font=('Arial', 12), bd=0, relief=tk.FLAT, width=30)
        self.input_entry.grid(row=0, column=1, padx=(0, 10))

        # Cevap frame'i
        self.answer_frame = tk.Frame(self.master, padx=10, pady=10, bd=2, relief=tk.GROOVE)
        self.answer_frame.pack(pady=10)

        # Soru sor butonu
        self.ask_button = tk.Button(self.master, text="Sor", command=self.cevap_ver, font=('Arial', 12), bg='lightblue', width=20)
        self.ask_button.pack(pady=10)

        # Cevap etiketi
        self.answer_label = tk.Label(self.answer_frame, text="", font=('Arial', 14), bd=10, relief=tk.GROOVE, wraplength=400)
        self.answer_label.pack()

        # Klavye üzerinde "Enter" tuşuna basıldığında cevap ver
        self.master.bind('<Return>', self.cevap_ver)

    def cevap_ver(self, event=None):
        # Kullanıcının girdiği soruyu al ve yapay zekadan cevap al
        soru = self.input_entry.get().strip()
        cevap = self.yapay_zeka.cevap_ver(soru)

        # Cevabı etikete yaz ve giriş kutusunu temizle
        self.answer_label.config(text=f"Yapay Zeka: {cevap}")
        self.input_entry.delete(0, tk.END)

        # Eğer cevap bilinmiyorsa, kullanıcıya eğitme seçeneğini sun
        if cevap == "Bunu bilmiyorum. Lütfen başka bir soru sorun.":
            self.egit_popup(soru)

    def egit_popup(self, soru):
        # Kullanıcıdan yeni cevapları al ve yapay zekayı eğit
        cevaplar = self.ask_for_user_answers(soru)

        if cevaplar is not None:
            self.yapay_zeka.egit(soru, cevaplar)
            messagebox.showinfo("Başarılı", "Yapay zeka başarıyla eğitildi!")

    def ask_for_user_answers(self, soru):
        # Kullanıcıdan cevapları al
        user_input = simpledialog.askstring("Yeni Cevap Ekle", f"Lütfen \"{soru}\" için doğru cevapları virgülle ayırarak girin:")

        if user_input:
            return user_input.split(',')
        return None

def main():
    root = tk.Tk()
    app = YapayZekaArayuzu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
