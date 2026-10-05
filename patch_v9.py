# -*- coding: utf-8 -*-
"""V9: dark/light theme system + loader removal + real catalog with real prices."""
import io, re

s = io.open('index.html', encoding='utf-8').read()

# ================= 1. REMOVE LOADER (markup/CSS/JS) =================
m1 = re.search(r'<!-- ================= LOADER ================= -->\n', s)
m2 = re.search(r'<!-- ================= NAV ================= -->', s)
assert m1 and m2, 'loader bounds missing'
s = s[:m1.start()] + s[m2.start():]

# loader CSS block
c1 = s.find('/* ============ LOADER')
c2 = s.find('/* ============ NAV ============ */')
assert c1 > 0 and c2 > c1, 'loader css missing'
s = s[:c1] + s[c2:]

# loader JS chunk
j1 = s.find("/* ---------- LOADER: pot fills")
j2 = s.find("/* ---------- NAV: scrolled bg")
assert j1 > 0 and j2 > j1, 'loader js missing'
s = s[:j1] + s[j2:]

# boot was also adding body.loaded — set it immediately instead
s = s.replace("$('#yr').textContent=arInt(new Date().getFullYear());",
              "$('#yr').textContent=arInt(new Date().getFullYear());\ndocument.body.classList.add('loaded');", 1)

# ================= 2. DARK/LIGHT THEME SYSTEM =================
# vars: add dark overrides + nav-bg/arch/tile semantic vars
old_vars = """  --bg:#f8f3ea; --card:#fffdf8; --soft:#f1e9db; --soft-2:#ece2cf;
  --ink:#262019; --mut:#8a7d6b;
  --gold:#8a6b25; --gold-2:#b0913d; --gold-deep:#6e5518;
  --terra:#7a5230; --terra-2:#e0924f; --amber:#d99a2b;
  --line:rgba(38,32,25,.12);"""
new_vars = """  --bg:#f6efe3; --card:#fffdf8; --soft:#f1e9db; --soft-2:#ece2cf;
  --ink:#262019; --mut:#8a7d6b;
  --gold:#8a6b25; --gold-2:#b0913d; --gold-deep:#6e5518;
  --terra:#c96f4a; --terra-2:#e0924f; --amber:#d99a2b;
  --line:rgba(38,32,25,.12);
  --nav-bg:rgba(248,243,234,.94);
  --tile-a:#eef1e6; --tile-b:var(--soft);
  --arch-a:#fbf7ef; --arch-b:var(--soft);
  --hero-grad-a:#fbf7ef; --hero-grad-b:var(--soft);"""
assert old_vars in s, 'vars not found'
s = s.replace(old_vars, new_vars, 1)

# dark overrides right after the :root block close
root_end = s.find('}', s.find(':root{')) + 1
dark_css = '''
html[data-theme="dark"]{
  --bg:#171009; --card:#221a10; --soft:#2a2013; --soft-2:#352a18;
  --ink:#f2e7d0; --mut:#aa9678;
  --gold:#cfa64a; --gold-2:#e6c878; --gold-deep:#9a7a26;
  --terra:#c98a5a; --terra-2:#e0a878; --amber:#e0b45c;
  --line:rgba(242,231,208,.13);
  --nav-bg:rgba(23,16,9,.92);
  --tile-a:#2e2416; --tile-b:#1f180e;
  --arch-a:#2b2213; --arch-b:#1e170c;
  --hero-grad-a:#2b2213; --hero-grad-b:#1e170c;
}'''
s = s[:root_end] + dark_css + s[root_end:]

# nav bg → var
s = s.replace(".nav.scrolled{background:rgba(248,243,234,.94);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);",
              ".nav.scrolled{background:var(--nav-bg);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);")
s = s.replace(".nav.scrolled{backdrop-filter:none;-webkit-backdrop-filter:none;background:rgba(248,243,234,.97)}",
              ".nav.scrolled{backdrop-filter:none;-webkit-backdrop-filter:none;background:var(--nav-bg)}")
# arch / tile / stage backgrounds → vars
s = s.replace("background:radial-gradient(80% 74% at 50% 30%,#eef1e6,var(--soft) 78%)}",
              "background:radial-gradient(80% 74% at 50% 30%,var(--tile-a),var(--tile-b) 78%)}")
