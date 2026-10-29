"""Oydem marka kiti: kırtasiye, dijital ve rehber dosyalarını üretir.

Kullanım (kit klasörünün içinden):
    python3 araclar/build_docs.py        # kaynak/*.html + manifest.json üretir
    node   araclar/render.js             # PDF ve PNG çıktılarını üretir
Bilgileri marka-bilgileri.json içinde değiştirip komutları yeniden çalıştırın.
"""
import json, os, base64, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
D = json.load(open(ROOT + 'marka-bilgileri.json', encoding='utf-8'))
E = lambda k: html.escape(D[k])
os.makedirs(ROOT + 'kaynak', exist_ok=True)
manifest = []

NAVY, TEAL, INK, GREY, DARK = '#1E2A78', '#12B5A6', '#12183B', '#5B6080', '#0B1030'

CSS = f"""
@font-face{{font-family:Poppins;font-weight:300;src:url(../fontlar/poppins-latin-300-normal.woff);unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122,U+2212}}
@font-face{{font-family:Poppins;font-weight:300;src:url(../fontlar/poppins-latin-ext-300-normal.woff);unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20CF}}
@font-face{{font-family:Poppins;font-weight:400;src:url(../fontlar/poppins-latin-400-normal.woff);unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122,U+2212}}
@font-face{{font-family:Poppins;font-weight:400;src:url(../fontlar/poppins-latin-ext-400-normal.woff);unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20CF}}
@font-face{{font-family:Poppins;font-weight:500;src:url(../fontlar/poppins-latin-500-normal.woff);unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122,U+2212}}
@font-face{{font-family:Poppins;font-weight:500;src:url(../fontlar/poppins-latin-ext-500-normal.woff);unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20CF}}
@font-face{{font-family:Poppins;font-weight:600;src:url(../fontlar/poppins-latin-600-normal.woff);unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122,U+2212}}
@font-face{{font-family:Poppins;font-weight:600;src:url(../fontlar/poppins-latin-ext-600-normal.woff);unicode-range:U+0100-02AF,U+1E00-1EFF,U+20A0-20CF}}
@font-face{{font-family:Michroma;src:url(../fontlar/michroma-latin-400-normal.woff);unicode-range:U+0000-00FF,U+0131,U+2000-206F}}
@font-face{{font-family:Michroma;src:url(../fontlar/michroma-latin-ext-400-normal.woff);unicode-range:U+0100-02AF,U+1E00-1EFF}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:Poppins,Arial,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;overflow:hidden;background:#fff;page-break-after:always}}
.page:last-child{{page-break-after:auto}}
.a4{{width:210mm;height:297mm}}
.lockup{{display:flex;align-items:center;gap:4.2mm}}
.lockup img{{display:block}}
.word .name{{font-family:Michroma,sans-serif;letter-spacing:.16em;color:{INK};transform:skewX(-11deg);transform-origin:left bottom;white-space:nowrap}}
.word .sub{{font-family:Michroma,sans-serif;letter-spacing:.44em;color:{NAVY};transform:skewX(-11deg);transform-origin:left bottom;white-space:nowrap}}
.word .tag{{font-weight:300;letter-spacing:.2em;color:{GREY};white-space:nowrap}}
.dark .word .name{{color:#fff}} .dark .word .sub{{color:#7F93FF}} .dark .word .tag{{color:#9AA6E8}}
.rule{{height:.55mm;background:linear-gradient(90deg,{TEAL},{NAVY})}}
.legal{{font-size:6.1pt;line-height:1.6;color:{GREY}}}
.legal b{{color:{INK};font-weight:600}}
.dim{{color:{GREY}}}
table{{border-collapse:collapse;width:100%}}
"""
open(ROOT + 'kaynak/ortak.css', 'w', encoding='utf-8').write(CSS)


def lockup(w_mm, dark=False, name_pt=15, tag=True):
    icon = '../01-logo/oydem-kure-koyu.svg' if dark else '../01-logo/oydem-kure-lacivert.svg'
    return (f'<div class="lockup {"dark" if dark else ""}"><img src="{icon}" style="width:{w_mm}mm">'
            f'<div class="word"><div class="name" style="font-size:{name_pt}pt">OYDEM</div>'
            f'<div class="sub" style="font-size:{name_pt*0.41:.1f}pt;margin-top:1.1mm">YAZILIM</div>'
            + (f'<div class="tag" style="font-size:{name_pt*0.36:.1f}pt;margin-top:1.1mm">SANAYİ VE TİCARET LTD. ŞTİ.</div>' if tag else '')
            + '</div></div>')


def pixel_strip(w=62, h=6, n=16):
    s = ''
    for i in range(n):
        t = i / (n - 1)
        size = min(h, w / n * 0.82) * (1 - 0.6 * t)
        r = round(0x1E + (0x12 - 0x1E) * t); g = round(0x2A + (0xB5 - 0x2A) * t); b = round(0x78 + (0xA6 - 0x78) * t)
        x = i * (w / n)
        s += f'<rect x="{x:.1f}" y="{(h-size)/2:.1f}" width="{size:.1f}" height="{size:.1f}" rx=".6" fill="rgb({r},{g},{b})"/>'
    return f'<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" style="display:block">{s}</svg>'


