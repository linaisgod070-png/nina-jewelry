#!/usr/bin/env python3
"""Generate NinaJewelryUSA static site from product data."""
import json, html, os

with open('/tmp/szwego_products.json') as f:
    products = json.load(f)

# Categorize
categories = {
    'Pendants': [p for p in products if 'Pendants' in p.get('tags', [])],
    'ChanelNecklace': [p for p in products if 'ChanelNecklace' in p.get('tags', [])],
    'Scrunchie': [p for p in products if 'Scrunchie' in p.get('tags', [])],
}

WHATSAPP = "https://wa.me/8613928692115"
PHONE = "+8613928692115"

def esc(s):
    return html.escape(s, quote=True)

def product_card(p):
    thumbs = p.get('thumb_images', [])
    originals = p.get('images', [])
    title = esc(p.get('title', 'Product'))
    gid = esc(p.get('goods_id', ''))
    if not thumbs:
        return ''
    
    dots = ''
    slides = ''
    for i, (thumb, orig) in enumerate(zip(thumbs, originals)):
        active = ' active' if i == 0 else ''
        slides += f'<div class="slide{active}"><img src="{esc(thumb)}" data-full="{esc(orig)}" alt="{title}" loading="lazy" onclick="openLightbox(this)"></div>\n'
        dot_active = ' active' if i == 0 else ''
        dots += f'<span class="dot{dot_active}" onclick="goSlide(this,{i})"></span>'
    
    nav = ''
    if len(thumbs) > 1:
        nav = f'''<button class="slide-btn prev" onclick="changeSlide(this,-1)">&#10094;</button>
<button class="slide-btn next" onclick="changeSlide(this,1)">&#10095;</button>
<div class="dots">{dots}</div>'''
    
    return f'''<div class="product-card" data-id="{gid}">
<div class="slider">{slides}{nav}</div>
<div class="product-info">
<h3 class="product-title">{title}</h3>
<a href="{WHATSAPP}?text=Hi!%20I%27m%20interested%20in%20{gid}" class="wa-btn" target="_blank" rel="noopener">
<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.943 11.943 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.387 0-4.594-.822-6.34-2.2l-.442-.362-3.262 1.093 1.093-3.262-.362-.442A9.956 9.956 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
Order via WhatsApp</a>
</div>
</div>'''

