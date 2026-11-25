#!/usr/bin/env python3
"""Generator for the Augusta Weld Works demo site (RGWebD). Writes /workspace/augustaweldworks/site."""
import json, shutil, html, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from icons import I
from data import *
GEN=Path(__file__).parent; OUT=GEN.parent/'site'; BR=GEN.parent/'brand'
e=html.escape
# ---------- assets ----------
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name in ('.git',): continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); shutil.copytree(GEN/'assets'/'fonts',A/'fonts')
for f in ['aww-horizontal-dark.svg','aww-horizontal-light.svg','aww-stacked-dark.svg','aww-stacked-light.svg','aww-emblem-badge.svg','aww-emblem.svg','aww-logo-full.svg','aww-wordmark-white.svg','aww-wordmark-black.svg','aww-favicon.svg']: shutil.copy(BR/f,A/f)
shutil.copy(BR/'png/favicon.ico',OUT/'favicon.ico'); shutil.copy(BR/'png/favicon-180.png',OUT/'apple-touch-icon.png')
for f in ['favicon-32.png','favicon-512.png']: shutil.copy(BR/'png'/f,A/f)
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
# OG image: charcoal plate + hero photo + horizontal logo
og=Image.new('RGB',(1200,630),(10,10,11))
ph=Image.open(A/'img/g11-1600.webp').convert('RGB'); ph=ph.resize((520,round(ph.height*520/ph.width))); top=int(ph.height*0.18); ph=ph.crop((0,top,520,top+630))
m=Image.new('L',(520,630),255); ImageDraw.Draw(m).rectangle((0,0,120,630),fill=0); m=m.filter(ImageFilter.GaussianBlur(60))
og.paste(ph,(680,0),m)
d=ImageDraw.Draw(og); d.rectangle((0,614,1200,630),fill=(255,107,26))
lg=Image.open(BR/'png/horizontal-dark-1400.png').convert('RGBA'); lg=lg.resize((640,round(lg.height*640/lg.width)))
og=og.convert('RGBA'); og.alpha_composite(lg,(56,170)); og=og.convert('RGB'); d=ImageDraw.Draw(og)
try:
    fnt=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Chakra Petch/ChakraPetch-SemiBold.ttf',26)
    d.text((60,420),'MOBILE WELDING · TRAILER REPAIR · FABRICATION',font=fnt,fill=(255,201,40)); d.text((60,460),'AUGUSTA, GA · (706) 550-5298 · OPEN DAILY 6–6',font=fnt,fill=(225,225,220))
except Exception as ex: print('og font',ex)
og.save(A/'og-image.jpg',quality=86)

def dims(name,w=1600): return Image.open(A/'img'/f'{name}-{w}.webp').size
def pic(name,alt=None,cls='',sizes='(max-width:980px) 100vw, 50vw',eager=False,attrs=''):
    alt=PH[name] if alt is None else alt; w,h=dims(name); w8,_=dims(name,800)
    lazy='fetchpriority="high" ' if eager else 'loading="lazy" '
    return (f'<img src="assets/img/{name}-1600.webp" srcset="assets/img/{name}-800.webp {w8}w, assets/img/{name}-1600.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {lazy}decoding="async"{(" class=\""+cls+"\"") if cls else ""}{(" "+attrs) if attrs else ""}>')
