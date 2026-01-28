# Cisco CUBE Active Voice Traffic Analyzer

Bu proje, Cisco CUBE (Unified Border Element) üzerinden geçen aktif ses trafiğini gerçek zamanlı olarak analiz eden ve anlamlı bir rapor sunan Python tabanlı bir araçtır. 

Özellikle yoğun çağrı trafiği olan santrallerde, çağrı bacaklarını (Call Legs) birbirleriyle eşleştirerek "Arayan" ve "Aranan" bilgisini hatasız bir şekilde raporlar.

## Özellikler

- **Akıllı Eşleştirme:** Call ID atlamalarını tolere ederek çağrı bacaklarını birbirine bağlar.
- **Gerçek Zamanlı Durum:** Çağrıların `ACTIVE` (Görüşme devam ediyor) veya `CONNECTING` (Çalıyor) durumlarını anlık analiz eder.
- **Router Zaman Damgası:** Python sistem saati yerine, Router üzerindeki gerçek çağrı başlangıç zamanını raporlar.
- **Otomatik Filtreleme:** Sadece cep telefonu aramalarını ayıklayarak karmaşık loglar arasında kaybolmanızı önler.
- **Özet Rapor:** Listenin sonunda toplam aktif çağrı sayısını sunar.

## Örnek Çıktı

```text
--- 192.168.1.1 Gerçek Zamanlı Aktif Çağrı Raporu ---
TARİH / SAAT         | DURUM        | ARAYAN (DAHİLİ)      | ARANAN CEP
-----------------------------------------------------------------------
28.01.2026 13:45:12  | ACTIVE       | 02123136685          | 05354543296
28.01.2026 13:45:30  | ACTIVE       | 4881515              | 0542407XXXX
28.01.2026 13:46:05  | CONNECTING   | 02164215218          | 0505214XXXX
28.01.2026 13:46:18  | ACTIVE       | 3127044              | 0541747XXXX
-----------------------------------------------------------------------
TOPLAM AKTİF CEP ARAMASI: 4

```


## Gereksinimler
- **Python 3.x:** Projenin temel çalışma ortamı.
- **Netmiko:** Cisco cihazlarına SSH üzerinden bağlanmak ve komut çalıştırmak için kullanılan kütüphane.
- **Cisco Gateway Erişimi:** CUBE cihazına SSH erişim yetkisi olan bir kullanıcı hesabı.
```bash
pip install -r requirements.txt
```

