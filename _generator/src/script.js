(()=>{
const d=document,root=d.documentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];

/* live open/closed: America/New_York, open daily 6 AM-6 PM. Google flags these dates "hours might differ". */
const HOLI={'2026-11-26':'Thanksgiving','2026-11-27':'day after Thanksgiving'};
function etNow(t=new Date()){const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(t);const o={};p.forEach(x=>o[x.type]=x.value);
 return{day:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(o.weekday),min:(+o.hour%24)*60+(+o.minute),date:`${o.year}-${o.month}-${o.day}`}}
function status(){const n=etNow();const open=n.min>=360&&n.min<1080;let t;
 if(open)t=HOLI[n.date]?'Open · '+HOLI[n.date]+', hours may vary':'Open now · until 6 PM';
 else if(n.min<360)t='Closed · opens 6 AM today';
 else t='Closed · opens 6 AM tomorrow';
 $$('[data-status]').forEach(el=>{el.classList.toggle('open',open);el.classList.toggle('closed',!open);const s=$('span',el);if(s)s.textContent=t});
 $$('.hours tr').forEach(tr=>tr.classList.toggle('today',+tr.dataset.d===n.day))}
status();setInterval(status,60000);

/* header, bead progress, mobile bar */
const hdr=$('.hdr'),prog=$('.progress'),mbar=$('.mbar');
function onScroll(){const y=scrollY,h=root.scrollHeight-innerHeight;hdr&&hdr.classList.toggle('scrolled',y>30);if(prog)prog.style.transform=`scaleX(${h>0?y/h:0})`;if(mbar)mbar.classList.toggle('show',y>260)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* mobile nav */
const bg=$('.burger'),mn=$('.mnav');
if(bg&&mn){const set=o=>{bg.setAttribute('aria-expanded',o);bg.setAttribute('aria-label',o?'Close menu':'Open menu');mn.classList.toggle('open',o);mn.setAttribute('aria-hidden',!o);mn.inert=!o;d.body.style.overflow=o?'hidden':''};
 mn.inert=true;
 bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}})}

/* split headings into characters */
$$('.split-h').forEach(h=>{if(RM)return;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(w=>{if(!w)return;if(/^\s+$/.test(w)){f.appendChild(d.createTextNode(w));return}const ws=d.createElement('span');ws.style.whiteSpace='nowrap';ws.style.display='inline-block';[...w].forEach(ch=>{const s=d.createElement('span');s.className='ch1';s.textContent=ch;ws.appendChild(s)});f.appendChild(ws)});c.replaceWith(f)}else if(c.nodeType===1&&!c.classList.contains('hot'))walk(c)})};
 h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim());walk(h);[...h.children].forEach(s=>s.setAttribute('aria-hidden','true'));$$('.ch1',h).forEach((c,i)=>c.style.transitionDelay=(i*20)+'ms')});

/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -5% 0px'});
$$('[data-r],.stagger,.split-h,.bead').forEach(el=>{if(RM)el.classList.add('in');else io.observe(el)});
$$('.stagger').forEach(g=>[...g.children].forEach((c,i)=>c.style.transitionDelay=(i*70)+'ms'));

/* spark engine (canvas, gravity, bounce, cooling colour) */
function Sparks(cv,opt){const ctx=cv.getContext('2d');let W=0,H=0,ps=[],run=false,raf,last=0;const dpr=Math.min(devicePixelRatio||1,2);
 function size(){const r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
 size();addEventListener('resize',size);
 function emit(x,y,n,pow=1){for(let i=0;i<n;i++){const a=opt.angle+(Math.random()-.5)*opt.spread,v=(opt.speed*.35+Math.random()*opt.speed)*pow;ps.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:0,max:.5+Math.random()*opt.life,b:0})}}
 function col(k){if(k<.15)return'255,250,225';if(k<.45)return'255,214,90';if(k<.75)return'255,138,45';return'210,60,20'}
 function frame(t){const dt=Math.min(.033,(t-(last||t))/1000);last=t;ctx.clearRect(0,0,W,H);ctx.globalCompositeOperation='lighter';
  if(opt.src&&run){const s=opt.src();if(s&&Math.random()<opt.rate)emit(s[0]*W,s[1]*H,1+Math.floor(Math.random()*opt.burst))}
  for(let i=ps.length-1;i>=0;i--){const p=ps[i];p.life+=dt;if(p.life>p.max){ps.splice(i,1);continue}
   const px=p.x,py=p.y;p.vy+=opt.g*dt;p.vx*=.995;p.x+=p.vx*dt;p.y+=p.vy*dt;
   if(opt.floor&&p.y>H*opt.floor&&p.vy>0&&p.b<2){p.y=H*opt.floor;p.vy*=-.32;p.vx*=.6;p.b++}
   const k=p.life/p.max;ctx.strokeStyle=`rgba(${col(k)},${1-k*k})`;ctx.lineWidth=k<.2?2.2:1.5;ctx.beginPath();ctx.moveTo(px-(p.vx*dt*1.6),py-(p.vy*dt*1.6));ctx.lineTo(p.x,p.y);ctx.stroke()}
  ctx.globalCompositeOperation='source-over';
  if(run||ps.length)raf=requestAnimationFrame(frame);else{last=0;raf=null}}
 return{emit,start(){if(run)return;run=true;if(!raf)raf=requestAnimationFrame(frame)},stop(){run=false},kick(){if(!raf)raf=requestAnimationFrame(frame)}}}