def legal_block(en=False):
    if en:
        return (f'<b>{E("unvan_tam")}</b><br>{E("adres")}<br>'
                f'Trade Registry: {E("sicil_mudurlugu")} / {E("sicil_no")} &nbsp;·&nbsp; MERSIS: {E("mersis")} &nbsp;·&nbsp; Tax Office / No: {E("vergi_dairesi")} / {E("vkn")}<br>'
                f'Tel: {E("telefon")} &nbsp;·&nbsp; {E("eposta")} &nbsp;·&nbsp; {E("web")} &nbsp;·&nbsp; KEP: {E("kep")}')
    return (f'<b>{E("unvan_tam")}</b><br>{E("adres")}<br>'
            f'Ticaret Sicil: {E("sicil_mudurlugu")} / {E("sicil_no")} &nbsp;·&nbsp; MERSİS No: {E("mersis")} &nbsp;·&nbsp; Sermaye: {E("sermaye")}<br>'
            f'Vergi Dairesi / No: {E("vergi_dairesi")} / {E("vkn")}<br>'
            f'Tel: {E("telefon")} &nbsp;·&nbsp; {E("eposta")} &nbsp;·&nbsp; {E("web")} &nbsp;·&nbsp; KEP: {E("kep")}')


def header_a4(en=False):
    return f"""
<div style="position:absolute;left:18mm;right:18mm;top:13mm;display:flex;justify-content:space-between;align-items:center">
  {lockup(19, name_pt=15)}
  <div class="legal" style="text-align:right;line-height:1.7">{E("telefon")}<br>{E("eposta")}<br>{E("web")}</div>
</div>
<div class="rule" style="position:absolute;left:18mm;right:18mm;top:37mm"></div>"""


def footer_a4(en=False):
    return f"""
<div style="position:absolute;left:18mm;right:18mm;bottom:9mm">
  <div class="rule" style="height:.3mm;margin-bottom:2.6mm"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:6mm">
    <div class="legal">{legal_block(en)}</div>
    <div>{pixel_strip(34, 5, 12)}</div>
  </div>
</div>"""


def watermark():
    return '<img src="../01-logo/oydem-kure-lacivert.svg" style="position:absolute;right:-48mm;bottom:12mm;width:150mm;opacity:.045">'


def write(name, body, w_css='', extra_css='', title='Oydem'):
    doc = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{title}</title><link rel="stylesheet" href="ortak.css"><style>{extra_css}</style></head><body>{body}</body></html>'
    open(ROOT + f'kaynak/{name}.html', 'w', encoding='utf-8').write(doc)


def add(name, out, kind, w, h, unit='mm', pdf=True):
    manifest.append(dict(html=f'kaynak/{name}.html', out=out, w=w, h=h, unit=unit, pdf=pdf))


# ---------------------------------------------------------------- 1. Antetli kağıt
sample = f"""
<div style="position:absolute;left:18mm;right:18mm;top:50mm;font-size:9.3pt;line-height:1.7;font-weight:300">
 <div style="display:flex;justify-content:space-between;margin-bottom:9mm"><div>Sayı : [Yazı No]<br>Konu : [Konu]</div><div>Tarih : [GG.AA.YYYY]</div></div>
 <div style="margin-bottom:7mm;font-weight:500">[SAYIN ALICI ÜNVANI]<br><span style="font-weight:300">[Adres]</span></div>
 <p>Sayın İlgili,</p>
 <p>Bu alan örnek yazı metnidir. Antetli kağıdın baş ve alt bilgi alanları sabittir; yazınızı bu iki alanın arasına yerleştirin.
 Üst bilgi şirket kimliğini, alt bilgi ise ticari yazışmalarda bulunması gereken ticari unvan, ticaret sicil, MERSİS, vergi ve iletişim bilgilerini taşır.</p>
 <p>Gereğini bilgilerinize arz ederiz.</p>
 <p style="margin-top:12mm">Saygılarımızla,<br><b style="font-weight:600">{E("unvan_kisa")}</b><br><span class="dim">[Yetkili Ad Soyad — Görev]</span></p>
</div>"""
for nm, content in (('antetli-kagit-bos', ''), ('antetli-kagit-ornek', sample)):
    write(nm, f'<div class="page a4">{watermark()}{header_a4()}{content}{footer_a4()}</div>', title='Antetli Kağıt')
    add(nm, f'02-kirtasiye/{nm}', 'a4', 210, 297)