def stars(n=5): return f'<span class="stars" aria-label="{n} out of 5 stars">'+I['star']*n+'</span>'
def btn_call(cls='',label=None): return f'<a class="btn mag {cls}" href="{TEL}">{I["phone"]}<span class="lbl">{label or "Call "+PHONE}</span></a>'
def btn_est(cls='ghost'): return f'<a class="btn mag {cls}" href="contact.html#estimate">{I["msg"]}<span class="lbl">Get an estimate</span></a>'
def btn_dir(cls='ghost'): return f'<a class="btn mag {cls}" href="{DIR}" target="_blank" rel="noopener">{I["dir"]}<span class="lbl">Directions</span></a>'
BEAD='<span class="bead" aria-hidden="true"></span>'
STATUS='<span class="status" data-status><i></i><span>Open daily 6 AM–6 PM</span></span>'
NAV=[('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('reviews.html','Reviews'),('contact.html','Contact')]
HOURS=[(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'),(0,'Sunday')]
def hours_table(): return '<table class="hours"><caption style="position:absolute;left:-9999px">Hours (Eastern Time)</caption><tbody>'+''.join(f'<tr data-d="{n}"><th scope="row">{d_}</th><td>6 AM – 6 PM</td></tr>' for n,d_ in HOURS)+'</tbody></table><p class="note">Eastern Time. Holiday hours may vary: Google flags Thanksgiving and the day after as “hours might differ,” so call ahead.</p>'
DEFS='<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><linearGradient id="heat" x1="0" x2="1"><stop offset="0" stop-color="#C93A12"/><stop offset=".55" stop-color="#FF6B1A"/><stop offset="1" stop-color="#FFE07A"/></linearGradient><linearGradient id="beadg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9a9ca1"/><stop offset=".85" stop-color="#d0d2d6"/><stop offset="1" stop-color="#FFB347"/></linearGradient></defs></svg>'

def header(cur):
    nav=''.join(f'<a href="{f}"{" aria-current=\"page\"" if f==cur else ""}>{t}</a>' for f,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="hdr"><div class="wrap"><a class="brand" href="index.html" aria-label="Augusta Weld Works home"><img src="assets/aww-horizontal-dark.svg" width="352" height="120" alt="Augusta Weld Works LLC, Mobile Welding &amp; Fabrication"></a>
<nav class="nav" aria-label="Main">{nav}</nav><div class="hdr-cta">{STATUS}<a class="btn sm mag" href="{TEL}">{I["phone"]}<span class="lbl">{PHONE}</span></a></div>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span><span></span><span></span></button></div></header>
<nav class="mnav" id="mnav" aria-label="Mobile" aria-hidden="true">{nav}<div class="ctas">{btn_call()}{btn_est()}</div><p style="margin-top:18px">{STATUS}</p></nav>'''
def footer():
    pages=''.join(f'<li><a href="{f}">{t}</a></li>' for f,t in NAV)
    sv=''.join(f'<li><a href="services.html#{s["id"]}">{s["t"]}</a></li>' for s in SERV[:6])
    return f'''<footer class="ftr"><div class="wrap"><div class="fgrid">
<div><img src="assets/aww-horizontal-dark.svg" width="300" height="102" alt="Augusta Weld Works LLC" loading="lazy" style="width:300px;height:auto;margin-bottom:18px"><p>Mobile welding and fabrication in Augusta, Georgia. Trailer repair, railings, gates, mailbox posts and custom metalwork.</p>
<address style="font-style:normal"><a href="{DIR}" target="_blank" rel="noopener">{ADDR}</a><br><a href="{TEL}">{PHONE}</a></address></div>
<div><h4>Pages</h4><ul>{pages}</ul></div><div><h4>Services</h4><ul>{sv}</ul></div><div><h4>Hours</h4><ul><li>Every day: 6 AM – 6 PM</li><li class="muted" style="font-size:.85rem">Eastern Time · holiday hours may vary</li></ul><h4 style="margin-top:22px">Find us</h4><ul><li><a href="{GLIST}" target="_blank" rel="noopener">Google Maps listing</a></li><li><a href="{DIR}" target="_blank" rel="noopener">Directions</a></li></ul></div>
</div><div class="bigword" aria-hidden="true">WELD WORKS</div><div class="legal"><span>© 2026 {NAME}. All rights reserved.</span><span>Design preview by RGWebD</span></div></div></footer>
<div class="mbar">{btn_call('', 'Call now')}{btn_est()}</div>
<div class="demo" role="note">Design preview by RGWebD<button type="button" aria-label="Dismiss preview note">×</button></div>'''
def lightbox(): return f'<div class="lb" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true"><figure><img alt=""><p></p></figure><button class="x1" type="button" aria-label="Close">{I["x"]}</button><button class="pv" type="button" aria-label="Previous photo">{I["left"]}</button><button class="nx" type="button" aria-label="Next photo">{I["arrow"]}</button></div>'

# ---------- JSON-LD ----------
def biz(extra=None):
    b={"@context":"https://schema.org","@type":"LocalBusiness","@id":BASE+"#business","name":NAME,"alternateName":SHORT,
       "description":"Mobile welding and fabrication in Augusta, Georgia: onsite welding, trailer repair (landing gear, gates, hinges, tailgates, rails, floors, spring hangers), ramps and ladder racks, ornamental railings and gates, mailbox posts, mower, bike and go-kart frame repair, and custom fabrication.",
       "url":BASE,"telephone":"+1-706-550-5298","image":[BASE+"assets/img/g11-1600.webp",BASE+"assets/img/g18b-1600.webp",BASE+"assets/og-image.jpg"],"logo":BASE+"assets/favicon-512.png",
       "address":{"@type":"PostalAddress","streetAddress":STREET,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},
       "geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LNG},"hasMap":GPLACE,"sameAs":[GPLACE],"areaServed":{"@type":"City","name":"Augusta, GA"},
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"06:00","closes":"18:00"}],
       "knowsAbout":["Mobile welding","Trailer repair","Metal fabrication","Ornamental iron railings","Mailbox posts"],
       "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":COUNT,"bestRating":5},
       "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["t"],"url":BASE+"services.html#"+s["id"]}} for s in SERV]}
    if extra: b.update(extra)
    return b
def reviews_ld(): return {"review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":5,"bestRating":5},"reviewBody":t,"publisher":{"@type":"Organization","name":"Google"}} for n,_,t in REV]}
def crumbs_ld(name,f): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":name,"item":BASE+f}]}
faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
def crumbs(name): return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span aria-current="page">{name}</span></nav>'
def phero(img,kick,h1,lead,name,pos='50% 50%'):
    return f'''<section class="phero"><div class="bg" data-px="0.12">{pic(img,sizes="100vw",eager=True,attrs=f'style="object-position:{pos}"')}</div><div class="wrap">{crumbs(name)}<p class="kicker">{kick}</p><h1 class="split-h">{h1}</h1><p class="lead">{lead}</p><div class="ctas" style="margin-top:26px">{btn_call()}{btn_est()}</div></div></section>'''
def cta(img,h,sub,pos='50% 50%'):
    return f'''<section class="cta"><div class="bg" data-px="0.1">{pic(img,alt="",sizes="100vw",attrs=f'style="object-position:{pos}"')}</div><div class="embers" aria-hidden="true"></div><div class="wrap"><p class="kicker" style="justify-content:center">Call or text the shop</p><h2 class="split-h">{h}</h2><p class="lead" style="margin:0 auto">{sub}</p><a class="big" href="{TEL}">{PHONE}</a><div class="ctas">{btn_call()}{btn_est()}</div></div></section>'''
def gauge(val,frac,lab,dec=0,suffix=''):
    R=78; L=round(2*math.pi*R*0.75,2); C=round(2*math.pi*R,2); tk=''
    for i in range(0,41):
        a=math.radians(135+270*i/40); mj=i%10==0; r1=R-14 if mj else R-9; r2=R-4
        tk+=f'<line class="{"mj" if mj else ""}" x1="{100+r1*math.cos(a):.1f}" y1="{100+r1*math.sin(a):.1f}" x2="{100+r2*math.cos(a):.1f}" y2="{100+r2*math.sin(a):.1f}"/>'
    return f'''<div class="gauge"><svg viewBox="0 0 200 170" aria-hidden="true"><circle class="trk" cx="100" cy="100" r="{R}" stroke-dasharray="{L} {C}" transform="rotate(135 100 100)"/>
<circle class="val" cx="100" cy="100" r="{R}" stroke-dasharray="{L} {C}" style="stroke-dashoffset:{L}" data-len="{L}" data-frac="{frac}" transform="rotate(135 100 100)"/>
<g class="ticks">{tk}</g><g class="ndl" data-deg="{-135+270*frac:.1f}"><line x1="100" y1="100" x2="100" y2="40"/><circle cx="100" cy="100" r="9"/></g></svg>
<div class="num" data-count="{val}" data-dec="{dec}"><b>{val:.{dec}f}</b>{f"<small>{suffix}</small>" if suffix else ""}</div><div class="lab">{lab}</div></div>'''
def ba(a,b,title,sub,start=50):
    return f'''<figure class="ba-card" data-r><div class="ba" style="--p:{start}%">{pic(b,sizes="(max-width:980px) 100vw, 50vw")}{pic(a,cls="ba-top",sizes="(max-width:980px) 100vw, 50vw")}<span class="ba-lab b" aria-hidden="true">Before</span><span class="ba-lab a" aria-hidden="true">After</span><span class="ba-seam" aria-hidden="true"></span><span class="ba-knob" aria-hidden="true">{I["left"]}{I["arrow"]}</span><input type="range" min="0" max="100" value="{start}" aria-label="Before and after slider: {e(title)}"></div><figcaption><b>{e(title)}</b><span>{e(sub)}</span></figcaption></figure>'''

def page(fname,title,desc,body,ld):
    canon=BASE+('' if fname=='index.html' else fname)
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="index,follow">
<meta name="theme-color" content="#09090A"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="assets/aww-favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SHORT}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<link rel="preload" href="assets/fonts/bigshoulders.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/barlow-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css"><script>document.documentElement.classList.add('js')</script>{lds}</head>
<body>{DEFS}{header(fname)}<main id="main">{body}</main>{footer()}{lightbox() if 'gal-item' in body else ''}<script src="assets/script.js" defer></script></body></html>'''

# ---------- HOME ----------
tick=''.join(f'<li>{s["t"]}</li>' for s in SERV)
tags=''.join(f'<a class="tcard" href="services.html#{s["id"]}"><i class="rv a"></i><i class="rv b"></i><span class="no">{k+1:02d} / {len(SERV):02d}</span><span class="ic">{I[s["ic"]]}</span><h3>{s["t"]}</h3><p>{s["s"]}</p><span class="arrow">{I["arrow"]}</span></a>' for k,s in enumerate(SERV))
HR=[(REV[1][0],REV[1][2]),(REV[3][0],"After speaking with Brock over the phone, he came out the next day and took care of my trailer! He did a fantastic job, price was very reasonable and he was very professional!"),
    (REV[9][0],REV[9][2]),(REV[4][0],"Augusta Weld Works will be my first call next time I need anything welded. Also worth noting he does do mobile service which is a plus."),
    (REV[0][0],"He does excellent work, is very responsive in communication, and will always attempt to offer same-day service.")]
def carousel(items):
    sl=''.join(f'<div class="slide" role="group" aria-roledescription="slide" aria-label="{k+1} of {len(items)}">{stars()}<blockquote>“{e(t)}”</blockquote><p class="who"><span>{e(n)}</span> · Google review</p></div>' for k,(n,t) in enumerate(items))
    return f'<div class="car" aria-roledescription="carousel" aria-label="Customer reviews"><div class="car-view"><div class="car-track">{sl}</div></div><button class="pv" type="button" aria-label="Previous review">{I["left"]}</button><button class="nx" type="button" aria-label="Next review">{I["arrow"]}</button><div class="dots"></div></div>'
home=f'''<div class="arc" aria-hidden="true"><canvas></canvas><span class="pt"></span><p>STRIKING AN ARC</p></div>
<section class="hero" aria-labelledby="h1"><div class="bgword" aria-hidden="true">WELD</div>
<div class="hero-copy"><p class="kicker fade">Mobile welding &amp; fabrication · Augusta, GA</p>
<h1 id="h1"><span class="l"><span>Broken metal?</span></span><span class="l"><span>We bring</span></span><span class="l"><span class="hot">the welder.</span></span></h1>
<p class="lead fade">Trailers, gates, railings, mower decks, mailbox posts and custom fabrication, repaired on site or at the shop. Open 6 AM to 6 PM, seven days a week.</p>
<div class="ctas fade d2">{btn_call()}{btn_est()}</div>
<div class="trust fade d2"><a class="chip" href="{GLIST}" target="_blank" rel="noopener"><span class="st">★★★★★</span> 5.0 from 74 Google reviews</a>{STATUS}</div></div>
<div class="hero-media"><div class="ph">{pic("g11",sizes="(max-width:980px) 92vw, 520px",eager=True)}</div><canvas class="sparks" aria-hidden="true" data-x="0.536" data-y="0.449"></canvas>
<div class="tag" aria-hidden="true">{I["van"]}<div><b>Onsite service</b><span>We come to the job</span></div></div>
<div class="hs" style="left:72%;top:30%"><a href="services.html#trailer-repair"><span class="dot"></span><span class="hl">Trailer repair</span></a></div>
<div class="hs rev" style="left:18%;top:62%"><a href="services.html#mobile-welding"><span class="dot"></span><span class="hl">Mobile welding</span></a></div></div></section>
<div class="ticker" aria-hidden="true"><ul>{tick}{tick}</ul></div>
<section class="sec plate"><div class="wrap"><div class="head"><div><p class="kicker">What gets welded</p><h2 class="split-h">Fixed, built, <span class="hot">welded.</span></h2>{BEAD}</div><p>Every service here comes from the shop’s Google listing, its photos and what customers say in their reviews.</p></div>
<div class="tags stagger">{tags}</div></div></section>
<section class="sec g2"><div class="wrap feature"><div>{ba("g03a","g03b","Dump trailer rear gates","Broken and strapped shut, then repaired, aligned and latching again.",55)}</div>
<div data-r><p class="kicker">Drag the seam</p><h2 class="split-h">Before. <span class="hot">After.</span></h2>{BEAD}<p class="lead">Real jobs from the shop’s Google photos. Slide the glowing seam to see the repair.</p><a class="btn ghost mag" href="work.html"><span class="lbl">See more work</span>{I["arrow"]}</a></div></div></section>
<section class="sec plate"><div class="wrap why"><div class="why-img" data-r="left">{pic("g18b",attrs='data-px="0.06"')}<span class="stamp">Shop on wheels</span></div>
<div data-r><p class="kicker">Why Augusta calls</p><h2 class="split-h">Welds that hold. <span class="hot">Service that shows up.</span></h2>{BEAD}
<div class="pts"><div class="pt"><span class="n">01</span><div><h3>Mobile service</h3><p>Onsite service is on the Google profile. One customer’s trailer was repaired the day after he called.</p></div></div>
<div class="pt"><span class="n">02</span><div><h3>Same day when possible</h3><p>Customers describe same-day frame welds and gate repairs finished “within only a few hours.”</p></div></div>
<div class="pt"><span class="n">03</span><div><h3>Fair prices</h3><p>“Reasonably priced,” “a great price,” “fair in his pricing”: it comes up in review after review.</p></div></div>
<div class="pt"><span class="n">04</span><div><h3>Built to last</h3><p>One customer says his landing gear welds were “better than factory OEM.” Another says earlier frame welds “have held up nicely.”</p></div></div></div></div></div></section>
<section class="sec g2"><div class="wrap"><div class="gauges stagger" style="margin-bottom:clamp(44px,5vw,64px)">{gauge(5.0,1.0,"Google rating · out of 5",1,"★")}{gauge(74,0.74,"Google reviews")}{gauge(7,1.0,"Days a week · 6 AM to 6 PM")}</div><div class="head center" style="justify-content:center;text-align:center"><div><p class="kicker" style="justify-content:center">Straight from Google</p><h2 class="split-h">Five stars. <span class="hot">Every one.</span></h2>{BEAD}</div></div>
{carousel(HR)}<p style="text-align:center;margin-top:40px"><a class="btn ghost mag" href="reviews.html"><span class="lbl">Read the reviews</span>{I["arrow"]}</a></p></div></section>
<section class="sec plate"><div class="wrap"><div class="head"><div><p class="kicker">Take a look</p><h2 class="split-h">Pick a <span class="hot">page.</span></h2>{BEAD}</div></div>
<div class="teasers stagger"><a class="pcard" href="services.html">{pic("g26b",sizes="(max-width:980px) 100vw, 33vw")}<span class="tx"><span class="mono">Services</span><h3>Every service</h3><p>Trailers, railings, gates, posts, frames and more</p></span></a>
<a class="pcard" href="work.html">{pic("g19b",sizes="(max-width:980px) 100vw, 33vw")}<span class="tx"><span class="mono">Our Work</span><h3>Before &amp; after</h3><p>Repairs and builds from the shop’s photos</p></span></a>
<a class="pcard" href="contact.html">{pic("g18a",sizes="(max-width:980px) 100vw, 33vw")}<span class="tx"><span class="mono">Contact</span><h3>Get an estimate</h3><p>{ADDR}</p></span></a></div></div></section>
{cta("g06","Got something <span class='hot'>broken?</span>","Open every day, 6 AM to 6 PM. Call, describe the job, and get it on the schedule.")}'''

# ---------- SERVICES ----------
def svc(s,k):
    q=f'<blockquote class="q">“{e(s["q"][0])}”<cite>{e(s["q"][1])}</cite></blockquote>' if s['q'] else ''
    li=''.join(f'<li>{e(x)}</li>' for x in s['li'])
    return f'''<article class="svc" id="{s["id"]}"><div class="svc-img" data-r="zoom">{pic(s["img"],attrs=f'style="object-position:{s.get("pos","50% 50%")}"')}<span class="bay">{k+1:02d} / {len(SERV):02d}</span></div>
<div data-r><p class="kicker">{e(s["s"])}</p><h2 class="split-h">{e(s["t"])}</h2>{BEAD}<p class="lead">{e(s["p"])}</p><ul>{li}</ul>{q}<div class="ctas" style="margin-top:22px">{btn_call("sm")}</div></div></article>'''
jump=''.join(f'<a href="#{s["id"]}">{s["t"]}</a>' for s in SERV)
STEPS=[('Step 01','Call and describe it',f'Call {PHONE} and tell the shop what broke, or send the details through the estimate form.'),
       ('Step 02','Get an estimate','Online estimates are listed on the Google profile. Customers describe the pricing as fair and reasonable.'),
       ('Step 03','Onsite or drop-off','The welder can come to you, or you can bring the trailer or equipment by. Open every day, 6 AM to 6 PM.'),
       ('Step 04','Welded right','Customers say the work gets done in a timely, professional way, and one was even shown how the original weld should have been done.'),
       ('Step 05','Back to work','Same-day turnarounds happen often, according to reviews. Then your trailer, gate or mower is back in service.')]
tl=''.join(f'<div class="step"><span class="k">{a}</span><h3>{b}</h3><p>{c}</p></div>' for a,b,c in STEPS)
services=f'''{phero("g05","Services","Mobile welding <span class='hot'>&amp; fabrication.</span>","Nine kinds of work, from trailer landing gear and hinges to iron railings, mailbox posts, mower decks and custom builds.","Services","50% 40%")}
<section class="sec tight plate"><div class="wrap"><p class="kicker">Jump to a service</p><div class="jump">{jump}</div>
{''.join(svc(s,k) for k,s in enumerate(SERV))}</div></section>
<section class="sec g2"><div class="wrap"><div class="head" style="max-width:820px;margin-inline:auto"><div><p class="kicker">How it works</p><h2 class="split-h">From the call to <span class="hot">the last bead.</span></h2>{BEAD}</div></div>
<div class="tl"><svg class="line" aria-hidden="true" preserveAspectRatio="none"><line class="road" x1="12" y1="0" x2="12" y2="100"/><line class="draw" x1="12" y1="0" x2="12" y2="0"/></svg><span class="torch" aria-hidden="true">{I["torch"]}</span>{tl}</div></div></section>
{cta("g07","Not sure it can be <span class='hot'>welded?</span>","Call and describe it. Customers say the shop is great for any type of welding work.")}'''

# ---------- WORK ----------
BAS=[('g03a','g03b','Dump trailer rear gates','Broken gate strapped shut, then repaired and latching.'),
     ('g21a','g21b','Spring hanger rebuild','Torn-off hanger replaced with a new boxed hanger under the frame.'),
     ('g29a','g29b','Trailer floor frame','Rotted edge cut out and replaced with new steel rail and cross members.'),
     ('g28a','g28b','Iron stair railing','Damaged railing straightened and welded back into place.'),
     ('g24a','g24b','Cracked mounting boss','Cracked steel boss rebuilt with fresh welds.'),
     ('g27a','g27b','Enclosed trailer floor','Floor opened up and rebuilt with new steel cross members.'),
     ('g23a','g23b','Ramp door frame','Old ramp door frame out, new steel frame built for the trailer.'),
     ('g20a','g20b','Mailbox post bracket','Broken bracket replaced with a new scroll bracket.')]
bas=''.join(ba(a,b,t,s) for a,b,t,s in BAS)
GAL=['g26b','g09','g26a','g08','g06','g02a','g02b','g19b','g17a','g25b','g01a','g10','g30b','g30a','g18a','g13']
gal=''.join(f'<button class="gal-item" type="button" data-full="assets/img/{g}-1600.webp" aria-label="Open photo: {e(PH[g])}">{pic(g,sizes="(max-width:640px) 80vw, 30vw")}<span class="cap" aria-hidden="true">{e(PH[g])}</span></button>' for g in GAL)
work=f'''{phero("g04","Our Work","Real jobs. <span class='hot'>Real welds.</span>","Before-and-after repairs and finished builds, all from the shop’s own Google photos.","Our Work","50% 45%")}
<section class="sec plate"><div class="wrap"><div class="head"><div><p class="kicker">Before &amp; after · drag the seam</p><h2 class="split-h">Broke. <span class="hot">Fixed.</span></h2>{BEAD}</div><p>Slide each glowing seam to compare. Other companies’ logos on customer trailers are blurred.</p></div>
<div class="ba-grid">{bas}</div></div></section>
<section class="sec g2" style="padding-bottom:60px"><div class="wrap"><div class="head"><div><p class="kicker">Gallery · drag or swipe</p><h2 class="split-h">More from <span class="hot">the shop.</span></h2>{BEAD}</div><p>Railings, gates, ramps, mailbox posts, trailers and frames. Tap any photo to open it.</p></div></div>
<div class="gal-track" tabindex="0" aria-label="Photo gallery, scroll sideways">{gal}</div></section>
{cta("g05","Your job <span class='hot'>could be next.</span>","Open every day, 6 AM to 6 PM. Onsite service or drop-off.","50% 40%")}'''

# ---------- REVIEWS ----------
rc=''.join(f'<figure class="rcard">{stars()}<blockquote>{e(t)}</blockquote><figcaption class="who"><b>{e(n)}</b> · Google review · {a}</figcaption></figure>' for n,a,t in REV)
reviews=f'''{phero("g26b","Reviews","74 reviews. <span class='hot'>All five stars.</span>","What Augusta customers say about Augusta Weld Works on Google, quoted word for word.","Reviews","50% 60%")}
<section class="sec tight plate"><div class="wrap"><div class="rsum" data-r><div class="big" data-count="5.0" data-dec="1"><b>5.0</b><small>/5</small></div>
<div>{stars()}<p style="margin:8px 0 0;font-size:1.15rem">From <b>74 Google reviews</b>. Topics customers mention most:</p><div class="topics">{''.join(f"<span>{t}</span>" for t in TOPICS)}</div>
<p style="margin:18px 0 0"><a class="btn sm ghost mag" href="{GLIST}" target="_blank" rel="noopener"><span class="lbl">See every review on Google</span>{I["arrow"]}</a></p></div></div></div></section>
<section class="sec tight g2"><div class="wrap"><div class="head"><div><p class="kicker">In their words</p><h2 class="split-h">Ten reviews. <span class="hot">One verdict.</span></h2>{BEAD}</div><p>Reviews are shown exactly as written on Google, spelling included.</p></div><div class="rgrid">{rc}</div></div></section>
{cta("g09","Add your project <span class='hot'>to the list.</span>","Call the shop and tell them what needs welding.")}'''

# ---------- CONTACT ----------
faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in FAQ)
JOBS=['Trailer repair','Gate, hinge or tailgate','Ramps or ladder rack','Railing or gate','Mailbox post','Mower, bike or go-kart frame','Custom fabrication','Something else']
est=f'''<form class="est" id="estimate-form" data-sms="{SMS}" novalidate><label>Your name<input name="name" autocomplete="name" required></label><label>Your phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Type of job<select name="job">{''.join(f"<option>{j}</option>" for j in JOBS)}</select></label><label>Onsite or drop-off?<select name="where"><option>Come to me (onsite)</option><option>I can bring it by</option><option>Not sure yet</option></select></label>
<label class="full">What needs welding?<textarea name="details" required placeholder="What broke, how big it is, and where it is"></textarea></label>
<div class="btns"><button class="btn mag" type="submit">{I["msg"]}<span class="lbl">Text the details</span></button>{btn_call("ghost")}<small>Opens a text message to {PHONE} on your phone. Nothing is sent until you hit send.</small></div></form>'''
contact=f'''{phero("g08","Contact","Call. <span class='hot'>Text. Weld.</span>","Open every day, 6 AM to 6 PM Eastern. Onsite service around Augusta, or bring it by.","Contact","50% 55%")}
<section class="sec tight plate"><div class="wrap cgrid"><div class="map" data-r="zoom"><iframe src="{EMBED}" title="Map to Augusta Weld Works, {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<div class="panel" data-r><h2>Get in touch</h2>{STATUS}<div class="clines"><a class="cline" href="{TEL}"><span class="ic">{I["phone"]}</span><span><b>{PHONE}</b><span>Call for onsite service or an estimate</span></span></a>
<a class="cline" href="{DIR}" target="_blank" rel="noopener"><span class="ic">{I["pin"]}</span><span><b>{STREET}</b><span>{CITY}, {REGION} {ZIP} · Directions</span></span></a>
<a class="cline" href="{GLIST}" target="_blank" rel="noopener"><span class="ic">{I["star"]}</span><span><b>5.0 on Google</b><span>74 reviews · open the listing</span></span></a></div>{hours_table()}</div></div></section>
<section class="sec steelsec diamond" id="estimate" style="scroll-margin-top:70px"><div class="wrap split"><div data-r><p class="kicker">Online estimate</p><h2 class="split-h">Tell us what <span style="color:#D2540F">broke.</span></h2>{BEAD}<p class="lead">Fill this in and your phone opens a text to the shop with everything filled in. Add a photo of the damage before you send it.</p><div class="logo-plate" style="max-width:420px;margin-top:28px"><img src="assets/aww-logo-full.svg" width="1134" height="732" alt="Augusta Weld Works LLC original logo: welder in a mask with a bright torch spark" loading="lazy"></div></div>
<div data-r>{est}</div></div></section>
<section class="sec plate"><div class="wrap"><div class="head" style="max-width:900px;margin-inline:auto"><div><p class="kicker">FAQ</p><h2 class="split-h">Good <span class="hot">questions.</span></h2>{BEAD}</div></div><div class="faq">{faq}</div></div></section>'''

PAGES=[
 ('index.html','Augusta Weld Works | Mobile Welding & Fabrication in Augusta, GA','Mobile welding and fabrication in Augusta, GA: trailer repair, gates and hinges, ramps, iron railings, mailbox posts and custom work. 5.0★ from 74 Google reviews. Open daily 6–6. Call (706) 550-5298.',home,[biz()]),
 ('services.html','Services | Trailer Repair, Railings, Mailbox Posts & Mobile Welding | Augusta Weld Works','Onsite welding, trailer repair, gates, hinges and tailgates, spring hangers, ramps and ladder racks, ornamental railings and gates, mailbox posts, mower and bike frames and custom fabrication in Augusta, GA.',services,[biz(),crumbs_ld('Services','services.html')]),
 ('work.html','Our Work | Before & After Welding Repairs | Augusta Weld Works','Before-and-after welding repairs and fabrication from Augusta Weld Works in Augusta, GA: trailer gates, spring hangers, floors, railings, mailbox posts and more.',work,[biz(),crumbs_ld('Our Work','work.html')]),
 ('reviews.html','Reviews | 5.0 Stars from 74 Google Reviews | Augusta Weld Works','Read what customers say about Augusta Weld Works in Augusta, GA: 5.0 stars from 74 Google reviews, quoted word for word.',reviews,[biz(reviews_ld()),crumbs_ld('Reviews','reviews.html')]),
 ('contact.html','Contact, Hours & Estimates | Augusta Weld Works, 204 Plymouth Rd, Augusta, GA','Augusta Weld Works: 204 Plymouth Rd, Augusta, GA 30907. Call (706) 550-5298. Open every day 6 AM–6 PM. Map, hours, estimate form and FAQ.',contact,[biz(),crumbs_ld('Contact','contact.html'),faq_ld]),
]
for f,t,dsc,b,ld in PAGES: (OUT/f).write_text(page(f,t,dsc,b,ld))
nf=f'''<section class="phero" style="min-height:80vh"><div class="wrap"><p class="kicker">Error 404</p><h1>Weld <span class="hot">missed.</span></h1><p class="lead">That page isn’t here. Head back home or give the shop a call.</p><div class="ctas" style="margin-top:24px"><a class="btn mag" href="index.html"><span class="lbl">Back home</span></a>{btn_call('ghost')}</div></div></section>'''
P=f'/{REPO}/'
h404=page('404.html','Page not found | Augusta Weld Works','This page could not be found.',nf,[biz()])
for a in ['href="index.html','href="services.html','href="work.html','href="reviews.html','href="contact.html','src="assets/','href="assets/','href="favicon.ico"','href="apple-touch-icon.png"']:
    h404=h404.replace(a,a.replace('="','="'+P,1))
h404=h404.replace('content="index,follow"','content="noindex"').replace(f'<link rel="canonical" href="{BASE}404.html">','')
(OUT/'404.html').write_text(h404)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{"" if f=="index.html" else f}</loc><lastmod>2026-11-25</lastmod></url>\n' for f,*_ in PAGES)+'</urlset>\n')
llms=f'''# {NAME}

> Mobile welding and fabrication business at {ADDR}. Phone {PHONE}. Open every day, 6 AM–6 PM Eastern Time (holiday hours may vary; Thanksgiving and the day after are flagged "hours might differ" on Google). Rated {RATING} stars from {COUNT} Google reviews. Onsite services and online estimates are listed on its Google profile.

## Key facts
- Category: Welder (mobile welding & fabrication)
- Services: {"; ".join(s["t"] for s in SERV)}
- Typical jobs from reviews: trailer landing gear, gooseneck ramp side rails, enclosed trailer repairs, utility trailer tailgates and gate hinges, ladder racks, mower deck cracks, motorcycle frame welds, a cast iron bench support bar
- Service options: onsite services; online estimates; no online booking (call {PHONE})
- Website, social links and prices: none listed on the Google profile
- Google Maps: {GPLACE}

## Pages
- [Home]({BASE}): overview, services, a before-and-after repair, why customers call, reviews
- [Services]({BASE}services.html): each service in detail and how a job works
- [Our Work]({BASE}work.html): before-and-after repairs and a photo gallery
- [Reviews]({BASE}reviews.html): {RATING}★ from {COUNT} Google reviews, ten quoted verbatim
- [Contact]({BASE}contact.html): map, hours, phone, estimate form and FAQ
'''
(OUT/'llms.txt').write_text(llms)
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text(f'# {NAME} — website design preview\n\nStatic site generated by `_generator/build.py` (RGWebD). Live: {BASE}\n')
g=OUT/'_generator'; g.mkdir(exist_ok=True)
for f in ['build.py','data.py','icons.py','qa.py']: shutil.copy(GEN/f,g/f)
shutil.copytree(GEN/'src',g/'src')
print('built',[p[0] for p in PAGES])
