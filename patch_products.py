# -*- coding: utf-8 -*-
"""Patch index.html: real products + product modal + hero photo collage."""
import io, re

s = io.open('index.html', encoding='utf-8').read()

# ---- 1. hero markup: canvas → real-photo collage ----
old_hero = re.search(r'    <div class="hero-3d" aria-hidden="true">\n.*?\n    </div>\n\n    <div class="hero-ctas">', s, re.S)
assert old_hero, 'hero 3d markup not found'
new_hero = '''    <div class="hero-3d" aria-hidden="true">
      <div class="hv-arch">
        <img class="hv-photo" src="img/granite-pink.jpg" alt="طقم حلل جرانيت سافلون الكوري">
      </div>
      <div class="hv-mini">
        <img src="img/silicone-black.jpg" alt="طقم توزيع سيليكون مستورد">
      </div>
      <div class="hv-badge hv-b1">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 15 8.5 22 9.3 17 14l1.2 7L12 17.8 5.8 21 7 14 2 9.3 9 8.5z"/></svg>
        تقييم ٤.٩ من ٥
      </div>
      <div class="hv-badge hv-b2">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>
        خصم لحد ٣٠٪
      </div>
    </div>

    <div class="hero-ctas">'''
s = s[:old_hero.start()] + new_hero + s[old_hero.end():]

# ---- 2. hero CSS: arch photo + mini card (replace canvas rules) ----
s = s.replace('''.hv-arch{position:absolute;inset-inline:0;top:0;bottom:6%;
  border-radius:999px 999px 28px 28px / 460px 460px 28px 28px;
  background:radial-gradient(80% 70% at 50% 22%,#fbf7ef,var(--soft) 78%);
  border:1px solid var(--line);box-shadow:var(--shadow)}
.hv-arch::before{content:"";position:absolute;inset:0;border-radius:inherit;
  background:radial-gradient(58% 44% at 50% 30%,rgba(93,138,107,.15),transparent 70%)}
#hv-gl{position:absolute;inset:0;width:100%;height:100%;z-index:1;display:block;touch-action:pan-y;cursor:grab}
#hv-gl:active{cursor:grabbing}''',
'''.hv-arch{position:absolute;inset-inline:0;top:0;bottom:0;
  border-radius:999px 999px 28px 28px / 460px 460px 28px 28px;
  border:1px solid var(--line);box-shadow:var(--shadow);overflow:hidden;background:var(--soft)}
.hv-photo{width:100%;height:100%;object-fit:cover;object-position:center 65%;display:block}
.hv-arch::after{content:"";position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(248,243,234,.3),transparent 45%)}
.hv-mini{position:absolute;bottom:-7%;inset-inline-start:-5%;width:40%;border-radius:20px;overflow:hidden;
  border:5px solid var(--card);box-shadow:0 26px 54px -26px rgba(38,32,25,.55);transform:rotate(-3deg);z-index:2}
.hv-mini img{width:100%;display:block}''')

# ---- 3. remove the hero three.js module script ----
old_mod = re.search(r'<script type="module">\n/\* ---------- HERO: realistic 3D pot.*?</script>\n</body>', s, re.S)
assert old_mod, 'hero module not found'
s = s[:old_mod.start()] + '</body>' + s[old_mod.end():]

