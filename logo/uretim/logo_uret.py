"""Oydem logosu (v20) üretici.

Kullanım:  python3 logo/uretim/logo_uret.py [çıktı_klasörü]
Gerekenler: python3, fonttools (pip install fonttools). Fontlar marka-kiti/fontlar içinden okunur.
Tasarım parametreleri: mark() (küre, D, limanlar), globe() (kareler), logo() (yerleşim).
"""
import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os, sys
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','marka-kiti','fontlar')+os.sep
def lerp(a,b,t): return a+(b-a)*t
def hexrgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def mix(c1,c2,t):
    a,b=hexrgb(c1),hexrgb(c2); return '#%02x%02x%02x'%tuple(round(lerp(a[i],b[i],t)) for i in range(3))
_c={}
def wm(file,text,x,y,size,track,fill):
    if file not in _c: _c[file]=TTFont(FD+file)
    f=_c[file]; cm=f.getBestCmap(); gs=f.getGlyphSet(); sc=size/f['head'].unitsPerEm
    d='';cx=x
    for ch in text:
        gn=cm.get(ord(ch)) or cm[ord('I')]
        pen=SVGPathPen(gs); gs[gn].draw(TransformPen(pen,(sc,0,0,-sc,cx,y))); d+=pen.getCommands(); cx+=gs[gn].width*sc+track
    return '<path fill="%s" d="%s"/>'%(fill,d)
MICH='michroma-latin-400-normal.woff'
POP='poppins-latin-300-normal.woff'
POPX='poppins-latin-ext-300-normal.woff'
def sub_text(text,x,y,size,track,fill):
    d='';cx=x
    fl=TTFont(FD+POP); fx=TTFont(FD+POPX)
    for ch in text:
        f=fl if ord(ch) in fl.getBestCmap() else fx
        cm=f.getBestCmap(); gs=f.getGlyphSet(); sc=size/f['head'].unitsPerEm; gn=cm[ord(ch)]
        pen=SVGPathPen(gs); gs[gn].draw(TransformPen(pen,(sc,0,0,-sc,cx,y))); d+=pen.getCommands(); cx+=gs[gn].width*sc+track
    return '<path fill="%s" d="%s"/>'%(fill,d)


def dpoly(hole,dtilt=11,k=1.22):
    hx,hy,_=hole; TK=math.tan(math.radians(dtilt)); ox=hx-1
    rel={'l1':(-24,-34),'l3':(-24,34),'t':(2,-34)}
    P={n:(ox+v[0]*k-v[1]*k*TK,hy+v[1]*k) for n,v in rel.items()}
    arc=[]
    for i in range(25):
        ang=-math.pi/2+math.pi*i/24
        px=2+34*math.cos(ang); py=34*math.sin(ang)
        arc.append((ox+px*k-py*k*TK,hy+py*k))
    return [P['l3'],P['l1'],P['t']]+arc[1:]
def _segd(p,a,b):
    ax,ay=a;bx,by=b;px,py=p
    dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy
    u=0 if L==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-(ax+u*dx),py-(ay+u*dy))
def poly_dist(p,poly):
    inside=False; n=len(poly); d=1e9
    for i in range(n):
        a=poly[i]; b=poly[(i+1)%n]
        d=min(d,_segd(p,a,b))
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]: inside=not inside
    return d,inside

