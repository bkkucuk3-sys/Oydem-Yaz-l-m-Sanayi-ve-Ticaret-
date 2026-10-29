# Oydem Yazılım – proje notları

Sahibi: Oydem Yazılım Sanayi ve Ticaret Limited Şirketi (ithalat/ihracat + yapay zeka). Dil: Türkçe konuşulur.
Bu depo şirketin logo ve marka kitini içerir. Kod projesi değil, tasarım çıktıları ve üretim betikleridir.

## Durum
- Son onaylanan logo: **v20** (`logo/oydem-v20-*.svg|png`). Önceki sürümler (v1–v19) `logo/` içinde duruyor.
- Marka kiti: `marka-kiti/` (logo dosyaları, antetli kağıt, fatura, proforma invoice, kartvizit, zarf, kaşe, dijital dosyalar, rehber). Ayrıntı için `marka-kiti/README.md`.
- Logoyu yeniden üreten betik: `logo/uretim/logo_uret.py` (v20'yi birebir üretir). Kit belgeleri: `marka-kiti/araclar/build_docs.py` + `render.js`.

## Tasarım kararları (kullanıcının onayladıkları)
- Küre karelerden oluşur ve bir çerçeve (halka) içindedir; küre hem **O (Öykü)** hem dünya (ithalat/ihracat).
- İçindeki **D (Didem)** kalın değil kibar çizgili, hafif italik (~11°), üzerinde 3 "liman" geçidi var (halka düğümler + çıkan pikseller). Merkez düğümden limanlara ince bağlantı çizgileri gider; yapay zekayı temsil eder.
- Yazı: **OYDEM** (Michroma, büyük harf, ~11° eğik), alt yazı YAZILIM + "SANAYİ VE TİCARET LTD. ŞTİ.". Metin fontu Poppins. İkisi de OFL lisanslı.
- Renkler: lacivert #1E2A78, turkuaz #12B5A6, mürekkep #12183B, koyu zemin #0B1030 (koyu sürümde #4B5FE8 / #2EE6D0).
- Çerçeve küreye her yerde eşit uzaklıkta; yazı çerçeveyi böler (çerçevede yazı için açıklık var), çerçeve piksel dağılmasının bittiği yerden devam eder.
- Kareler çok hafif yumuşatılmış; karelerin üzerinden çizgi geçmez; D'nin çevresinde D'ye paralel dağılan kareler var.

## Bekleyenler
- Şirket bilgileri `marka-kiti/marka-bilgileri.json` içinde `[...]` yer tutucu. Kullanıcı verince doldur, `python3 marka-kiti/araclar/build_docs.py && node marka-kiti/araclar/render.js` ile belgeleri yeniden üret; kartvizit için ad/ünvan da gerekir.
- Önerilen sonraki işler: matbaa için baskı payı/kesim işaretli PDF, kağıt fatura/e-fatura entegratör şablonu, TÜRKPATENT marka başvurusu (sınıf 9, 35, 42), alan adı ve sosyal medya hesapları.
- Yasal içerik genel bilgidir; mali müşavir/avukat teyidi gerekir (bunu kullanıcıya hatırlat).

## Çalışma notları
- Gerçek bilgiyi uydurma; bilinmeyen alanlar yer tutucu kalır.
- Logo değişikliğinde tüm sürümleri (açık, koyu, tek renk, ikon) yeniden üret ve kiti güncelle.
- Üretim ortamı: Python 3 (`fonttools`, `pillow`, `python-docx`), Node + Playwright (PNG/PDF render).