# ---- 4. products: real items first (photos + long desc + 3D model mapping) ----
old_products = re.search(r'const products=\[.*?\];\n', s, re.S)
assert old_products, 'products not found'
new_products = '''const products=[
 {img:'img/granite-pink.jpg', imgs:['img/granite-pink.jpg','img/granite-black.jpg'],
  cat:'مقالي', name:'طقم حلل جرانيت سافلون الكوري 🇰🇷', price:'٢٤٩٩', n:2499, old:'٢٩٩٩',
  rate:'٤.٩', revs:186, tag:'الأكثر مبيعاً', hot:true, model:'models/cooking-pot.glb',
  desc:'الطقم اللي يجمع بين الشياكة والجودة في نفس الوقت 😍\\nخامة جرانيت أصلية 💎 بتوزع الحرارة بالتساوي والطبيخ بيطلع مظبوط ولذيذ 👩‍🍳🔥\\n💪 متين وهيعيش معاكي سنين\\n🧽 سهل التنضيف جدًا ومش بيلزق\\n💨 الغطا محكم يحافظ على النكهة والطعم\\n🎨 ألوانه تحفة وتدي لمسة فخامة لمطبخك\\nخلي مطبخك كوري على أصوله 🇰🇷\\nواختاري الجودة اللي تليق بيكي 👑\\n📦 متوفر بألوان وأحجام مختلفة\\n📞 احجزي طقمك قبل ما يخلص 💥'},
 {img:'img/ceramic-linezon.jpg', imgs:['img/ceramic-linezon.jpg','img/ceramic-pink.jpg'],
  cat:'أواني', name:'طقم حلل سيراميك لينزون الكوري 💜', price:'٢٧٥٠', n:2750, old:'٣٢٠٠',
  rate:'٤.٨', revs:142, tag:'جديد', model:'models/cooking-pot.glb',
  desc:'الجمال الكوري وصل مطبخك 😍\\nألوان فخمة ولمعة تخطف العين ✨\\nوخامة سيراميك أصلية 💯 بتوزع الحرارة كويس والطبيخ بيطلع مظبوط ولذيذ 👩‍🍳🔥\\n💪 متين وهيعيش معاكي سنين\\n🧽 سهل التنضيف جدًا ومش بيلزق\\n💨 الغطا محكم بيحافظ على الطعم والروايح\\n👌 شكل أنيق يدي لمسة فخامة لمطبخك\\nخلي مطبخك شيك بجودة كورية على أصولها 🇰🇷💎\\nواختاري الطقم اللي يليق بيكي 💕\\n📦 متوفر بألوان وأحجام مختلفة\\n📞 احجزي طقمك قبل ما يخلص 💥'},
 {img:'img/silicone-black.jpg', imgs:['img/silicone-black.jpg','img/silicone-pink.jpg','img/silicone-gray.jpg'],
  cat:'إكسسوارات', name:'طقم توزيع سيليكون مستورد 💎', price:'٣٧٥', n:375, old:'٤٩٠',
  rate:'٤.٩', revs:203, tag:'وصل حديثًا', model:'models/wooden-spatula.glb',
  desc:'لو بتدوري على الأناقة والعملية في نفس الوقت 👌\\nالطقم ده هيكون إضافة شيك لمطبخك 💕\\n🔥 يتحمّل الحرارة العالية من غير ما يتأثر\\n🧽 سهل التنضيف جدًا\\n🚫 مش بيلزق ومش بيجرّح الحلل\\n💪 خامة سيليكون تقيلة وجودة مستوردة 💯\\n🎨 ألوانه تحفة وتفتح النفس 😍\\nخلي مطبخك ستايل ومريح في الاستخدام ✨\\nواختاري الطقم اللي يسهّل عليكي كل طبخة 👩‍🍳💜\\n📦 متوفر دلوقتي بألوان مختلفة\\n📞 احجزي طقمك قبل ما يخلص 💥'}
];'''
s = s[:old_products.start()] + new_products + s[old_products.end():]

# ---- 5. catalog: real products first, then the 16 3D models (deduped) ----
s = s.replace('''/* full catalog = the 16 3D models + the 6 essentials above (deduped by name) */
const catalog=(function(){
  const seen=new Set(products.map(p=>p.name));
  const extra=MODELS
    .filter(function(m){return !seen.has(m.name)})
    .map(function(m){return {art:m.art,cat:m.cat,name:m.name,price:arInt(m.n),n:m.n,old:m.old?arInt(m.old):0,rate:m.rate,tag:m.cat}});
  return extra.concat(products);
})();''',
'''/* full catalog = the real photo products first, then the 16 3D models */
const catalog=products.concat(MODELS.filter(function(m){return !products.some(function(p){return p.model===m.src})}))
  .map(function(p){return {img:p.img,imgs:p.imgs,desc:p.desc,model:p.model,
    art:p.art,cat:p.cat,name:p.name,price:p.price,n:p.n,old:p.old,rate:p.rate,tag:p.tag,hot:p.hot}});''')

# old: old price may be string '٢٤٩' in products or number in MODELS — normalize price/old at map: price uses arInt(p.n) in template? The card uses p.price (string) ✓ MODELS lack price string! MODELS entries have n only. In the mapped catalog add price: arInt(m.n)+' ج.م'? The template does ${p.price} ج.م — MODELS p.price undefined → "undefined ج.م"! Fix in map: price: p.price||arInt(p.n). Apply below.