# ---------------------------------------------------------------- 2. Fatura başlığı (TR)
rows = ''.join('<tr>' + '<td style="height:8.2mm"></td>' * 7 + '</tr>' for _ in range(12))
inv = f"""
<div class="page a4">{header_a4()}
<div style="position:absolute;left:18mm;right:18mm;top:44mm">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div><div style="font-family:Michroma;font-size:19pt;letter-spacing:.14em;transform:skewX(-11deg);transform-origin:left bottom;color:{INK}">FATURA</div>
      <div class="dim" style="font-size:6.4pt;letter-spacing:.22em;margin-top:1.5mm">E-FATURA / E-ARŞİV / MATBU</div></div>
    <table style="width:78mm;font-size:7.6pt">
      <tr><td class="dim" style="padding:.9mm 0">Fatura No</td><td style="border-bottom:.2mm solid #cfd3e6;width:46mm"></td></tr>
      <tr><td class="dim" style="padding:.9mm 0">Düzenleme Tarihi</td><td style="border-bottom:.2mm solid #cfd3e6"></td></tr>
      <tr><td class="dim" style="padding:.9mm 0">Vade Tarihi</td><td style="border-bottom:.2mm solid #cfd3e6"></td></tr>
      <tr><td class="dim" style="padding:.9mm 0">Ödeme Şekli</td><td style="border-bottom:.2mm solid #cfd3e6"></td></tr>
    </table>
  </div>
  <div style="display:flex;gap:6mm;margin-top:6mm;font-size:7.6pt">
    <div style="flex:1.25;border:.25mm solid #cfd3e6;border-radius:1.6mm;padding:3mm 4mm;min-height:27mm">
      <div class="dim" style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">SAYIN / ALICI</div>
      <div style="font-weight:500">[Alıcı Unvanı / Ad Soyad]</div><div class="dim" style="margin-top:1mm;line-height:1.6">[Adres]<br>Vergi Dairesi: [ ] &nbsp;·&nbsp; VKN / TCKN: [ ]</div></div>
    <div style="flex:1;border:.25mm solid #cfd3e6;border-radius:1.6mm;padding:3mm 4mm">
      <div class="dim" style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">SATICI</div>
      <div style="font-weight:500">{E("unvan_kisa")}</div><div class="dim" style="margin-top:1mm;line-height:1.6">Vergi Dairesi: {E("vergi_dairesi")}<br>VKN: {E("vkn")}<br>MERSİS: {E("mersis")}</div></div>
  </div>
  <table style="margin-top:6mm;font-size:7.4pt">
    <thead><tr style="background:linear-gradient(90deg,{NAVY},#2a3a9a);color:#fff;text-align:left">
      <th style="padding:2.2mm 2mm;width:9mm">Sıra</th><th style="padding:2.2mm 2mm">Mal / Hizmet Cinsi</th><th style="padding:2.2mm 2mm;width:16mm">Miktar</th>
      <th style="padding:2.2mm 2mm;width:14mm">Birim</th><th style="padding:2.2mm 2mm;width:24mm">Birim Fiyat</th><th style="padding:2.2mm 2mm;width:14mm">KDV %</th><th style="padding:2.2mm 2mm;width:26mm;text-align:right">Tutar</th></tr></thead>
    <tbody style="border-bottom:.25mm solid #cfd3e6">{rows.replace('<td style="height:8.2mm"></td>','<td style="height:8.2mm;border-bottom:.2mm solid #e5e8f3;padding:0 2mm"></td>')}</tbody>
  </table>
  <div style="display:flex;justify-content:space-between;margin-top:5mm;font-size:7.4pt">
    <div style="width:92mm" class="dim"><div style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">BANKA BİLGİLERİ</div>
      {E("banka")}<br>IBAN: {E("iban")}<br><div style="margin-top:3mm;font-size:6.4pt">Yalnız: ........................................................ TL'dir.</div></div>
    <table style="width:68mm">
      <tr><td class="dim" style="padding:1.3mm 0">Ara Toplam</td><td style="text-align:right;border-bottom:.2mm solid #e5e8f3;width:32mm"></td></tr>
      <tr><td class="dim" style="padding:1.3mm 0">Toplam İskonto</td><td style="text-align:right;border-bottom:.2mm solid #e5e8f3"></td></tr>
      <tr><td class="dim" style="padding:1.3mm 0">Hesaplanan KDV</td><td style="text-align:right;border-bottom:.2mm solid #e5e8f3"></td></tr>
      <tr style="font-weight:600"><td style="padding:2mm 0;color:{NAVY}">GENEL TOPLAM</td><td style="text-align:right;border-bottom:.5mm solid {TEAL}"></td></tr>
    </table>
  </div>
</div>
{footer_a4()}</div>"""
write('fatura-sablonu', inv, title='Fatura Şablonu')
add('fatura-sablonu', '02-kirtasiye/fatura-sablonu', 'a4', 210, 297)

