"""marka-kiti/01-logo ve 03-dijital içindeki şeffaf/zeminli logo SVG'lerini üretir (PNG için araclar/render.js ve marka-kiti betiklerine bakın)."""
import re
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from logo_uret import *
K=os.path.join(HERE,'..','..','marka-kiti')+os.sep
def strip_rect(p):
    t=open(p).read(); t=re.sub(r'<rect width="\d+" height="\d+" fill="[^"]*"/>','',t,count=1); open(p,'w').write(t)
for nm,(pal,bg) in PAL.items():
    logo(K+f'01-logo/oydem-logo-yatay-{nm}.svg',pal,bg,uid=nm[:2]+'h'); strip_rect(K+f'01-logo/oydem-logo-yatay-{nm}.svg')
    logo(K+f'01-logo/oydem-kure-{nm}.svg',pal,bg,icon=True,uid=nm[:2]+'k'); strip_rect(K+f'01-logo/oydem-kure-{nm}.svg')
print('ok')