# ---- 6. card template: photo support + modal open ----
s = s.replace('''     <div class="p-tile">
     <span class="p-tag ${p.hot?'hot':''}">${p.tag||p.cat}</span>
     <div class="art">${ART[p.art]}</div>
   </div>''',
'''     <div class="p-tile">
     <span class="p-tag ${p.hot?'hot':''}">${p.tag||p.cat}</span>
     ${p.img?`<img class="p-img" src="${p.img}" loading="lazy" alt="${p.name}">`:`<div class="art">${ART[p.art]}</div>`}
   </div>''')

# price normalization inside the catalog map (MODELS have no price string)
s = s.replace("price:p.price,n:p.n,old:p.old,rate:p.rate,tag:p.tag,hot:p.hot}});",
              "price:p.price||arInt(p.n),n:p.n,old:p.old||'',rate:p.rate,tag:p.tag||p.cat,hot:p.hot}});")

# old price string in template: normalize old display in card: p.old may be number → template uses ${p.old} — for MODELS-derived old:'' ✓ fine; for products old:'٢٤٩' string ✓.

# ---- 7. click card → modal (and + still adds) ----
s = s.replace("$('#p-grid').addEventListener('click',e=>{\n  const b=e.target.closest('[data-add]');if(!b)return;",
"""$('#p-grid').addEventListener('click',e=>{
  const add=e.target.closest('[data-add]');
  if(add){const p=catalog[+add.dataset.add];addToCart({name:p.name,n:p.n,img:p.img,art:p.art});toastShow(p.name+' — اتضاف للسلة');return}
  const cardEl=e.target.closest('.p-card');
  if(cardEl){openModal(+cardEl.dataset.add);return}""")

# ---- 8. modal markup after cart drawer ----
anchor_cart = re.search(r'</aside>\n\n<main>', s)
assert anchor_cart, 'cart anchor not found'
modal_html = '''</aside>

<!-- ================= PRODUCT MODAL ================= -->
<div class="pmodal-ov" id="pmodal-ov"></div>
<aside class="pmodal" id="pmodal" role="dialog" aria-modal="true">
  <button class="pm-close" id="pm-close" aria-label="قفل">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
  </button>
  <div class="pm-body">
    <span class="mv-cat" id="pm-cat"></span>
    <h3 id="pm-name"></h3>
    <div class="pm-rate" id="pm-rate"></div>
    <p class="pm-desc" id="pm-desc"></p>
    <div class="pm-prices"><b id="pm-price"></b><s id="pm-old"></s></div>
    <div class="pm-qtyrow">
      <span>الكمية</span>
      <div class="pm-qty">
        <button class="qty-btn" id="pm-minus" aria-label="أقل"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14"/></svg></button>
        <b id="pm-qty">١</b>
        <button class="qty-btn" id="pm-plus" aria-label="أكثر"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button>
      </div>
    </div>
    <button class="btn btn-primary pm-addbtn" id="pm-add">أضف للسلة
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
    </button>
    <p class="pm-note">شحن مجاني فوق ٢٠٠ ج.م · الدفع عند الاستلام</p>
  </div>
  <div class="pm-media">
    <div class="pm-photo" id="pm-photo"></div>
    <div class="pm-thumbs" id="pm-thumbs"></div>
    <div class="pm-3dbox" id="pm-3dbox">
      <canvas id="pm-gl"></canvas>
      <span class="pm-3dtag">3D — لفّها بإيدك</span>
    </div>
  </div>
</aside>

<main>'''
s = s[:anchor_cart.start()] + modal_html + s[anchor_cart.end():]

