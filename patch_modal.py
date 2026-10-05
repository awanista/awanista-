# -*- coding: utf-8 -*-
"""Patch 2: modal JS + modal 3D module + mobile modal CSS."""
import io

s = io.open('index.html', encoding='utf-8').read()

# ---- 1. modal logic into the main classic script (before counters chunk) ----
anchor = '/* ---------- COUNTERS (count up on scroll) ---------- */'
assert anchor in s, 'counters anchor missing'
modal_js = '''/* ---------- PRODUCT MODAL ---------- */
let pmItem=null,pmQty=1;
const pmEl=$('#pmodal'),pmOv=$('#pmodal-ov');
function openModal(i){
  pmItem=catalog[i];pmQty=1;
  $('#pm-cat').textContent=pmItem.cat;
  $('#pm-name').textContent=pmItem.name;
  $('#pm-rate').innerHTML=star.repeat(5)+'<small>'+(pmItem.rate||'٤.٨')+' ('+arInt(pmItem.revs||0)+' تقييم)</small>';
  $('#pm-desc').innerHTML=(pmItem.desc||'').split('\\n').filter(function(l){return l}).map(function(l){return '<span>'+l+'</span>'}).join('');
  $('#pm-price').textContent=pmItem.price+' ج.م';
  $('#pm-old').textContent=pmItem.old?pmItem.old+' ج.م':'';
  const photo=$('#pm-photo'),thumbs=$('#pm-thumbs');
  if(pmItem.img){
    photo.innerHTML='<img src="'+pmItem.img+'" alt="'+pmItem.name+'">';
    thumbs.innerHTML=pmItem.imgs.map(function(im,k){return '<img src="'+im+'" data-k="'+k+'" class="'+(k?'':'on')+'" alt="">'}).join('');
    thumbs.onclick=function(e){
      const t=e.target.closest('img');if(!t)return;
      $('#pm-img').src=pmItem.imgs[+t.dataset.k];
      thumbs.querySelectorAll('img').forEach(function(im,k2){im.classList.toggle('on',k2===+t.dataset.k)});
    };
  }else{
    photo.innerHTML='<div class="art">'+(ART[pmItem.art]||'')+'</div>';
    thumbs.innerHTML='';
  }
  const box=$('#pm-3dbox');
  if(pmItem.model){
    box.classList.add('on');
    dispatchEvent(new CustomEvent('pm-3d',{detail:{src:pmItem.model}}));
  }else box.classList.remove('on');
  $('#pm-qty').textContent=arInt(pmQty=1);
  document.body.classList.add('pm-open');
  document.documentElement.classList.add('lock');
  wake();
}
function closeModal(){
  document.body.classList.remove('pm-open');
  document.documentElement.classList.remove('lock');
  dispatchEvent(new Event('pm-3d-off'));
}
$('#pm-close').addEventListener('click',closeModal);
pmOv.addEventListener('click',closeModal);
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){closeModal();closeCart();document.body.classList.remove('menu-open')}
});
$('#pm-plus').addEventListener('click',()=>{pmQty=clamp(pmQty+1,1,99);$('#pm-qty').textContent=arInt(pmQty)});
$('#pm-minus').addEventListener('click',()=>{pmQty=clamp(pmQty-1,1,99);$('#pm-qty').textContent=arInt(pmQty)});
$('#pm-add').addEventListener('click',()=>{
  if(!pmItem)return;
  addToCart({name:pmItem.name,n:pmItem.n,img:pmItem.img,art:pmItem.art},pmQty);
  toastShow(pmItem.name+' — اتضاف للسلة ('+arInt(pmQty)+')');
  setTimeout(closeModal,450);
});

''' + anchor
s = s.replace(anchor, modal_js, 1)

# addToCart accepts qty
s = s.replace('''function addToCart(item){
  const found=cartArr.find(it=>it.name===item.name);
  if(found)found.qty++;else cartArr.push({name:item.name,n:item.n,art:item.art,qty:1});
  renderCart();
}''',
'''function addToCart(item,qty){
  const q=qty||1;
  const found=cartArr.find(it=>it.name===item.name);
  if(found)found.qty+=q;else cartArr.push({name:item.name,n:item.n,img:item.img||'',art:item.art||'',qty:q});
  renderCart();
}''')
s = s.replace("if(found)found.qty++;else cartArr.push({idx,qty:1});", "if(found)found.qty++;else cartArr.push({idx,qty:1});")  # noop guard
# p-grid quick-add passes qty 1 explicitly (uses addToCart(item) default ✓)
# cart items now may carry img — renderCart thumb
s = s.replace("      <div class=\"cd-thumb\">${ART[it.art]||''}</div>",
              "      <div class=\"cd-thumb\">${it.img?`<img src=\"${it.img}\" alt=\"\">`:ART[it.art]||''}</div>")

# ---- 2. modal mobile CSS ----
s = s.replace('''.pm-3dtag{position:absolute;bottom:10px;inset-inline-start:50%;transform:translateX(50%);padding:6px 14px;border-radius:99px;
  background:rgba(38,32,25,.6);color:var(--bg);font-weight:700;font-size:.74rem;white-space:nowrap}''',
'''.pm-3dtag{position:absolute;bottom:10px;inset-inline-start:50%;transform:translateX(50%);padding:6px 14px;border-radius:99px;
  background:rgba(38,32,25,.6);color:var(--bg);font-weight:700;font-size:.74rem;white-space:nowrap}
@media (max-width:760px){
  .pmodal{flex-direction:column-reverse;width:100vw;max-height:94vh;border-radius:24px 24px 0 0;
    top:auto;bottom:0;left:0;transform:translateY(10%)}
  body.pm-open .pmodal{transform:translateY(0)}
  .pm-photo{min-height:210px}
  .pm-media{flex:none}
  .pm-body{padding:22px 20px}
}''')

io.open('index.html', 'w', encoding='utf-8', newline='').write(s)
print('modal js + css applied')
