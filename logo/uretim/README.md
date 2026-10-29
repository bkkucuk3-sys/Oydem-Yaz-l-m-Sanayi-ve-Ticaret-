# Logo üretim betikleri

Oydem logosunun (v20) SVG dosyalarını kodla üretir; böylece küre, D, limanlar ve yerleşim üzerinde değişiklik yapılabilir.

- `logo_uret.py` — ana üretici. `python3 logo/uretim/logo_uret.py [çıktı_klasörü]` açık, koyu ve tek renk yatay logo ile kare ikonları yazar.
- `marka_kiti_logolari.py` — `marka-kiti/01-logo` içindeki şeffaf SVG'leri üretir.

Gereken: Python 3 ve `pip install fonttools`. Fontlar `marka-kiti/fontlar` içinden okunur.
SVG'den PNG'ye dönüştürmek için herhangi bir araç (Playwright, Inkscape, tarayıcı) kullanılabilir.

Önemli parametreler `logo_uret.py` içinde: `mark()` (D'nin kalınlığı `stroke-width`, liman sayısı/yeri `centres`, boşluk genişliği `H`), `globe()` (kare sıklığı `nlat/nlon`, dağılma `t`), `logo()` (yerleşim ve yazı).