# ---- 9. modal CSS (append to style) ----
s = s.replace('''/* ============ 3D GALLERY ============ */''',
'''/* ============ PRODUCT MODAL ============ */
.pmodal-ov{position:fixed;inset:0;z-index:1100;background:rgba(38,32,25,.55);opacity:0;visibility:hidden;
  transition:opacity .35s ease,visibility .35s}
body.pm-open .pmodal-ov{opacity:1;visibility:visible}
.pmodal{position:fixed;top:50%;left:50%;transform:translate(-50%,-46%);z-index:1101;width:min(960px,94vw);
  max-height:90vh;overflow:auto;background:var(--card);border-radius:28px;display:flex;flex-direction:row-reverse;
  opacity:0;visibility:hidden;transition:opacity .4s ease,transform .4s var(--ease),visibility .4s;
  box-shadow:0 50px 120px -40px rgba(38,32,25,.6)}
body.pm-open .pmodal{opacity:1;visibility:visible;transform:translate(-50%,-50%)}
.pm-close{position:absolute;top:14px;inset-inline-start:14px;z-index:5;width:40px;height:40px;border-radius:12px;
  border:1.5px solid var(--line);background:var(--card);display:grid;place-items:center;color:var(--mut);
  transition:color .3s ease,border-color .3s ease}
.pm-close:hover{color:var(--terra);border-color:var(--terra)}
.pm-close svg{width:16px;height:16px}
.pm-body{flex:1.05;padding:30px 28px;min-width:0}
.pm-body h3{font-family:var(--font-d);font-weight:700;font-size:1.5rem;line-height:1.4;margin-top:8px}
.pm-rate{display:flex;align-items:center;gap:6px;color:var(--amber);font-weight:800;font-size:.88rem;margin-top:6px}
.pm-rate svg{width:14px;height:14px}
.pm-rate small{color:var(--mut);font-weight:700}
.pm-desc{color:var(--ink);font-size:.95rem;line-height:1.95;margin-top:14px}
.pm-desc span{display:block;padding:2px 0}
.pm-prices{display:flex;align-items:baseline;gap:10px;margin-top:14px}
.pm-prices b{font-family:var(--font-d);font-weight:700;font-size:1.7rem;color:var(--green)}
.pm-prices s{color:var(--mut);font-size:1rem}
.pm-qtyrow{display:flex;align-items:center;gap:14px;margin-top:16px;font-weight:800;font-size:.92rem}
.pm-qty{display:flex;align-items:center;gap:10px}
.pm-qty b{min-width:30px;text-align:center;font-size:1.05rem}
.pm-addbtn{width:100%;margin-top:18px}
.pm-note{color:var(--mut);font-size:.8rem;font-weight:700;text-align:center;margin-top:10px}
.pm-media{flex:1;background:var(--soft);display:flex;flex-direction:column;min-width:0}
.pm-photo{flex:1;min-height:280px;display:grid;place-items:center;overflow:hidden}
.pm-photo img{width:100%;height:100%;object-fit:cover}
.pm-photo .art{width:62%}
.pm-thumbs{display:flex;gap:8px;padding:12px;justify-content:center;flex-wrap:wrap}
.pm-thumbs img{width:54px;height:54px;object-fit:cover;border-radius:12px;border:2px solid var(--line);
  cursor:pointer;transition:border-color .3s ease}
.pm-thumbs img.on{border-color:var(--green)}
.pm-3dbox{height:250px;border-top:1px solid var(--line);position:relative;display:none;background:radial-gradient(70% 60% at 50% 40%,#eef1e6,var(--soft-2) 80%)}
.pm-3dbox.on{display:block}
.pm-3dbox canvas{width:100%;height:100%;display:block;touch-action:pan-y;cursor:grab}
.pm-3dtag{position:absolute;bottom:10px;inset-inline-start:50%;transform:translateX(50%);padding:6px 14px;border-radius:99px;
  background:rgba(38,32,25,.6);color:var(--bg);font-weight:700;font-size:.74rem;white-space:nowrap}

/* ============ 3D GALLERY ============ */''', 1)

# ---- 10. cart img thumbs ----
s = s.replace("      <div class=\"cd-thumb\">${ART[it.art]||''}</div>",
              "      <div class=\"cd-thumb\">${it.img?`<img src=\"${it.img}\" alt=\"\">`:ART[it.art]||''}</div>")
s = s.replace(".cd-thumb svg{width:78%;height:78%}",
              ".cd-thumb svg{width:78%;height:78%}\n.cd-thumb img{width:100%;height:100%;object-fit:cover;border-radius:10px}")

io.open('index.html', 'w', encoding='utf-8', newline='').write(s)
print('patched: products+modal+hero collage')
