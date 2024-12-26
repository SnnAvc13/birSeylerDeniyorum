import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
import customtkinter as ctk

class ModernPixelArtUygulamasi:
    def __init__(self):
        # Ana pencere ayarları
        self.root = ctk.CTk()
        self.root.title("Pixel Art Dönüştürücü")
        self.root.geometry("1000x700")
        self.root.configure(fg_color="#2b2b2b")
        
        # Tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Sol panel - Kontroller
        self.sol_panel = ctk.CTkFrame(self.root, corner_radius=10)
        self.sol_panel.pack(side="left", fill="y", padx=20, pady=20)
        
        # Logo ve başlık
        self.baslik = ctk.CTkLabel(
            self.sol_panel, 
            text="Pixel Art\nDönüştürücü",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        self.baslik.pack(pady=20)
        
        # Kontrol butonları
        self.resim_sec_btn = ctk.CTkButton(
            self.sol_panel,
            text="Resim Seç",
            command=self.resim_sec,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.resim_sec_btn.pack(pady=10, padx=20, fill="x")
        
        # Pixel boyutu ayarı
        self.boyut_frame = ctk.CTkFrame(self.sol_panel)
        self.boyut_frame.pack(pady=10, padx=20, fill="x")
        
        self.boyut_label = ctk.CTkLabel(
            self.boyut_frame,
            text="Pixel Boyutu:",
            font=ctk.CTkFont(size=12)
        )
        self.boyut_label.pack()
        
        self.pixel_boyutu = ctk.CTkSlider(
            self.boyut_frame,
            from_=2,
            to=64,
            number_of_steps=31,
            command=self.slider_event
        )
        self.pixel_boyutu.set(32)
        self.pixel_boyutu.pack(pady=5)
        
        self.boyut_deger = ctk.CTkLabel(
            self.boyut_frame,
            text="32",
            font=ctk.CTkFont(size=12)
        )
        self.boyut_deger.pack()
        
        # İşlem butonları
        self.donustur_btn = ctk.CTkButton(
            self.sol_panel,
            text="Dönüştür",
            command=self.donustur,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.donustur_btn.pack(pady=10, padx=20, fill="x")
        
        self.kaydet_btn = ctk.CTkButton(
            self.sol_panel,
            text="Kaydet",
            command=self.kaydet,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.kaydet_btn.pack(pady=10, padx=20, fill="x")
        
        # Sağ panel - Resim görüntüleme
        self.sag_panel = ctk.CTkFrame(self.root, corner_radius=10)
        self.sag_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Resim etiketleri
        self.orjinal_label = ctk.CTkLabel(
            self.sag_panel,
            text="Orijinal Resim",
            font=ctk.CTkFont(size=16)
        )
        self.orjinal_label.pack(pady=5)
        
        self.orjinal_frame = ctk.CTkFrame(self.sag_panel, fg_color="#1f1f1f")
        self.orjinal_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.orjinal_resim_label = ctk.CTkLabel(self.orjinal_frame, text="")
        self.orjinal_resim_label.pack(expand=True)
        
        self.pixel_label = ctk.CTkLabel(
            self.sag_panel,
            text="Pixel Art",
            font=ctk.CTkFont(size=16)
        )
        self.pixel_label.pack(pady=5)
        
        self.pixel_frame = ctk.CTkFrame(self.sag_panel, fg_color="#1f1f1f")
        self.pixel_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.pixel_resim_label = ctk.CTkLabel(self.pixel_frame, text="")
        self.pixel_resim_label.pack(expand=True)
        
        # Değişkenler
        self.orjinal_resim = None
        self.pixel_resim = None
        
    def slider_event(self, value):
        self.boyut_deger.configure(text=str(int(value)))
        
    def resim_sec(self):
        dosya_yolu = filedialog.askopenfilename(
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if dosya_yolu:
            try:
                self.orjinal_resim = Image.open(dosya_yolu)
                self.resim_goster(self.orjinal_resim, self.orjinal_resim_label)
                self.pixel_resim_label.configure(image=None)
                self.pixel_resim = None
            except Exception as e:
                messagebox.showerror("Hata", f"Resim yüklenirken hata oluştu: {str(e)}")
    
    def donustur(self):
        if self.orjinal_resim is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        pixel_boyutu = int(self.pixel_boyutu.get())
        
        # Resmi yeniden boyutlandır
        en = self.orjinal_resim.size[0] // pixel_boyutu
        boy = self.orjinal_resim.size[1] // pixel_boyutu
        
        kucuk_resim = self.orjinal_resim.resize((en, boy), Image.Resampling.NEAREST)
        self.pixel_resim = kucuk_resim.resize(
            (en * pixel_boyutu, boy * pixel_boyutu), 
            Image.Resampling.NEAREST
        )
        
        self.resim_goster(self.pixel_resim, self.pixel_resim_label)
    
    def resim_goster(self, resim, label):
        # Resmi pencereye sığacak şekilde yeniden boyutlandır
        max_boyut = (400, 250)
        gosterim_resmi = resim.copy()
        gosterim_resmi.thumbnail(max_boyut)
        
        # Tkinter'da göstermek için PhotoImage'e dönüştür
        tk_resim = ImageTk.PhotoImage(gosterim_resmi)
        label.configure(image=tk_resim)
        label.image = tk_resim
    
    def kaydet(self):
        if self.pixel_resim is None:
            messagebox.showwarning("Uyarı", "Önce bir resmi pixel art'a dönüştürün!")
            return
            
        dosya_yolu = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")]
        )
        if dosya_yolu:
            try:
                self.pixel_resim.save(dosya_yolu)
                messagebox.showinfo("Başarılı", "Resim başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Resim kaydedilirken hata oluştu: {str(e)}")
    
    def calistir(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernPixelArtUygulamasi()
    app.calistir() 