/* hero sparks from the torch tip */
const hero=$('.hero'),sc=$('.sparks');let heroSparks=null;
if(sc&&!RM){const tip=[+sc.dataset.x,+sc.dataset.y];
 heroSparks=Sparks(sc,{angle:-Math.PI/2.4,spread:2.6,speed:520,life:1.1,g:900,rate:.9,burst:3,floor:.93,src:()=>tip});
 const hio=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting?heroSparks.start():heroSparks.stop()));hio.observe(hero)}

/* arc-strike intro (home only, once per session) */
const arc=$('.arc');
function goHero(){hero&&hero.classList.add('go')}
if(arc){let seen=false;try{seen=sessionStorage.getItem('aww-arc')==='1';sessionStorage.setItem('aww-arc','1')}catch(e){}
 if(RM||seen){arc.classList.add('gone');goHero()}
 else{const cv=$('canvas',arc);const s=Sparks(cv,{angle:-Math.PI/2,spread:6.2,speed:900,life:1,g:1100,rate:0,burst:0});
  const c=()=>[cv.clientWidth/2,cv.clientHeight/2];
  [140,330,520].forEach((t,i)=>setTimeout(()=>{const[x,y]=c();s.emit(x,y,i===2?140:30,i===2?1.3:.7);s.kick()},t));
  setTimeout(()=>arc.classList.add('flash'),900);setTimeout(()=>{arc.classList.add('done');goHero()},1000);setTimeout(()=>arc.classList.add('gone'),1800)}}
else goHero();

/* parallax */
const px=$$('[data-px]');
if(!RM&&px.length){const tick=()=>{px.forEach(el=>{const r=el.parentElement.getBoundingClientRect();if(r.bottom<-100||r.top>innerHeight+100)return;const f=+el.dataset.px;const c=r.top+r.height/2-innerHeight/2;el.style.transform=`translate3d(0,${(c*-f).toFixed(1)}px,0)`})};
 addEventListener('scroll',()=>requestAnimationFrame(tick),{passive:true});addEventListener('resize',tick);tick()}

/* heat gauges + counters */
function runCount(el){const end=+el.dataset.count,dec=+(el.dataset.dec||0),out=$('b',el)||el;const g=el.closest('.gauge');
 if(g){const a=$('.val',g);if(a)a.style.strokeDashoffset=+a.dataset.len*(1-(+a.dataset.frac));const n=$('.ndl',g);if(n)n.style.transform=`rotate(${n.dataset.deg}deg)`}
 if(RM){out.textContent=end.toFixed(dec);return}
 const t0=performance.now(),D=1900;(function f(t){const k=Math.min(1,(t-t0)/D),e=1-Math.pow(1-k,4);out.textContent=(end*e).toFixed(dec);if(k<1)requestAnimationFrame(f);else out.textContent=end.toFixed(dec)})(t0)}
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){runCount(e.target);cio.unobserve(e.target)}}),{threshold:.35});
$$('[data-count]').forEach(el=>cio.observe(el));

/* tilt cards + magnetic buttons */
if(FINE&&!RM)$$('.tcard,.pcard').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*9).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*9).toFixed(2)+'deg')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})});
if(FINE&&!RM)$$('.btn.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transform=`translate(${(x*.2).toFixed(1)}px,${(y*.3).toFixed(1)}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});

/* weld-seam timeline: bead draws and the torch travels down as you scroll */
$$('.tl').forEach(tl=>{const svg=$('svg.line',tl),p=$('.draw',tl),tk=$('.torch',tl),steps=$$('.step',tl);
 function upd(){const r=tl.getBoundingClientRect(),H=r.height;svg.setAttribute('viewBox',`0 0 24 ${H}`);$$('line',svg).forEach(l=>l.setAttribute('y2',l===p?l.getAttribute('y2'):H));
  const k=RM?1:Math.min(1,Math.max(0,(innerHeight*.6-r.top)/H));p.setAttribute('y2',H*k);if(tk)tk.style.top=Math.max(0,H*k-24)+'px';
  steps.forEach(s=>{const sr=s.getBoundingClientRect();s.classList.toggle('lit',RM||sr.top+20<innerHeight*.6)})}
 addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true});addEventListener('resize',upd);upd()});

/* before/after sliders */
$$('.ba').forEach(b=>{const r=$('input',b);const set=v=>{b.style.setProperty('--p',v+'%');r.setAttribute('aria-valuetext',`${Math.round(v)}% before photo shown`)};r.addEventListener('input',()=>set(+r.value));set(+r.value);
 if(!RM){const o=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){o.unobserve(b);let t0=null;const D=1400;(function f(t){t0=t0||t;const k=Math.min(1,(t-t0)/D);const v=50+Math.sin(k*Math.PI*2)*22*(1-k);if(!b.dataset.touched){set(v);r.value=v}if(k<1)requestAnimationFrame(f)})(performance.now())}}),{threshold:.5});o.observe(b);r.addEventListener('pointerdown',()=>b.dataset.touched=1)}});