def globe(main, accent, hole, cut=False, dp=None, R=107, nlat=24, nlon=40, seed=11):
    hx,hy,hr=hole
    rnd=random.Random(seed)
    tilt=math.radians(28); roll=math.radians(-25)
    def proj(lat,lon):
        x=math.cos(lat)*math.sin(lon); y=math.sin(lat); z=math.cos(lat)*math.cos(lon)
        y2=y*math.cos(tilt)-z*math.sin(tilt); z2=y*math.sin(tilt)+z*math.cos(tilt)
        x3=x*math.cos(roll)-y2*math.sin(roll); y3=x*math.sin(roll)+y2*math.cos(roll)
        return x3,-y3,z2
    out=[]
    for i in range(nlat):
        la0=-math.pi/2+math.pi*i/nlat; la1=-math.pi/2+math.pi*(i+1)/nlat
        for j in range(nlon):
            lo0=-math.pi+2*math.pi*j/nlon; lo1=-math.pi+2*math.pi*(j+1)/nlon
            cla,clo=(la0+la1)/2,(lo0+lo1)/2
            cx,cy,cz=proj(cla,clo)
            if cz<0.02: continue
            pts=[]
            for (a,b) in ((la0,lo0),(la0,lo1),(la1,lo1),(la1,lo0)):
                x,y,_=proj(lerp(cla,a,.6),lerp(clo,b,.6)); pts.append((x*R,y*R))
            ccx,ccy=cx*R,cy*R
            dd,ins=poly_dist((ccx,ccy),dp)
            if ins or dd<10: continue
            t=max(0,(cx*0.9-cy*0.35-0.5)/0.6)
            td=max(0,1-(dd-10)/26)
            tgp=t
            t=max(t,td)
            if cut:
                if ccx>56 and -36<ccy<60: continue
                bd=math.hypot(ccx-124,ccy-12)
                if bd<54: continue
                t=max(t,1-(bd-54)/34)
            if t>0:
                if rnd.random()< max(tgp**1.4*0.8,td**1.6*0.45): continue
                sc=1-0.45*t; ang=rnd.uniform(-0.7,0.7)*t*0.6-math.radians(11)*td; off=t*R*0.025
                np_=[]
                for (x,y) in pts:
                    dx,dy=(x-ccx)*sc,(y-ccy)*sc
                    dx,dy=dx*math.cos(ang)-dy*math.sin(ang),dx*math.sin(ang)+dy*math.cos(ang)
                    np_.append((ccx+dx+off,ccy+dy-off*0.3))
                pts=np_
            cl=[]
            for (x,y) in pts:
                r=math.hypot(x,y)
                if False: x,y=x*R*0.995/r,y*R*0.995/r
                cl.append((x,y))
            out.append((cl,mix(main,accent,min(1,t*1.4))))
    return out

def mark(main,accent,bg,dtilt=11,uid='a',cut=False):
    hole=(-2,3,57)
    tiles=globe(main,accent,hole,cut=cut,dp=dpoly(hole))
    g='<g clip-path="url(#cp%s)">'%uid+''.join('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.1" stroke-linejoin="round"/>'%(' '.join('%.1f,%.1f'%p for p in pts),c,c) for pts,c in tiles)+'</g>'
    # frame
    RR=107.5
    pt=lambda a:(RR*math.cos(math.radians(a)),RR*math.sin(math.radians(a)))
    if not cut:
        ring=f'<circle r="{RR}" fill="none" stroke="url(#fr{uid})" stroke-width="5.5"/>'
    else:
        def arc(a0,a1):
            x0,y0=pt(a0);x1,y1=pt(a1)
            return f'<path d="M{x0:.1f} {y0:.1f} A{RR} {RR} 0 {1 if (a1-a0)%360>180 else 0} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="url(#fr{uid})" stroke-width="5.5" stroke-linecap="round"/>'
        ring=arc(44,332)
    g=ring+g
    hx,hy,_=hole
    k=1.22; TK=math.tan(math.radians(dtilt)); ox=hx-1
    def sk(px,py): return (ox+px*k-py*k*TK,hy+py*k)
    L1=sk(-24,-34); L3=sk(-24,34); T=sk(2,-34); C=sk(-6,0)
    arcp=[sk(2+34*math.cos(-math.pi/2+math.pi*i/24),34*math.sin(-math.pi/2+math.pi*i/24)) for i in range(25)]
    f=lambda p:'%.1f %.1f'%p
    # closed outline sampled densely: stem (L3->L1), top edge, arc, bottom edge
    def seg(p,q,n): return [(p[0]+(q[0]-p[0])*i/n,p[1]+(q[1]-p[1])*i/n) for i in range(n)]
    outline=seg(L3,L1,14)+seg(L1,T,6)+arcp[:-1]+seg(arcp[-1],L3,6)
    N=len(outline)
    cum=[0.0]
    for i in range(1,2*N+1):
        p=outline[(i-1)%N]; q=outline[i%N]; cum.append(cum[-1]+math.hypot(q[0]-p[0],q[1]-p[1]))
    Lt=cum[N]
    def at(s):
        s%=Lt
        if s<0: s+=Lt
        # work on the doubled list
        for i in range(2*N):
            if cum[i]<=s<=cum[i+1] or (s<cum[0]):
                p=outline[i%N]; q=outline[(i+1)%N]; u=(s-cum[i])/max(1e-9,cum[i+1]-cum[i])
                return (p[0]+(q[0]-p[0])*u,p[1]+(q[1]-p[1])*u)
        return outline[0]
    # gap centres (arc length from L3, going up the stem, over the top, round the arc)
    stem=math.hypot(L1[0]-L3[0],L1[1]-L3[1]); top=math.hypot(T[0]-L1[0],T[1]-L1[1])
    arc_i=lambda i:cum[20+int(i)]+(i-int(i))*(cum[21+int(i)]-cum[20+int(i)])
    centres=[stem*0.62, arc_i(10.5), arc_i(19.5)]
    centres=sorted(centres); H=7.6
    paths=''; rings=''; pix=''; mids=[]; bridges=''
    for gi,c in enumerate(centres):
        a0=c+H; b0=(centres[(gi+1)%len(centres)]-H)
        if b0<=a0: b0+=Lt
        pts=[at(a0)]
        for i in range(2*N+1):
            if a0<cum[i]<b0 or (a0<cum[i]+Lt<b0 and False): pts.append(outline[i%N])
        if b0>Lt:
            pts=[at(a0)]+[outline[i%N] for i in range(2*N+1) if a0<cum[i]<b0]
        pts.append(at(b0))
        paths+='<path d="M'+' L'.join(f(q) for q in pts)+'"/>'
        for e in (c-H,c+H):
            q=at(e); rings+='<circle cx="%.1f" cy="%.1f" r="3.7" fill="%s" stroke="%s" stroke-width="1.8"/>'%(*q,bg,accent)
        m=at(c); mids.append(m)
        e0,e1=at(c-H),at(c+H)
        bridges+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(*e0,*e1)
        dx,dy=m[0]-C[0],m[1]-C[1]; dl=math.hypot(dx,dy); dx,dy=dx/dl,dy/dl
        for j,(dist,w) in enumerate(((8,3.6),(12.5,2.8),(16.5,2.0))):
            px,py=m[0]+dx*dist,m[1]+dy*dist
            pix+='<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" transform="rotate(-11 %.1f %.1f)"/>'%(px-w/2,py-w/2,w,w,accent,px,py)
    thick=f'<g fill="none" stroke="url(#dg{uid})" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round">{paths}</g>'
    cl2=''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(*C,*q) for q in mids)
    spk=f'<g stroke="{accent}" stroke-width="1.5" stroke-linecap="round">{cl2}</g>'
    spk+=f'<g stroke="{accent}" stroke-width="1.4" stroke-dasharray="1.6 2.4" stroke-linecap="round">{bridges}</g>'
    spk+=''.join('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>'%(*q,accent) for q in mids)
    g+=spk+thick+rings+pix
    g+=f'<circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="0.01" fill="none"/><circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="5.4" fill="{accent}" stroke="{bg}" stroke-width="1.6"/>'
    defs=f'<linearGradient id="dg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{mix(accent,main,0.6)}"/></linearGradient>'
    defs+=f'<linearGradient id="fr{uid}" gradientUnits="userSpaceOnUse" x1="-108" y1="-108" x2="108" y2="108"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{main}"/></linearGradient>'
    defs+=f'<clipPath id="cp{uid}"><circle r="99.5"/></clipPath>'
    return g,defs