# ---------------------------------------------------------------- 3. Proforma invoice (EN)
prow = ''.join('<tr>' + '<td style="height:8mm;border-bottom:.2mm solid #e5e8f3"></td>' * 7 + '</tr>' for _ in range(9))
info = lambda a, b: f'<tr><td class="dim" style="padding:1mm 0;width:34mm">{a}</td><td style="border-bottom:.2mm solid #cfd3e6">{b}</td></tr>'
pro = f"""
<div class="page a4">{header_a4(True)}
<div style="position:absolute;left:18mm;right:18mm;top:44mm">
  <div style="font-family:Michroma;font-size:17pt;letter-spacing:.12em;transform:skewX(-11deg);transform-origin:left bottom">PROFORMA INVOICE</div>
  <div class="dim" style="font-size:6.4pt;letter-spacing:.22em;margin-top:1.5mm">COMMERCIAL / EXPORT DOCUMENT</div>
  <div style="display:flex;gap:8mm;margin-top:6mm;font-size:7.4pt">
    <table style="flex:1">{info('Proforma No','')}{info('Date','')}{info('Validity','')}{info('Currency','')}</table>
    <table style="flex:1">{info('Incoterms® 2020','')}{info('Payment Terms','')}{info('Delivery Time','')}{info('Country of Origin','Türkiye')}</table>
  </div>
  <div style="display:flex;gap:6mm;margin-top:5mm;font-size:7.4pt">
    <div style="flex:1;border:.25mm solid #cfd3e6;border-radius:1.6mm;padding:3mm 4mm;min-height:27mm"><div class="dim" style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">SELLER / EXPORTER</div>
      <div style="font-weight:500">{E("unvan_tam")}</div><div class="dim" style="line-height:1.6;margin-top:1mm">{E("adres")}<br>Tax No: {E("vkn")} &nbsp;·&nbsp; MERSIS: {E("mersis")}</div></div>
    <div style="flex:1;border:.25mm solid #cfd3e6;border-radius:1.6mm;padding:3mm 4mm"><div class="dim" style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">BUYER / CONSIGNEE</div>
      <div style="font-weight:500">[Company Name]</div><div class="dim" style="line-height:1.6;margin-top:1mm">[Address, City, Country]<br>VAT / Tax ID: [ ]<br>Contact: [ ]</div></div>
  </div>
  <div style="display:flex;gap:8mm;margin-top:4mm;font-size:7.4pt"><table style="flex:1">{info('Port of Loading','')}</table><table style="flex:1">{info('Port of Discharge','')}</table></div>
  <table style="margin-top:5mm;font-size:7.2pt">
    <thead><tr style="background:linear-gradient(90deg,{NAVY},#2a3a9a);color:#fff;text-align:left">
      <th style="padding:2.2mm 2mm;width:8mm">No</th><th style="padding:2.2mm 2mm">Description of Goods</th><th style="padding:2.2mm 2mm;width:20mm">HS Code</th><th style="padding:2.2mm 2mm;width:14mm">Qty</th>
      <th style="padding:2.2mm 2mm;width:12mm">Unit</th><th style="padding:2.2mm 2mm;width:22mm">Unit Price</th><th style="padding:2.2mm 2mm;width:24mm;text-align:right">Amount</th></tr></thead>
    <tbody>{prow}</tbody></table>
  <div style="display:flex;justify-content:space-between;margin-top:5mm;font-size:7.2pt">
    <div style="width:96mm" class="dim"><div style="font-size:6pt;letter-spacing:.18em;margin-bottom:1.5mm">BANK DETAILS</div>
      Beneficiary: {E("unvan_tam")}<br>Bank: {E("banka")} &nbsp;·&nbsp; SWIFT: {E("swift")}<br>IBAN: {E("iban")}
      <div style="margin-top:3mm;font-size:6.2pt;line-height:1.5">This proforma invoice is issued for customs and payment-arrangement purposes and is not a tax invoice.</div></div>
    <table style="width:66mm"><tr><td class="dim" style="padding:1.3mm 0">Subtotal</td><td style="border-bottom:.2mm solid #e5e8f3;width:30mm"></td></tr>
      <tr><td class="dim" style="padding:1.3mm 0">Freight / Insurance</td><td style="border-bottom:.2mm solid #e5e8f3"></td></tr>
      <tr style="font-weight:600"><td style="padding:2mm 0;color:{NAVY}">TOTAL</td><td style="border-bottom:.5mm solid {TEAL}"></td></tr></table>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:9mm;font-size:6.4pt" class="dim"><div style="width:62mm;border-top:.25mm solid #9aa0c0;padding-top:1.5mm">Authorized signature &amp; stamp</div><div style="width:62mm;border-top:.25mm solid #9aa0c0;padding-top:1.5mm">Buyer's acceptance</div></div>
</div>
{footer_a4(True)}</div>"""
write('proforma-invoice', pro, title='Proforma Invoice')
add('proforma-invoice', '02-kirtasiye/proforma-invoice', 'a4', 210, 297)

# ---------------------------------------------------------------- 4. Kartvizit (90x50, ön + arka)
card = f"""
<div class="page" style="width:90mm;height:50mm;background:#fff">
  <img src="../01-logo/oydem-kure-lacivert.svg" style="position:absolute;right:-17mm;bottom:-17mm;width:56mm;opacity:.06">
  <div style="position:absolute;left:6mm;top:6mm">{lockup(8.6, name_pt=8.2, tag=False)}</div>
  <div style="position:absolute;left:6mm;top:22mm"><div style="font-weight:600;font-size:9pt">{E("kisi_ad")}</div><div class="dim" style="font-size:6.2pt;font-weight:300;letter-spacing:.06em;margin-top:.6mm">{E("kisi_unvan")}</div></div>
  <div style="position:absolute;left:6mm;bottom:5.2mm;font-size:6pt;line-height:1.6;font-weight:300">{E("kisi_tel")}<br>{E("kisi_eposta")}<br>{E("web")}</div>
  <div style="position:absolute;right:6mm;bottom:5.2mm;text-align:right;font-size:5pt;line-height:1.55;color:{GREY};font-weight:300;width:36mm">{E("adres")}</div>
  <div class="rule" style="position:absolute;left:0;right:0;top:0;height:1.1mm"></div>
</div>
<div class="page dark" style="width:90mm;height:50mm;background:radial-gradient(circle at 30% 40%,#16206b,{DARK} 70%)">
  <div style="position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center">{lockup(17, dark=True, name_pt=14, tag=True)}</div>
  <div style="position:absolute;left:0;right:0;bottom:3.5mm;text-align:center;font-size:5pt;letter-spacing:.3em;color:#7F93FF;font-weight:300">İTHALAT · İHRACAT · YAPAY ZEKA</div>
</div>"""
write('kartvizit', card, title='Kartvizit')
add('kartvizit', '02-kirtasiye/kartvizit', 'card', 90, 50)

