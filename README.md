

# 🛰️ Cosmic-Telemetry-Sanitizer: Kozmik Veri Ayıklama ve İşleme Hattı

![Project Banner](assets/banner.png)



![TUA Astrohackathon](https://img.shields.io/badge/Etkinlik-TUA_Astrohackathon-0052cc?style=flat-square)

![Milli Uzay Programı](https://img.shields.io/badge/Hedef-Mühendislik_ve_Yazılım-e60000?style=flat-square)

![Sürüm](https://img.shields.io/badge/Sürüm-v1.0.0--beta-orange?style=flat-square)

![Teknoloji](https://img.shields.io/badge/Teknoloji-Data_Engineering_%7C_Kalman_Filters_%7C_AI-2ea44f?style=flat-square)



## 📌 Yüksek Düzey Özet

**Cosmic-Telemetry-Sanitizer**, yörüngedeki veya derin uzaydaki araçlardan yer istasyonuna inen (downlink) telemetri verilerindeki radyasyon kaynaklı anormallikleri otonom olarak tespit eden, filtreleyen ve temizlenmiş veriyi yeniden inşa eden çok katmanlı bir veri işleme (Data Pipeline) ve arındırma (Sanitization) hattıdır.



Sistem; galaktik kozmik ışınlar ve Güneş patlamalarının mikroçiplerde yarattığı "Tekil Olay Bozulmaları"nı (SEU - Single Event Upset / Bit-Flips), istatistiksel filtreler ve gözetimsiz makine öğrenmesi algoritmaları kullanarak tespit eder. Böylece uydunun sağlık durumu (State of Health) verilerindeki ölümcül yanılsamalar, uydunun fiziksel dinamiklerine uygun olarak otonom bir şekilde düzeltilir.



---



## 🎯 Problem Tanımı ve Mühendislik Kısıtları

Uzay radyasyonu, mikrodenetleyicilerin belleklerindeki bitlerin (0 ve 1'lerin) anlık olarak yön değiştirmesine neden olur. Bu durum, yer istasyonuna ulaşan veri paketlerinde kritik anomalilere yol açar:

1. **Fiziksel İmkansızlıklar (Point Anomalies):** Uydunun batarya voltajının milisaniyeler içinde 28V'tan 400V'a çıkıp tekrar normal seviyesine inmesi.

2. **Bağlamsal Bozulmalar (Contextual Anomalies):** Sensör okumalarının fiziksel sınırlar içinde kalmasına rağmen, uydunun genel dinamiğiyle uyuşmayan sistematik sensör gürültüleri.



Klasik alt-üst sınır (threshold) uyarı sistemleri bu durumlarda gereksiz alarmlar (False Positives) üreterek operasyonel körlüğe neden olur. Bu sorunun, veriyi bağlamına göre anlayan dinamik bir "veri temizleme mimarisi" ile çözülmesi şarttır.



---



## 🧠 Teknik Yaklaşım ve Sistem Mimarisi (Pipeline Katmanları)

Veri işleme hattı, ham telemetri verisini alıp 5 aşamalı bir filtreden geçirerek "Temiz Veri Havuzuna" (Data Lake) aktarır:

### 1. Katman: İstatistiksel Filtreleme (Spike Removal)
Median Absolute Deviation (MAD) kullanılarak, donanımsal bit kaymalarının yarattığı anlık, fiziksel olarak imkansız "Spike" (sıçrama) gürültüleri tespit edilir ve budanır.

### 2. Katman: Dinamik Durum Kestirimi (Kalman Filtresi)
Fiziksel sensörler için 1D Adaptif Kalman Filtresi uygulanır. Sistem, sensörün bir önceki durumuna bakarak gürültüyü sönümler ve sinyal stabilitesini sağlar.

### 3. Katman: Çok Değişkenli AI Anomali Tespiti
Gözetimsiz Öğrenme (Isolation Forest) modeli kullanılır. Sensörler arası korelasyon bozulmalarını (örneğin akım yüksek ama durum kapalı) tespit eder.

### 4. Katman: Spektral Arındırma (Butterworth Filter)
Kalan yüksek frekanslı salınım gürültülerini Butterworth Alçak Geçiren Filtre kullanarak temizler. Sinyalin pürüzsüzleşmesini sağlar.

### 5. Katman: Fiziksel Sınır Doğrulama (Safety Bounds)
Domain-specific kurallara göre (Örn: Batarya 10V-36V arası olmalı) veriyi nihai olarak doğrular ve fiziksel imkansızlıkları "clamp" eder.

---

## 📂 Depo Yapısı (Repository Structure)

```text
Cosmic-Telemetry-Sanitizer/
├── app.py                      # Interaktif Streamlit Dashboard
├── config/
│   └── settings.json           # Pipeline parametreleri (Window sizes, bounds)
├── data/
│   ├── raw_telemetry/          # Ham veri (anomali içerir)
│   └── sanitized_telemetry/    # Temizlenmiş operasyonel veri
├── docs/
│   └── SYSTEM_DESIGN.md        # Matematiksel ve mimari detaylar
├── pipeline/
│   ├── step1_mad_filter.py
│   ├── step2_kalman_smooth.py
│   ├── step3_autoencoder.py
│   ├── step4_spectral_denoise.py
│   └── step5_physical_bounds.py
├── scripts/
│   ├── cli.py
│   └── generate_data.py
├── requirements.txt
└── README.md
```



---



## 🛠️ Kurulum ve Test (Prototiplendirme)

Geliştirilen veri arındırma hattını kendi makinenizde test etmek için:

```bash
# Depoyu klonlayın
git clone https://github.com/kullaniciadi/Cosmic-Telemetry-Sanitizer.git
cd Cosmic-Telemetry-Sanitizer

# Gerekli bağımlılıkları yükleyin
pip install -r requirements.txt

# Sentetik veri üretin
python scripts/generate_data.py --output-dir data/raw_telemetry

# Tam pipeline'ı çalıştırın
python scripts/cli.py run-pipeline --input data/raw_telemetry/sample_orbit_data.csv --output-dir data/processed

# Sonuçları görselleştirin
python scripts/cli.py visualize --input data/processed/kalman_smoothed.csv
```

## 📦 Kullanım (CLI)

Proje, bir komut satırı arayüzü (`cosmic-sanitizer`) sunar:

```bash
# Yardım menüsü
python scripts/cli.py -h

# Veri üretimi
python scripts/cli.py generate-data --output-dir data/raw_telemetry

# Pipeline çalıştırma (isteğe bağlı adım atlama)
python scripts/cli.py run-pipeline --input data/raw_telemetry/sample_orbit_data.csv --output-dir data/processed --skip-step mad

# Görselleştirme
python scripts/cli.py visualize --input data/processed/kalman_smoothed.csv
```

---

## 📈 Gelecek Vizyonu

- [ ] **Gerçek Zamanlı Akış (Real-Time Stream):** Apache Kafka entegrasyonu ile yer istasyonuna akan telemetrinin asenkron ve milisaniye seviyesinde temizlenmesi.

- [ ] **Yazılım-Donanım Hibrit ECC:** Bu yazılımsal filtrelemenin, donanım seviyesindeki Hata Düzeltme Kodları (Reed-Solomon, Hamming) ile entegre çalışarak çift katmanlı bir güvenlik protokolü oluşturması.



---



## 👨‍💻 Geliştirici

Bu proje, **TUA Astrohackathon** etkinliği kapsamında uzay mühendisliği problemlerini gelişmiş veri analitiği ile otonomlaştırmak amacıyla tasarlanmıştır.



**Tasarım ve Geliştirme:** Multi-Disciplinary Systems Designer | Solopreneur | AI & Endüstriyel Optimizasyon

```