def logo(path,pal,bg,icon=False,uid='a'):
    cut=not icon
    main,accent,ink,sub,frame=pal
    g,defs=mark(main,accent,bg,uid=uid,cut=cut)
    if frame: defs=defs.replace(f'stop-color="{accent}"/><stop offset="1" stop-color="{main}"',f'stop-color="{frame[0]}"/><stop offset="1" stop-color="{frame[1]}"')
    if icon:
        open(path,'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400"><defs>{defs}</defs>
<rect width="400" height="400" fill="{bg}"/><g transform="translate(198,200) scale(1.7)">{g}</g></svg>''')
        return
    sk=lambda s,y:'<g transform="translate(0,%d) skewX(-11) translate(0,-%d)">%s</g>'%(y,y,s)
    T1=sk(wm(MICH,'OYDEM',340,212,64,9,ink),212)
    T2=sk(wm(MICH,'YAZILIM',344,262,21,15,main),262)
    T3=sub_text('SANAYİ VE TİCARET LTD. ŞTİ.',344,296,13.5,3.4,sub)
    open(path,'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" width="800" height="420"><defs>{defs}</defs>
<rect width="800" height="420" fill="{bg}"/><g transform="translate(222,210) scale(1.8)">{g}</g>
{T1}
{T2}
{T3}
</svg>''')

C=('#1E2A78','#12B5A6','#12183B','#5B6080',None)
D=('#4B5FE8','#2EE6D0','#FFFFFF','#9AA6E8',None)
MN=('#12183B','#12183B','#12183B','#12183B',('#12183B','#12183B'))
PAL={'lacivert':(C,'#ffffff'),'koyu':(D,'#0B1030'),'tek-renk':(MN,'#ffffff')}
if __name__=='__main__':
    out=sys.argv[1] if len(sys.argv)>1 else '.'
    os.makedirs(out,exist_ok=True)
    for nm,(pal,bg) in PAL.items():
        logo(os.path.join(out,'oydem-v20-%s.svg'%nm),pal,bg,uid=nm[:2])
        logo(os.path.join(out,'oydem-v20-ikon-%s.svg'%nm),pal,bg,icon=True,uid=nm[:2]+'i')