# ---------------------------------------------------------------- 5. Zarf (DL 220x110)
env = f"""
<div class="page" style="width:220mm;height:110mm">
  <img src="../01-logo/oydem-kure-lacivert.svg" style="position:absolute;right:-30mm;bottom:-40mm;width:110mm;opacity:.045">
  <div style="position:absolute;left:12mm;top:10mm">{lockup(13, name_pt=11, tag=True)}</div>
  <div class="legal" style="position:absolute;left:12mm;bottom:9mm;width:110mm"><b>{E("unvan_tam")}</b><br>{E("adres")}<br>{E("telefon")} · {E("eposta")} · {E("web")}</div>
  <div class="rule" style="position:absolute;left:0;right:0;bottom:0;height:2mm"></div>
  <div style="position:absolute;right:16mm;top:46mm;width:80mm;font-size:7pt;color:#b3b8d1;border-top:.2mm dashed #cfd3e6;padding-top:3mm">[Alıcı adres alanı]</div>
</div>"""
write('zarf-dl', env, title='Zarf DL')
add('zarf-dl', '02-kirtasiye/zarf-dl', 'env', 220, 110)

# ---------------------------------------------------------------- 6. Kaşe (şirket kaşesi tasarımı, tek renk)
STAMP = '#1B3A8C'
stamp = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 340" width="70mm" height="34mm">
<rect x="6" y="6" width="688" height="328" rx="20" fill="none" stroke="{STAMP}" stroke-width="9"/>
<rect x="24" y="24" width="652" height="292" rx="12" fill="none" stroke="{STAMP}" stroke-width="3"/>
<g fill="{STAMP}" font-family="Poppins,Arial,sans-serif" text-anchor="middle">
<text x="350" y="95" font-size="50" font-weight="700" letter-spacing="2">OYDEM YAZILIM</text>
<text x="350" y="140" font-size="30" font-weight="600">SANAYİ VE TİCARET LTD. ŞTİ.</text>
<line x1="70" x2="630" y1="160" y2="160" stroke="{STAMP}" stroke-width="2.5"/>
<text x="350" y="198" font-size="22" font-weight="500">{E("adres")}</text>
<text x="350" y="236" font-size="22" font-weight="500">V.D.: {E("vergi_dairesi")}  ·  V.N.: {E("vkn")}</text>
<text x="350" y="274" font-size="22" font-weight="500">MERSİS: {E("mersis")}</text>
<text x="350" y="305" font-size="19" font-weight="500">Tel: {E("telefon")}</text>
</g></svg>"""
open(ROOT + '02-kirtasiye/kase.svg', 'w', encoding='utf-8').write(stamp)
write('kase', f'<div class="page" style="width:70mm;height:34mm;background:#fff">{stamp}</div>', title='Kaşe')
add('kase', '02-kirtasiye/kase', 'stamp', 70, 34, pdf=False)

# ---------------------------------------------------------------- 7. Dijital
def px(name, out, w, h, body, css=''):
    write(name, body, extra_css=css, title=name)
    add(name, out, 'px', w, h, unit='px', pdf=False)

# LinkedIn banner 1584x396
px('linkedin-banner', '03-dijital/linkedin-banner', 1584, 396, f"""
<div class="page dark" style="width:1584px;height:396px;background:radial-gradient(circle at 12% 40%,#1b2a8a,{DARK} 62%)">
 <img src="../01-logo/oydem-kure-koyu.svg" style="position:absolute;right:-130px;top:-120px;width:640px;opacity:.28">
 <div style="position:absolute;left:96px;top:0;bottom:30px;display:flex;align-items:center">{lockup(128, dark=True, name_pt=34, tag=True).replace('mm','px')}</div>
 <div style="position:absolute;left:96px;bottom:34px;color:#2EE6D0;font-size:16px;letter-spacing:.34em;font-weight:300">İTHALAT · İHRACAT · YAPAY ZEKA</div>
</div>""")
# Instagram / sosyal kare 1080
px('sosyal-kare', '03-dijital/sosyal-medya-kare', 1080, 1080, f"""
<div class="page dark" style="width:1080px;height:1080px;background:radial-gradient(circle at 50% 38%,#1b2a8a,{DARK} 68%)">
 <img src="../01-logo/oydem-kure-koyu.svg" style="position:absolute;left:190px;top:80px;width:700px">
 <div style="position:absolute;left:0;right:0;top:810px;text-align:center"><div class="word dark" style="display:inline-block;text-align:left">
  <div class="name" style="font-size:64px">OYDEM</div><div class="sub" style="font-size:26px;margin-top:10px">YAZILIM</div></div>
  <div style="color:#2EE6D0;font-size:21px;letter-spacing:.34em;margin-top:34px;font-weight:300">İTHALAT · İHRACAT · YAPAY ZEKA</div></div>
