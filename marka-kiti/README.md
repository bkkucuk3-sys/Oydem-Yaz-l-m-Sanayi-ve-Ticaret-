# Oydem Yazılım – Marka Kiti

Bu klasör, Oydem Yazılım Sanayi ve Ticaret Limited Şirketi'nin logo ve kurumsal evrak şablonlarını içerir.

| Klasör | İçerik |
|---|---|
| `01-logo` | Küre (ikon) ve yatay logo: açık / koyu / tek renk, SVG + şeffaf PNG, ayrıca zeminli PNG |
| `02-kirtasiye` | Antetli kağıt (PDF + Word), fatura şablonu, proforma invoice (EN), kartvizit, zarf, kaşe |
| `03-dijital` | Favicon (SVG/PNG/ICO), e-posta imzası, LinkedIn banner, sosyal medya karesi, sunum kapağı ve içerik slaytı |
| `04-rehber` | Marka rehberi (renkler, fontlar, kullanım kuralları, yasal kontrol listesi) |
| `fontlar` | Michroma ve Poppins (SIL OFL lisansı, ticari kullanıma açık) |
| `marka-bilgileri.json` | Şirket bilgileri. Köşeli parantezli alanları doldurun |
| `kaynak`, `araclar` | HTML kaynakları ve üretim betikleri |

## Bilgileri doldurup belgeleri yeniden üretme
1. `marka-bilgileri.json` içindeki `[...]` alanlarını gerçek bilgilerle değiştirin.
2. Kit klasöründe sırayla çalıştırın:
   `python3 araclar/build_docs.py` ve `node araclar/render.js` (Playwright gerekir).
3. `02-kirtasiye/antetli-kagit.docx` Word'de doğrudan düzenlenir; bilgileri elle güncelleyin.

> Yasal içerik (zorunlu alanlar, marka tescili vb.) genel bilgidir; mali müşavir ve marka vekilinizle teyit edin.