s = s.replace("background:radial-gradient(80% 70% at 50% 22%,#fbf7ef,var(--soft) 78%);",
              "background:radial-gradient(80% 70% at 50% 22%,var(--arch-a),var(--arch-b) 78%);")
s = s.replace("background:radial-gradient(70% 60% at 50% 32%,#eef1e6,var(--soft-2) 80%);overflow:hidden;box-shadow:var(--shadow)}",
              "background:radial-gradient(70% 60% at 50% 32%,var(--tile-a),var(--tile-b) 80%);overflow:hidden;box-shadow:var(--shadow)}")
s = s.replace("background:radial-gradient(80% 70% at 50% 22%,var(--hero-grad-a),var(--hero-grad-b) 78%);",
              "background:radial-gradient(80% 70% at 50% 22%,var(--hero-grad-a),var(--hero-grad-b) 78%);")
# doodles visible in dark
s = s.replace('.doodle{position:absolute;opacity:.06;will-change:transform}',
              '.doodle{position:absolute;opacity:.06;will-change:transform}\nhtml[data-theme="dark"] .doodle svg{stroke:#f2e7d0}')

# theme toggle button in nav (before cart)
s = s.replace('''      <button class="cart-btn" id="cart-btn" aria-label="سلة التسوق">''',
'''      <button class="theme-btn" id="theme-btn" aria-label="الوضع الليلي / النهاري">
        <svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>
        <svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>''', 1)

# theme-btn CSS
s = s.replace('''.cart-btn{position:relative;width:44px;height:44px;border-radius:13px;border:1.5px solid var(--line);''',
'''.theme-btn{width:44px;height:44px;border-radius:13px;border:1.5px solid var(--line);
  display:grid;place-items:center;background:var(--card);color:var(--ink);transition:border-color .3s ease,color .3s ease}
.theme-btn:hover{border-color:var(--gold)}
.theme-btn .ic-sun{display:none}
html[data-theme="dark"] .theme-btn .ic-moon{display:none}
html[data-theme="dark"] .theme-btn .ic-sun{display:block}
.cart-btn{position:relative;width:44px;height:44px;border-radius:13px;border:1.5px solid var(--line);''')

# theme JS: init from localStorage (default dark) + toggle
s = s.replace("$('#yr').textContent=arInt(new Date().getFullYear());",
"""const savedTheme=localStorage.getItem('awanista-theme')||'dark';
document.documentElement.setAttribute('data-theme',savedTheme);
const themeBtn=$('#theme-btn');
if(themeBtn)themeBtn.addEventListener('click',()=>{
  const nt=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',nt);
  localStorage.setItem('awanista-theme',nt);
});
$('#yr').textContent=arInt(new Date().getFullYear());""", 1)

# ================= 3. EMAIL + LOGO =================
s = s.replace('hello@sekkeena.com', 'info@awanista.com')

