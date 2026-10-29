// manifest.json içindeki HTML dosyalarını PDF ve PNG'ye çevirir (Playwright gerekir).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..')+'/';
(async()=>{
  const list=JSON.parse(fs.readFileSync(ROOT+'araclar/manifest.json','utf8'));
  const b=await chromium.launch();
  for(const m of list){
    const pxw=m.unit==='mm'?Math.round(m.w*96/25.4):m.w, pxh=m.unit==='mm'?Math.round(m.h*96/25.4):m.h;
    const scale=m.unit==='mm'?(m.w<100?4:2.5):1;
    const p=await b.newPage({viewport:{width:pxw,height:pxh},deviceScaleFactor:scale});
    await p.goto('file://'+ROOT+m.html); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(150);
    const els=await p.$$('.page');
    for(let i=0;i<els.length;i++){
      await els[i].screenshot({path:ROOT+m.out+(els.length>1?'-'+(i+1):'')+'.png'});
    }
    if(m.pdf){
      await p.addStyleTag({content:`@page{size:${m.w}${m.unit} ${m.h}${m.unit};margin:0}`});
      await p.pdf({path:ROOT+m.out+'.pdf',width:m.w+m.unit,height:m.h+m.unit,printBackground:true,preferCSSPageSize:true});
    }
    await p.close();
  }
  await b.close(); console.log('render tamam');
})();