/* reviews carousel */
$$('.car').forEach(c=>{const tr=$('.car-track',c),sl=$$('.slide',c),dots=$('.dots',c);let i=0,tm;
 sl.forEach((s,k)=>{const b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Show review '+(k+1));b.onclick=()=>go(k,1);dots.appendChild(b)});
 function go(k,user){i=(k+sl.length)%sl.length;tr.style.transform=`translateX(${-100*i}%)`;$$('button',dots).forEach((b,j)=>b.setAttribute('aria-current',j===i));sl.forEach((s,j)=>{s.setAttribute('aria-hidden',j!==i);s.inert=j!==i});if(user)auto()}
 function auto(){clearInterval(tm);if(!RM)tm=setInterval(()=>go(i+1),7000)}
 $('.pv',c).onclick=()=>go(i-1,1);$('.nx',c).onclick=()=>go(i+1,1);
 c.addEventListener('mouseenter',()=>clearInterval(tm));c.addEventListener('mouseleave',auto);c.addEventListener('focusin',()=>clearInterval(tm));c.addEventListener('focusout',auto);
 let sx=null;tr.addEventListener('pointerdown',e=>sx=e.clientX);addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx;sx=null;if(Math.abs(dx)>50)go(i+(dx<0?1:-1),1)});
 go(0);auto()});

/* draggable gallery + lightbox */
$$('.gal-track').forEach(t=>{let down=false,sx=0,sl=0,moved=0,v=0,lx=0,raf;
 t.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=0;sx=lx=e.clientX;sl=t.scrollLeft;t.classList.add('drag');cancelAnimationFrame(raf)});
 addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx;moved=Math.max(moved,Math.abs(dx));v=e.clientX-lx;lx=e.clientX;t.scrollLeft=sl-dx});
 addEventListener('pointerup',()=>{if(!down)return;down=false;t.classList.remove('drag');if(!RM){(function m(){v*=.92;t.scrollLeft-=v;if(Math.abs(v)>.5)raf=requestAnimationFrame(m)})()}});
 t.addEventListener('click',e=>{if(moved>6){e.preventDefault();e.stopPropagation();moved=0}},true)});
const lb=$('.lb');
if(lb){const items=$$('.gal-item'),im=$('img',lb),cap=$('p',lb),btns=$$('button',lb);let k=0,last=null;
 function show(n){k=(n+items.length)%items.length;const it=items[k],ti=$('img',it);im.src=it.dataset.full;im.alt=ti.alt;cap.textContent=ti.alt}
 items.forEach((it,n)=>it.addEventListener('click',()=>{last=it;show(n);lb.classList.add('open');lb.setAttribute('aria-hidden','false');d.body.style.overflow='hidden';$('.x1',lb).focus()}));
 const close=()=>{lb.classList.remove('open');lb.setAttribute('aria-hidden','true');d.body.style.overflow='';last&&last.focus()};
 $('.x1',lb).onclick=close;$('.pv',lb).onclick=()=>show(k-1);$('.nx',lb).onclick=()=>show(k+1);
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 let tx=null;lb.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>50)show(k+(dx<0?1:-1))});
 addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(k-1);if(e.key==='ArrowRight')show(k+1);
  if(e.key==='Tab'){const i=btns.indexOf(d.activeElement);e.preventDefault();btns[(i+(e.shiftKey?-1:1)+btns.length)%btns.length].focus()}})}

/* embers in CTA bands */
if(!RM)$$('.embers').forEach(e=>{for(let i=0;i<22;i++){const s=d.createElement('i');s.style.left=(Math.random()*100)+'%';s.style.animationDuration=(6+Math.random()*8)+'s';s.style.animationDelay=(-Math.random()*12)+'s';s.style.setProperty('--dx',((Math.random()-.5)*160)+'px');const z=2+Math.random()*3;s.style.width=s.style.height=z+'px';e.appendChild(s)}});

/* estimate form: builds a text message (or call) to the shop, nothing is submitted anywhere */
const f=$('#estimate-form');
if(f){const msg=()=>{const v=n=>(f.elements[n]&&f.elements[n].value||'').trim();return `Estimate request from the website\nName: ${v('name')}\nPhone: ${v('phone')}\nJob: ${v('job')}\nWhere: ${v('where')}\nDetails: ${v('details')}`};
 f.addEventListener('submit',e=>{e.preventDefault();if(!f.reportValidity())return;const ios=/iP(hone|ad|od)/.test(navigator.userAgent);location.href=f.dataset.sms+(ios?'&':'?')+'body='+encodeURIComponent(msg())})}

/* demo pill */
const dm=$('.demo');if(dm){try{if(sessionStorage.getItem('aww-demo')==='x')dm.remove()}catch(e){};const x=$('button',dm);x&&x.addEventListener('click',()=>{dm.remove();try{sessionStorage.setItem('aww-demo','x')}catch(e){}})}
})();