def featured_products():
    """Pick 8 featured products, mix from all categories."""
    featured = []
    for cat in ['Pendants', 'ChanelNecklace', 'Scrunchie']:
        items = categories[cat]
        featured.extend(items[:3])
    return featured[:9]

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
:root{--primary:#1a1a2e;--accent:#e94560;--gold:#c9a96e;--bg:#fafafa;--card:#fff;--text:#333;--text-light:#777;--radius:12px;--shadow:0 2px 20px rgba(0,0,0,.08)}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{text-decoration:none;color:inherit}
/* NAV */
.navbar{background:var(--primary);padding:0 2rem;position:sticky;top:0;z-index:100;box-shadow:0 2px 10px rgba(0,0,0,.15)}
.nav-inner{max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:1.5rem;font-weight:700;color:#fff;letter-spacing:1px}
.logo span{color:var(--gold)}
.nav-links{display:flex;gap:2rem;list-style:none}
.nav-links a{color:rgba(255,255,255,.85);font-size:.95rem;font-weight:500;transition:color .2s;padding:.5rem 0;position:relative}
.nav-links a:hover,.nav-links a.active{color:var(--gold)}
.nav-links a.active::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--gold)}
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px}
.hamburger span{width:24px;height:2px;background:#fff;transition:.3s}
/* HERO */
.hero{background:linear-gradient(135deg,var(--primary) 0%,#16213e 50%,#0f3460 100%);padding:5rem 2rem;text-align:center;color:#fff;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(201,169,110,.1) 0%,transparent 50%);animation:shimmer 8s ease-in-out infinite}
@keyframes shimmer{0%,100%{transform:translate(0,0)}50%{transform:translate(5%,5%)}}
.hero h1{font-size:3rem;font-weight:700;margin-bottom:1rem;position:relative}
.hero h1 span{color:var(--gold)}
.hero p{font-size:1.2rem;opacity:.85;max-width:600px;margin:0 auto 2rem;position:relative}
.hero-cats{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;position:relative}
.hero-cat{background:rgba(255,255,255,.1);border:1px solid rgba(201,169,110,.3);padding:.75rem 2rem;border-radius:50px;color:#fff;font-weight:500;transition:all .3s;backdrop-filter:blur(10px)}
.hero-cat:hover{background:var(--gold);color:var(--primary);border-color:var(--gold);transform:translateY(-2px)}
/* PAGE HEADER */
.page-header{background:linear-gradient(135deg,var(--primary),#16213e);padding:3rem 2rem;text-align:center;color:#fff}
.page-header h1{font-size:2.2rem;font-weight:700}
.page-header p{opacity:.8;margin-top:.5rem}
/* SECTION */
.section{max-width:1400px;margin:0 auto;padding:3rem 1.5rem}
.section-title{font-size:1.8rem;font-weight:700;text-align:center;margin-bottom:.5rem;color:var(--primary)}
.section-sub{text-align:center;color:var(--text-light);margin-bottom:2.5rem}
/* GRID */
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem}
/* CARD */
.product-card{background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);transition:transform .3s,box-shadow .3s}
.product-card:hover{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,.12)}
.slider{position:relative;aspect-ratio:1;overflow:hidden;background:#f0f0f0}
.slide{display:none;width:100%;height:100%}
.slide.active{display:block}
.slide img{width:100%;height:100%;object-fit:cover;cursor:pointer;transition:transform .3s}
.slide img:hover{transform:scale(1.05)}
.slide-btn{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.4);color:#fff;border:none;padding:8px 12px;cursor:pointer;font-size:1rem;z-index:2;border-radius:50%;transition:background .2s;backdrop-filter:blur(4px)}
.slide-btn:hover{background:rgba(0,0,0,.7)}
.prev{left:8px}.next{right:8px}
.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px;z-index:2}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.5);cursor:pointer;transition:all .2s}
.dot.active{background:#fff;transform:scale(1.2)}
.product-info{padding:1rem 1.2rem 1.2rem}
.product-title{font-size:.95rem;font-weight:600;line-height:1.4;margin-bottom:.75rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.wa-btn{display:inline-flex;align-items:center;gap:6px;background:#25d366;color:#fff;padding:.5rem 1rem;border-radius:50px;font-size:.85rem;font-weight:600;transition:all .2s}
.wa-btn:hover{background:#1da851;transform:translateY(-1px)}
.wa-btn svg{flex-shrink:0}
/* LIGHTBOX */
.lightbox{display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:1000;justify-content:center;align-items:center;padding:2rem}
.lightbox.open{display:flex}
.lightbox img{max-width:90vw;max-height:85vh;object-fit:contain;border-radius:8px;animation:lbIn .3s ease}
@keyframes lbIn{from{opacity:0;transform:scale(.9)}to{opacity:1;transform:scale(1)}}
.lightbox .lb-close{position:absolute;top:1.5rem;right:1.5rem;color:#fff;font-size:2rem;cursor:pointer;width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.1);border-radius:50%;border:none;transition:background .2s}
.lightbox .lb-close:hover{background:rgba(255,255,255,.25)}
.lightbox .lb-nav{position:absolute;top:50%;transform:translateY(-50%);color:#fff;font-size:2rem;cursor:pointer;background:rgba(255,255,255,.1);border:none;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;transition:background .2s}
.lightbox .lb-nav:hover{background:rgba(255,255,255,.25)}
.lightbox .lb-prev{left:1.5rem}
.lightbox .lb-next{right:1.5rem}
/* FOOTER */
.footer{background:var(--primary);color:rgba(255,255,255,.8);padding:3rem 2rem;margin-top:3rem}
.footer-inner{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:2rem}
.footer h3{color:var(--gold);margin-bottom:1rem;font-size:1.1rem}
.footer p,.footer a{font-size:.9rem;line-height:1.8}
.footer a{color:rgba(255,255,255,.8);transition:color .2s}
.footer a:hover{color:var(--gold)}
.footer-bottom{text-align:center;padding-top:2rem;margin-top:2rem;border-top:1px solid rgba(255,255,255,.1);font-size:.85rem;opacity:.6}
.wa-float{position:fixed;bottom:2rem;right:2rem;background:#25d366;color:#fff;width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(37,211,102,.4);z-index:99;transition:transform .3s}
.wa-float:hover{transform:scale(1.1)}
.wa-float svg{width:28px;height:28px}
/* RESPONSIVE */
@media(max-width:768px){
.nav-links{display:none;position:absolute;top:64px;left:0;right:0;background:var(--primary);flex-direction:column;padding:1rem 2rem;gap:0;box-shadow:0 4px 10px rgba(0,0,0,.2)}
.nav-links.open{display:flex}
.nav-links a{padding:.75rem 0;border-bottom:1px solid rgba(255,255,255,.1)}
.hamburger{display:flex}
.hero h1{font-size:2rem}
.hero p{font-size:1rem}
.product-grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1rem}
.product-info{padding:.75rem}
.product-title{font-size:.85rem}
.section{padding:2rem 1rem}
.lightbox .lb-nav{width:36px;height:36px;font-size:1.2rem}
}
'''

JS = '''
function changeSlide(btn,dir){
var slider=btn.closest('.slider');
var slides=slider.querySelectorAll('.slide');
var dots=slider.querySelectorAll('.dot');
var cur=[...slides].findIndex(s=>s.classList.contains('active'));
slides[cur].classList.remove('active');
if(dots[cur])dots[cur].classList.remove('active');
var next=(cur+dir+slides.length)%slides.length;
slides[next].classList.add('active');
if(dots[next])dots[next].classList.add('active');
}
function goSlide(dot,idx){
var slider=dot.closest('.slider');
var slides=slider.querySelectorAll('.slide');
var dots=slider.querySelectorAll('.dot');
slides.forEach(s=>s.classList.remove('active'));
dots.forEach(d=>d.classList.remove('active'));
slides[idx].classList.add('active');
dots[idx].classList.add('active');
}
// Lightbox
var lbImages=[];var lbIdx=0;
function openLightbox(img){
var card=img.closest('.product-card');
var imgs=card.querySelectorAll('.slide img');
lbImages=[...imgs].map(i=>i.dataset.full||i.src);
lbIdx=[...imgs].indexOf(img);
var lb=document.getElementById('lightbox');
lb.querySelector('img').src=lbImages[lbIdx];
lb.classList.add('open');
document.body.style.overflow='hidden';
}
function closeLightbox(){
document.getElementById('lightbox').classList.remove('open');
document.body.style.overflow='';
}
function lbNav(dir){
lbIdx=(lbIdx+dir+lbImages.length)%lbImages.length;
document.querySelector('#lightbox img').src=lbImages[lbIdx];
}
document.addEventListener('keydown',function(e){
if(!document.getElementById('lightbox').classList.contains('open'))return;
if(e.key==='Escape')closeLightbox();
if(e.key==='ArrowLeft')lbNav(-1);
if(e.key==='ArrowRight')lbNav(1);
});
// Mobile nav
document.addEventListener('DOMContentLoaded',function(){
var h=document.querySelector('.hamburger');
if(h)h.addEventListener('click',function(){
document.querySelector('.nav-links').classList.toggle('open');
});
});
'''

def nav_html(active=''):
    links = [
        ('index.html', 'Home'),
        ('pendants.html', 'Pendants'),
        ('necklace.html', 'Necklaces'),
        ('scrunchie.html', 'Scrunchies'),
    ]
    items = ''
    for href, label in links:
        cls = ' class="active"' if label.lower().startswith(active.lower()) else ''
        items += f'<li><a href="{href}"{cls}>{label}</a></li>'
    return f'''<nav class="navbar">
<div class="nav-inner">
<a href="index.html" class="logo">Nina<span>Jewelry</span>USA</a>
<ul class="nav-links">{items}</ul>
<div class="hamburger" aria-label="Menu"><span></span><span></span><span></span></div>
</div>
</nav>'''

FOOTER = f'''<footer class="footer">
<div class="footer-inner">
<div>
<h3>NinaJewelryUSA</h3>
<p>Premium fashion jewelry and accessories.<br>Pendants, necklaces, scrunchies and more.</p>
</div>
<div>
<h3>Shop</h3>
<p><a href="pendants.html">Pendants</a></p>
<p><a href="necklace.html">Necklaces</a></p>
<p><a href="scrunchie.html">Scrunchies</a></p>
</div>
<div>
<h3>Contact Us</h3>
<p><a href="{WHATSAPP}" target="_blank">WhatsApp: {PHONE}</a></p>
<p>Order via WhatsApp for fastest service</p>
</div>
</div>
<div class="footer-bottom">&copy; 2026 NinaJewelryUSA. All rights reserved.</div>
</footer>'''

LIGHTBOX_HTML = '''<div id="lightbox" class="lightbox" onclick="if(event.target===this)closeLightbox()">
<button class="lb-close" onclick="closeLightbox()">&times;</button>
<button class="lb-nav lb-prev" onclick="lbNav(-1)">&#10094;</button>
<img src="" alt="Product image">
<button class="lb-nav lb-next" onclick="lbNav(1)">&#10095;</button>
</div>'''

WA_FLOAT = f'''<a href="{WHATSAPP}" class="wa-float" target="_blank" rel="noopener" aria-label="Contact on WhatsApp">
<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.943 11.943 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.387 0-4.594-.822-6.34-2.2l-.442-.362-3.262 1.093 1.093-3.262-.362-.442A9.956 9.956 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
</a>'''

def page_head(title):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} - NinaJewelryUSA</title>
<style>{CSS}</style>
</head>
<body>'''

def page_foot():
    return f'''{FOOTER}
{WA_FLOAT}
{LIGHTBOX_HTML}
<script>{JS}</script>
</body>
</html>'''

# === INDEX ===
cards = ''.join(product_card(p) for p in featured_products())
index = f'''{page_head("Premium Fashion Jewelry")}
{nav_html("home")}
<section class="hero">
<h1>Nina<span>Jewelry</span>USA</h1>
<p>Premium fashion jewelry and accessories. Shop our curated collection of pendants, necklaces, and designer scrunchies.</p>
<div class="hero-cats">
<a href="pendants.html" class="hero-cat">✨ Pendants ({len(categories["Pendants"])})</a>
<a href="necklace.html" class="hero-cat">💎 Necklaces ({len(categories["ChanelNecklace"])})</a>
<a href="scrunchie.html" class="hero-cat">🎀 Scrunchies ({len(categories["Scrunchie"])})</a>
</div>
</section>
<section class="section">
<h2 class="section-title">Featured Products</h2>
<p class="section-sub">Hand-picked favorites from our collection</p>
<div class="product-grid">{cards}</div>
</section>
{page_foot()}'''

outdir = '/root/.openclaw/workspace/nina-jewelry-site'
with open(f'{outdir}/index.html', 'w') as f:
    f.write(index)
print('index.html done')

# === CATEGORY PAGES ===
cat_pages = [
    ('pendants.html', 'Pendants', 'Pendants', 'Elegant pendants for every occasion', 'pendant'),
    ('necklace.html', 'Necklaces', 'ChanelNecklace', 'Designer necklaces to elevate your style', 'necklace'),
    ('scrunchie.html', 'Scrunchies', 'Scrunchie', 'Luxury designer scrunchies', 'scrunchie'),
]

for fname, title, tag, subtitle, nav_active in cat_pages:
    items = categories[tag]
    cards = ''.join(product_card(p) for p in items)
    page = f'''{page_head(title)}
{nav_html(nav_active)}
<section class="page-header">
<h1>{title}</h1>
<p>{subtitle} &mdash; {len(items)} items</p>
</section>
<section class="section">
<div class="product-grid">{cards}</div>
</section>
{page_foot()}'''
    with open(f'{outdir}/{fname}', 'w') as f:
        f.write(page)
    print(f'{fname} done ({len(items)} products)')

print('All pages generated!')