</div>""")
# Sunum kapak + içerik 1920x1080
px('sunum-kapak', '03-dijital/sunum-kapak', 1920, 1080, f"""
<div class="page dark" style="width:1920px;height:1080px;background:radial-gradient(circle at 78% 50%,#1b2a8a,{DARK} 62%)">
 <img src="../01-logo/oydem-kure-koyu.svg" style="position:absolute;right:-60px;top:70px;width:940px">
 <div style="position:absolute;left:130px;top:96px">{lockup(120, dark=True, name_pt=30, tag=False).replace('mm','px')}</div>
 <div style="position:absolute;left:130px;top:430px;width:900px"><div style="font-size:78px;font-weight:600;line-height:1.1;color:#fff">[Sunum Başlığı]</div>
  <div style="font-size:30px;font-weight:300;color:#9AA6E8;margin-top:28px">[Alt başlık · Tarih · Sunan]</div></div>
 <div style="position:absolute;left:130px;bottom:90px;color:#2EE6D0;font-size:20px;letter-spacing:.34em;font-weight:300">İTHALAT · İHRACAT · YAPAY ZEKA</div>
</div>""")
px('sunum-icerik', '03-dijital/sunum-icerik', 1920, 1080, f"""
<div class="page" style="width:1920px;height:1080px;background:#fff">
 <div class="rule" style="position:absolute;left:0;right:0;top:0;height:14px"></div>
 <div style="position:absolute;left:110px;top:70px;font-size:20px;letter-spacing:.3em;color:{TEAL};font-weight:500">BÖLÜM</div>
 <div style="position:absolute;left:110px;top:110px;font-size:62px;font-weight:600;color:{INK}">[Slayt başlığı]</div>
 <div style="position:absolute;left:110px;top:260px;right:110px;font-size:32px;line-height:1.7;font-weight:300;color:{GREY}">• [İçerik maddesi]<br>• [İçerik maddesi]<br>• [İçerik maddesi]</div>
 <img src="../01-logo/oydem-kure-lacivert.svg" style="position:absolute;right:-120px;bottom:-140px;width:620px;opacity:.06">
 <div style="position:absolute;left:110px;right:110px;bottom:50px;display:flex;justify-content:space-between;align-items:center;font-size:18px;color:{GREY}">
  <div style="display:flex;align-items:center;gap:16px"><img src="../01-logo/oydem-kure-lacivert.svg" style="width:46px"><span style="font-family:Michroma;letter-spacing:.2em;color:{INK};font-size:17px">OYDEM</span></div><div>{E("unvan_kisa")}</div></div>
</div>""")

# E-posta imzası (HTML, logo gömülü)
logo_b64 = ''
try:
    from PIL import Image
    im = Image.open(ROOT + '01-logo/oydem-kure-lacivert.png').convert('RGBA').resize((200, 200), Image.LANCZOS)
    im.save(ROOT + '03-dijital/imza-logo.png'); logo_b64 = base64.b64encode(open(ROOT + '03-dijital/imza-logo.png', 'rb').read()).decode()
except Exception as ex:
    print('imza logo uretilemedi', ex)
sig = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>E-posta imzası</title></head><body style="margin:24px;background:#fff">
<table cellpadding="0" cellspacing="0" style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:{INK};line-height:1.5">
<tr><td style="padding-right:16px;border-right:3px solid {TEAL};vertical-align:middle"><img src="data:image/png;base64,{logo_b64}" width="86" height="86" alt="Oydem Yazılım"></td>
<td style="padding-left:16px;vertical-align:middle">
 <div style="font-size:15px;font-weight:bold;color:{INK}">{E("kisi_ad")}</div><div style="color:{GREY};margin-bottom:6px">{E("kisi_unvan")} · <b style="color:{NAVY}">OYDEM YAZILIM</b></div>
 <div>T: {E("kisi_tel")}<br>E: <a href="#" style="color:{NAVY};text-decoration:none">{E("kisi_eposta")}</a><br>W: <a href="#" style="color:{NAVY};text-decoration:none">{E("web")}</a></div>
 <div style="color:{GREY};font-size:10px;margin-top:6px">{E("adres")}</div></td></tr>
<tr><td colspan="2" style="padding-top:12px;font-size:9px;color:#8a8fae;line-height:1.5;max-width:560px">{E("unvan_tam")} · MERSİS: {E("mersis")} · Ticaret Sicil: {E("sicil_mudurlugu")} / {E("sicil_no")} · KEP: {E("kep")}<br>
Bu e-posta ve ekleri yalnızca alıcısına yöneliktir ve gizli bilgi içerebilir. Yanlışlıkla size ulaştıysa lütfen göndericiyi bilgilendirip siliniz; içeriğin kullanımı, kopyalanması veya paylaşılması yasaktır.</td></tr>
</table></body></html>"""
open(ROOT + '03-dijital/eposta-imzasi.html', 'w', encoding='utf-8').write(sig)

# ---------------------------------------------------------------- 8. Marka rehberi (A4, 2 sayfa)
def cmyk(hexv):
    r, g, b = [int(hexv[i:i+2], 16) / 255 for i in (1, 3, 5)]
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(v * 100) for v in ((1-r-k)/(1-k), (1-g-k)/(1-k), (1-b-k)/(1-k), k))