# ================= 4. REAL CATALOG (13 items, real prices) =================
p1 = s.find('const products=[')
p2 = s.find('];', p1) + 2
assert p1 > 0, 'products not found'
new_products = '''const products=[
 {img:'img/tray-gold-set.jpg', imgs:['img/tray-gold-set.jpg','img/tray-gold-2.jpg','img/tray-gold-3.jpg','img/tray-gold-4.jpg'],
  cat:'صواني', name:'طقم صواني تقديم استانلس دهبي 2 قطعة', price:'٢٢٤٩', n:2249, old:'٢٩٩٩',
  rate:'٤.٩', revs:87, tag:'فخم', desc:'لمسة من الأناقة والفخامة إلى سفرتك ✨\\nطقم صواني التقديم الاستانلس المستورد بتصميم راقٍ ولمسات ذهبية مميزة\\n📦 طقم مكون من 2 قطعة بأحجام عملية (صينية كبيرة وأخرى متوسطة)\\n💪 استانلس ستيل عالي الجودة يدوم طويلًا\\n🎨 طلاء ذهبي أنيق يمنح الصواني مظهرًا فاخرًا\\n☕ مناسب لتقديم الحلويات، المشروبات، القهوة، الشاي والضيافة\\n🧽 سهل التنظيف ويحافظ على لمعانه\\n👌 مقابض جانبية مريحة وتصميم كلاسيكي فاخر بحواف مزخرفة'},
 {img:'img/tefal-set.jpg', imgs:['img/tefal-set.jpg','img/tefal-box.jpg','img/tefal-2.jpg','img/tefal-3.jpg'],
  cat:'أواني', name:'طقم حلل Evita الحداد التركي 16 قطعة', price:'٥٩٩٩', n:5999, old:'٧٤٩٩',
  rate:'٤.٩', revs:132, tag:'الأكثر مبيعاً', hot:true, desc:'تجربة طهي احترافية مع طقم Evita الحداد التركي الأصلي 🇹🇷\\n🍳 طبقة جرانيت غير لاصقة تقلل الزيوت وتسهل التنظيف\\n🔥 توزيع متساوٍ للحرارة لطهي مثالي في وقت أقل\\n💪 خامات متينة تتحمل الاستخدام اليومي\\n👁️ أغطية زجاج حراري لمتابعة الطعام\\n👌 مقابض مريحة وعازلة للحرارة\\n📦 16 قطعة تناسب جميع احتياجات الأسرة'},
 {img:'img/tefal-set.jpg', imgs:['img/tefal-set.jpg','img/tefal-box.jpg','img/tefal-2.jpg','img/tefal-3.jpg'],
  cat:'أواني', name:'طقم حلل Evita الحداد التركي 18 قطعة', price:'٦٧٩٩', n:6799, old:'٨٤٩٩',
  rate:'٤.٩', revs:98, tag:'شامل', desc:'طقم Evita 18 قطعة — كل اللي مطبخك محتاجه في طقم واحد 🇹🇷\\n🍳 جرانيت غير لاصق + توزيع حراري مثالي\\n📦 18 قطعة بمقاسات عملية'},
 {img:'img/tefal-set.jpg', imgs:['img/tefal-set.jpg','img/tefal-box.jpg','img/tefal-2.jpg','img/tefal-3.jpg'],
  cat:'أواني', name:'طقم حلل Evita الحداد التركي 20 قطعة', price:'٧٥٩٩', n:7599, old:'٩٤٩٩',
  rate:'٥.٠', revs:76, tag:'الأكبر', desc:'طقم Evita 20 قطعة — التشكيلة الكاملة 🇹🇷\\n🍳 جرانيت غير لاصق + كل المقاسات\\n📦 20 قطعة تغطي كل احتياجات المطبخ'},
 {img:'img/tray-box.jpg', imgs:['img/tray-box.jpg','img/tray-black.jpg','img/tray-maroon.jpg'],
  cat:'صواني', name:'طقم صواني جرانيت Martev التركي 3 قطع', price:'١٤٩٩', n:1499, old:'١٩٩٩',
  rate:'٤.٨', revs:64, tag:'تركي', desc:'أشهى المخبوزات وأكلات الفرن مع طقم صواني جرانيت Martev التركي 🇹🇷\\n📦 3 مقاسات (26/28/30 سم)\\n🍳 طبقة جرانيت غير لاصقة تمنع الالتصاق\\n🔥 توزيع متساوٍ للحرارة\\n💪 خامات متينة تتحمل الحرارة العالية\\n🍕 مثالي للكيك، البطاطس، المكرونة بالبشاميل وكل أكلات الفرن'},
 {img:'img/frypan-box.jpg', imgs:['img/frypan-box.jpg','img/frypan-red.jpg','img/frypan-black.jpg'],
  cat:'مقالي', name:'طقم مقلايات جرانيت تركي Martev 20/24/28', price:'١٣٤٩', n:1349, old:'١٧٩٩',
  rate:'٤.٨', revs:74, tag:'تركي', desc:'طقم المقلايات الجرانيت التركي وصل 🔥\\n👩‍🍳 ٣ مقاسات مختلفة (20/24/28 سم)\\n💪 جرانيت تقيل وجودة عالية\\n🍳 غير لاصق نهائي وسهل التنضيف\\n🔥 توزيع حراري ممتاز\\n🎁 لمسة تركية فخمة لمطبخك'},
 {img:'img/kanaka-red.jpg', imgs:['img/kanaka-red.jpg','img/kanaka-pour.jpg'],
  cat:'إكسسوارات', name:'طقم كنك جرانيت 3 قطع مع حامل ☕', price:'٩٧٤', n:974, old:'١٢٩٩',
  rate:'٤.٩', revs:91, tag:'جرانيت', desc:'لكل عشاق القهوة 😍\\nطقم كنك جرانيت 3 قطع مع حامل معدني أنيق\\n💪 خامة جرانيت تقيلة\\n🔥 توزيع متساوٍ للحرارة لقهوة غنية بالمذاق\\n☕ مناسب للقهوة التركية، الحليب والنسكافيه'},
 {img:'img/kanaka-purple.jpg', imgs:['img/kanaka-purple.jpg','img/kanaka-black.jpg'],
  cat:'إكسسوارات', name:'طقم كنك استانلس 3 قطع مع حامل ☕', price:'٧٩٩', n:799, old:'٩٩٩',
  rate:'٤.٧', revs:56, tag:'ستنلس', desc:'كنك استانلس أنيق بيد ستايل تركي 🇹🇷\\n💪 خامة تقيلة وجودة عالية\\n☕ قهوتك تطلع مظبوطة كل مرة'},
 {img:'img/standard-axis.jpg', imgs:['img/standard-axis.jpg','img/standard-lemon.jpg'],
  cat:'أواني', name:'طقم حلل Axis Stand استانلس 10 قطعة', price:'٣٨٤٩', n:3849, old:'٤٤٩٩',
  rate:'٤.٨', revs:113, tag:'ستانلس 304', desc:'أفضل أداء في مطبخك مع طقم Axis Stand استانلس ستيل 304 💎\\n💪 مقاوم للصدأ والتآكل\\n🔥 توزيع متساوٍ للحرارة\\n👁️ أغطية محكمة تحافظ على النكهة\\n👌 مناسب لمعظم أنواع البوتاجازات'},
 {img:'img/haddad-yonca.jpg', imgs:['img/haddad-yonca.jpg'],
  cat:'أواني', name:'طقم حلل استيل الحداد التركي 10 قطعة', price:'٥٤٩٩', n:5499, old:'٦٩٩٩',
  rate:'٤.٩', revs:87, tag:'تركي', desc:'أعلى مستويات الجودة مع طقم الحداد التركي 🇹🇷\\n💪 استانلس مقاوم للصدأ\\n🔥 توزيع متساوٍ للحرارة\\n👁️ أغطية محكمة\\n✔️ علامة الجودة الخاصة بالمصنع'},
 {img:'img/ceramic-linezon.jpg', imgs:['img/ceramic-linezon.jpg'],
  cat:'أواني', name:'طقم حلل سيراميك Linezon الكوري 11 قطعة', price:'٥٢٩٩', n:5299, old:'٥٩٩٩',
  rate:'٤.٨', revs:104, tag:'كوري', desc:'جودة الطهي مع سيراميك Linezon الكوري الأصلي 🇰🇷\\n🍳 سيراميك غير لاصق + توزيع متساوٍ للحرارة\\n👁️ أغطية زجاج حراري\\n📦 11 قطعة'},
 {img:'img/granite-black.jpg', imgs:['img/granite-black.jpg','img/granite-pink.jpg'],
  cat:'أواني', name:'طقم حلل جرانيت Linezon Die Cast كوري 11 قطعة', price:'٤٩٩٩', n:4999, old:'٥٤٩٩',
  rate:'٤.٩', revs:141, tag:'Die Cast', desc:'تقنية Die Cast الكورية الأصلية — قاعدة مصبوبة لمتانة أطول 🇰🇷\\n🍳 جرانيت غير لاصق + توزيع حرارة أعلى\\n📦 11 قطعة'},
 {img:'img/silicone-black.jpg', imgs:['img/silicone-black.jpg','img/silicone-pink.jpg','img/silicone-gray.jpg'],
  cat:'إكسسوارات', name:'طقم أدوات مطبخ سيليكون 12 قطعة بيد خشب', price:'٥٩٩', n:599, old:'٧٠٠',
  rate:'٤.٩', revs:167, tag:'12 قطعة', desc:'سيليكون غذائي مقاوم للحرارة + مقابض خشبية مريحة\\n🚫 لا يمتص الروائح ولا يخدش الطاسات\\n🎁 حامل أنيق يحافظ على الترتيب'}
];'''
s = s[:p1] + new_products + s[p2:]

io.open('index.html', 'w', encoding='utf-8', newline='').write(s)
print('v9 applied: loader gone + dark/light theme + real catalog')