def swatch(name, hexv, note=''):
    r, g, b = [int(hexv[i:i+2], 16) for i in (1, 3, 5)]
    c, m, y, k = cmyk(hexv)
    return (f'<div style="flex:1;min-width:0"><div style="height:19mm;border-radius:2mm;background:{hexv};border:.2mm solid #e1e4f0"></div>'
            f'<div style="font-weight:600;font-size:7.4pt;margin-top:1.6mm">{name}</div><div class="dim" style="font-size:6.4pt;line-height:1.55">{hexv}<br>RGB {r} {g} {b}<br>CMYK ≈ {c} {m} {y} {k}<br>{note}</div></div>')

guide = f"""
<div class="page a4"><div style="position:absolute;left:18mm;right:18mm;top:14mm">
  {lockup(16, name_pt=13)}<div class="rule" style="margin-top:6mm"></div>
  <div style="font-family:Michroma;font-size:15pt;letter-spacing:.12em;margin-top:8mm;transform:skewX(-11deg);transform-origin:left bottom">MARKA REHBERİ</div>
  <div class="dim" style="font-size:7.4pt;margin-top:2mm;font-weight:300">Küre, D ve yazı; ithalat-ihracatı (küre), yapay zekayı (düğüm ağı) ve kurucuların isimlerini (O ve D) tek işaret altında toplar.</div>
  <div style="display:flex;gap:5mm;margin-top:7mm">
    <div style="flex:1.6;border:.2mm solid #e1e4f0;border-radius:2mm;padding:6mm;display:flex;align-items:center;justify-content:center;height:46mm"><img src="../01-logo/oydem-logo-yatay-lacivert.svg" style="width:100%"></div>
    <div style="flex:1;border-radius:2mm;padding:6mm;display:flex;align-items:center;justify-content:center;height:46mm;background:{DARK}"><img src="../01-logo/oydem-kure-koyu.svg" style="height:100%"></div>
  </div>
  <div style="display:flex;gap:5mm;margin-top:5mm">
    <div style="flex:1.6;border-radius:2mm;padding:5mm;display:flex;align-items:center;justify-content:center;height:34mm;background:{DARK}"><img src="../01-logo/oydem-logo-yatay-koyu.svg" style="height:100%"></div>
    <div style="flex:1;border:.2mm solid #e1e4f0;border-radius:2mm;padding:5mm;display:flex;align-items:center;justify-content:center;height:34mm"><img src="../01-logo/oydem-logo-yatay-tek-renk.svg" style="height:100%"></div>
  </div>
  <div style="font-size:6.6pt;color:{GREY};margin-top:2mm;font-weight:300">Açık zeminde lacivert-turkuaz, koyu zeminde koyu sürüm; tek renk sürüm kaşe, fotokopi, faks ve tek renk baskı içindir.</div>
  <div style="font-weight:600;font-size:9pt;margin-top:7mm">Renkler</div>
  <div style="display:flex;gap:4mm;margin-top:3mm">{swatch('Lacivert', NAVY, 'Ana renk')}{swatch('Turkuaz', TEAL, 'Vurgu')}{swatch('Mürekkep', INK, 'Metin')}{swatch('Koyu zemin', DARK, 'Koyu sürüm')}{swatch('Parlak mavi', '#4B5FE8', 'Koyu zeminde')}{swatch('Neon turkuaz', '#2EE6D0', 'Koyu zeminde')}</div>
  <div style="font-weight:600;font-size:9pt;margin-top:7mm">Yazı karakterleri</div>
  <div style="display:flex;gap:6mm;margin-top:3mm">
    <div style="flex:1"><div style="font-family:Michroma;font-size:15pt;letter-spacing:.12em;transform:skewX(-11deg);transform-origin:left bottom">OYDEM</div><div class="dim" style="font-size:6.6pt;margin-top:1.5mm">Michroma — logo ve başlıklar (büyük harf, %11 eğik, geniş harf aralığı)</div></div>
    <div style="flex:1"><div style="font-size:15pt;font-weight:600">Poppins Aa</div><div class="dim" style="font-size:6.6pt;margin-top:1.5mm">Poppins 300 / 400 / 500 / 600 — metinler ve belgeler</div></div></div>
  <div class="dim" style="font-size:6.2pt;margin-top:2.5mm;font-weight:300">Her iki font da SIL Open Font License (OFL) ile ücretsiz ve ticari kullanıma açıktır; lisans metinleri <i>fontlar</i> klasöründedir.</div>
</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:9mm" class="legal"><div class="rule" style="height:.3mm;margin-bottom:2mm"></div>Oydem Yazılım — Marka Rehberi · Sayfa 1/2</div></div>

<div class="page a4"><div style="position:absolute;left:18mm;right:18mm;top:14mm">
  <div style="display:flex;justify-content:space-between;align-items:center"><div style="font-family:Michroma;font-size:11pt;letter-spacing:.12em;transform:skewX(-11deg);transform-origin:left bottom">KULLANIM KURALLARI</div>{pixel_strip(34,5,12)}</div><div class="rule" style="margin-top:4mm"></div>
  <div style="display:flex;gap:7mm;margin-top:6mm;font-size:7.4pt;line-height:1.65;font-weight:300">
   <div style="flex:1"><div style="font-weight:600;color:{TEAL};font-size:8pt;margin-bottom:1.5mm">YAPIN</div>
    • Logonun etrafında, küredeki "D" harfinin yüksekliğinin yarısı kadar boşluk bırakın.<br>
    • Yatay logoyu en az 35 mm / 140 px, kürenin kendisini en az 12 mm / 48 px kullanın. Daha küçük boyutlarda favicon sürümünü kullanın.<br>
    • Açık zeminde lacivert, koyu zeminde koyu sürümü seçin.<br>
    • Dosyaları SVG olarak büyütün; PNG'yi büyütmeyin.</div>
   <div style="flex:1"><div style="font-weight:600;color:#c0392b;font-size:8pt;margin-bottom:1.5mm">YAPMAYIN</div>
    • Logoyu eğmeyin, uzatmayın, renklerini değiştirmeyin.<br>
    • Kürenin ve yazının yerlerini birbirinden ayırmayın (ikon kullanımı hariç).<br>
    • Karmaşık fotoğraf veya desen üzerine koymayın.<br>
    • Gölge, parlama veya dış çizgi eklemeyin.</div></div>

  <div style="font-weight:600;font-size:9pt;margin-top:7mm">Dosya klasörü</div>
  <table style="font-size:7pt;margin-top:2mm;line-height:1.5">
   {''.join(f'<tr><td style="padding:1.2mm 0;border-bottom:.2mm solid #e5e8f3;width:46mm;font-weight:500">{a}</td><td class="dim" style="border-bottom:.2mm solid #e5e8f3;font-weight:300">{b}</td></tr>' for a, b in (
    ('01-logo','Küre ve yatay logo, 3 renk sürümü, SVG + şeffaf PNG'),
    ('02-kirtasiye','Antetli kağıt, fatura, proforma invoice, kartvizit, zarf, kaşe (PDF/PNG)'),
    ('03-dijital','Favicon, e-posta imzası, LinkedIn banner, sosyal medya, sunum'),
    ('kaynak + araclar','HTML kaynakları ve üretim betikleri'),
    ('marka-bilgileri.json','Şirket bilgileri: doldurup belgeleri yeniden üretin')))}
  </table>

  <div style="font-weight:600;font-size:9pt;margin-top:7mm">Yasal kontrol listesi <span class="dim" style="font-weight:300;font-size:6.6pt">(genel bilgidir; mali müşavir / avukatınızla teyit edin)</span></div>
  <div style="font-size:7pt;line-height:1.65;font-weight:300;margin-top:2mm">
   <b style="font-weight:600">Ticari yazışmalar ve antetli kağıt:</b> tescilli ticaret unvanı (unvanda "Limited Şirketi" ifadesi; kısaltma kullanıyorsanız tescildeki yazılışa uyun), ticaret sicil müdürlüğü ve sicil numarası, MERSİS numarası, merkez adresi, vergi dairesi ve numarası, limited şirkette sermaye bilgisi, iletişim bilgileri ve KEP adresi.<br>
   <b style="font-weight:600">Fatura:</b> Vergi Usul Kanunu md. 230 kapsamındaki zorunlu alanlar (satıcı ve alıcının unvanı, adresi, vergi dairesi ve numarası, fatura no, tarih, mal/hizmet cinsi, miktar, birim fiyat, KDV, toplam). E-fatura / e-arşiv mükellefiyseniz fatura GİB portalı veya özel entegratör üzerinden düzenlenir; bu şablondaki başlık, logo ve alt bilgi entegratörün tasarım şablonuna aktarılabilir. Kâğıt (matbu) fatura kullanacaksanız basım, yetkili matbaada ve güncel mevzuat şartlarıyla yaptırılmalıdır.<br>
   <b style="font-weight:600">Web sitesi ve e-posta:</b> sermaye şirketleri için internet sitesi ve KEP adresi yükümlülükleri vardır; sitede KVKK aydınlatma metni, gizlilik ve çerez politikası bulundurun.<br>
   <b style="font-weight:600">Marka tescili:</b> logo ve "OYDEM" adı için TÜRKPATENT'te benzerlik araştırması yaptırıp başvurun. Önerilen Nice sınıfları: 9 (yazılım), 42 (yazılım geliştirme, yapay zeka hizmetleri), 35 (ithalat-ihracat ve ticaret hizmetleri). Marka hakkı tescille doğar; tescil olmadan logo ve ad üçüncü kişilerce başvurulabilir.<br>
   <b style="font-weight:600">Alan adı ve sosyal medya:</b> şirket adıyla alan adı ve kullanıcı adlarını önceden rezerve edin.<br>
   <b style="font-weight:600">Fontlar ve görseller:</b> bu kitteki yazı karakterleri OFL lisanslıdır; logo bu çalışma için özgün olarak üretilmiştir, stok görsel veya üçüncü taraf telifli öğe içermez.</div>
</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:9mm" class="legal"><div class="rule" style="height:.3mm;margin-bottom:2mm"></div>{E("unvan_tam")} · Marka Rehberi · Sayfa 2/2</div></div>"""
write('marka-rehberi', guide, title='Marka Rehberi')
add('marka-rehberi', '04-rehber/marka-rehberi', 'a4', 210, 297)

json.dump(manifest, open(ROOT + 'araclar/manifest.json', 'w'), ensure_ascii=False, indent=1)
print('html hazır:', len(manifest))
