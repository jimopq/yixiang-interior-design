# -*- coding: utf-8 -*-
"""易向室內設計 — 靜態頁產生器。共用頁首／頁尾，避免手動複製造成不一致。"""
import io, os

NAV = [("index.html","Home","首頁"),("about.html","About","關於易向"),
       ("works.html","Works","作品總覽"),("service.html","Service","服務流程"),
       ("contact.html","Contact","聯絡我們")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600'
 '&family=Noto+Sans+TC:wght@200;300;400;500&family=Noto+Serif+TC:wght@200;300;400;500;600&display=swap" rel="stylesheet">')

def head(cur, title, desc, og="assets/hero/h05.jpg"):
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<link rel="icon" href="assets/brand/logo-purple.png">
{FONTS}
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

<header class="site-head">
  <a class="brand" href="index.html" aria-label="易向室內設計 首頁">
    <img class="l-white" src="assets/brand/logo-white.png" alt="易向室內設計">
    <img class="l-ink" src="assets/brand/logo-ink.png" alt="易向室內設計">
  </a>
  <nav class="nav">
''' + "\n".join(
 '    <a href="%s"%s><span class="en">%s</span><span class="ch">%s</span></a>'
 % (h, ' class="on"' if h==cur else '', e, c)
 for h,e,c in NAV) + '''
  </nav>
  <a class="head-cta" href="contact.html">免費諮詢丈量</a>
  <button class="burger" aria-label="選單"><i></i><i></i><i></i></button>
</header>
'''

def page_head(img, eyebrow, h1, crumb):
    return f'''
<section class="page-head" style="background-image:url({img})">
  <div class="wrap">
    <p class="eyebrow rv in">{eyebrow}</p>
    <h1 class="rv in rv-d1">{h1}</h1>
    <p class="crumb rv in rv-d2"><a href="index.html">首頁</a> ／ {crumb}</p>
  </div>
</section>
'''

FOOT = '''
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div>
        <img class="logo" src="assets/brand/logo-white.png" alt="易向室內設計">
        <p>讓家成為情感與心靈的寄託。<br>台北・桃園雙據點，深耕室內設計二十餘年。</p>
      </div>
      <div>
        <p class="foot-h">Sitemap</p>
        <ul class="foot-list">
          <li><a href="about.html">關於易向</a></li>
          <li><a href="works.html">作品總覽</a></li>
          <li><a href="service.html">服務與收費</a></li>
          <li><a href="contact.html">聯絡我們</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Contact</p>
        <ul class="foot-list">
          <li><a href="tel:0225955532">台北 02-2595-5532</a></li>
          <li><a href="tel:0333585835">桃園 03-358-5835</a></li>
          <li><a href="mailto:image238@hotmail.com">image238@hotmail.com</a></li>
          <li><a href="https://www.facebook.com/profile.php?id=100075962749629" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© 2026 易向室內設計 YIXIANG INTERIOR DESIGN</span>
      <span>台北市南京東路二段137號14樓 ・ 桃園市桃園區經國路719號1樓</span>
    </div>
  </div>
</footer>

<div class="dock">
  <a href="tel:0333585835" aria-label="撥打電話">撥打電話</a>
  <a href="mailto:image238@hotmail.com" aria-label="來信諮詢">來信諮詢</a>
</div>

<div class="lb" id="lb">
  <button class="lb-x" id="lbX" aria-label="關閉"></button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="上一件"></button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" id="lbNext" aria-label="下一件"></button>
  <div class="lb-cap"><p class="k" id="lbK"></p><h3 id="lbT"></h3></div>
</div>

<script src="assets/js/config.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

def write(name, body):
    open(name,'w',encoding='utf-8').write(body)
    print('  ✓', name, len(body), 'bytes')

# ---------------------------------------------------------------- 作品總覽
write('works.html',
  head('works.html','作品總覽｜易向室內設計 YIXIANG INTERIOR DESIGN',
       '易向室內設計作品總覽，收錄奢華新古典風、自然人文禪風、現代素雅休閒風、小坪數溫馨宅與公共空間共 86 件完工實績。',
       'assets/hero/h09.jpg')
  + page_head('assets/hero/h09.jpg','Works','作品總覽','作品總覽')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Portfolio</p>
      <h2 class="h-sec rv rv-d1">完工實績 <span class="thin">共 <span id="wcount">86</span> 件</span></h2>
      <p class="lede rv rv-d2" style="text-align:center">點選任一件作品可放大檢視。使用左右方向鍵可連續瀏覽。</p>
    </div>
    <div class="filters" id="filters"></div>
    <div class="grid" id="allworks"></div>
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap-n" style="text-align:center">
    <p class="eyebrow center rv">Next Step</p>
    <h2 class="h-sec rv rv-d1">看到喜歡的空間了嗎</h2>
    <p class="lede rv rv-d2" style="text-align:center;margin-inline:auto">
      告訴我們您的坪數、格局與生活習慣，我們會安排免費的現場丈量與初步討論。
    </p>
    <div class="btn-row center rv rv-d3">
      <a class="btn btn-light" href="contact.html"><span>預約免費丈量</span><span>→</span></a>
    </div>
  </div>
</section>
''' + FOOT)

# ---------------------------------------------------------------- 關於易向
VIDS = [("E9b6lGOiFKQ","【空間設計秘訣開箱】輕工業風格居家設計"),
        ("WYuW_FUWt28","【空間設計秘訣開箱】莫蘭迪色低調奢華設計專訪"),
        ("QFgFmfa30vI","【空間設計秘訣開箱】四個年輕人一定要做的設計"),
        ("AegVGxrSr7k","【直擊設計師的家】收納秘訣大公開・玄關客廳書房篇")]
vid_html = "\n".join(
 f'''      <article class="vid rv{f" rv-d{n%3}" if n%3 else ""}">
        <div class="vid-fr"><iframe src="https://www.youtube.com/embed/{vid}" title="{t}"
          loading="lazy" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"
          allowfullscreen></iframe></div>
        <h3>{t}</h3>
      </article>''' for n,(vid,t) in enumerate(VIDS))

write('about.html',
  head('about.html','關於易向｜易向室內設計 YIXIANG INTERIOR DESIGN',
       '易向室內設計深耕二十餘年，榮獲美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎、義大利 A′ Design Award 銀獎。',
       'assets/hero/h11.jpg')
  + page_head('assets/hero/h11.jpg','About Us','關於易向','關於易向')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="philo">
      <div class="philo-fig rv"><img src="assets/hero/h31.jpg" alt="易向室內設計 作品實景" loading="lazy"></div>
      <div class="philo-body">
        <p class="eyebrow rv">Philosophy</p>
        <h2 class="h-sec rv rv-d1">設計理念</h2>
        <p class="philo-q rv rv-d2">室內設計的真諦不在譁眾取寵，而是來自於居住者<em>發自內心的認同與肯定</em>。</p>
        <div class="rv rv-d3" style="margin-top:32px">
          <p>從事室內設計二十多個年頭，如何讓家成為情感與心靈的寄託，一直是整個設計團隊所秉持的原則。</p>
          <p>以無限的巧思及創新讓家的收納與美感合而為一，從細膩動人的設計觀點及高品質的施工，重新定義家人的互動。</p>
          <p>注重完美的線條比例，更在乎客戶的生活體驗與需求。我們不會強迫您的感官定義，更不會堅持學院派的理論。</p>
        </div>
      </div>
    </div>
    <div class="stats rv">
      <div><p class="n">20<small>餘年</small></p><p class="k">專業經驗</p></div>
      <div><p class="n">86<small>件</small></p><p class="k">完工實績</p></div>
      <div><p class="n">03<small>項</small></p><p class="k">國際設計獎</p></div>
      <div><p class="n">02<small>處</small></p><p class="k">台北・桃園據點</p></div>
    </div>
  </div>
</section>

<section class="sec sec-dark" id="awards">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Awards</p>
      <h2 class="h-sec rv rv-d1">國際設計獎項</h2>
    </div>
    <div class="awards">
      <article class="award rv"><p class="yr">2019</p><h3>美國 MUSE Design Awards</h3>
        <p class="lv">Gold Winner 金獎</p>
        <p>全球具指標性的國際設計獎項，表彰建築、室內、產品與品牌設計領域之創新與卓越表現。</p></article>
      <article class="award rv rv-d1"><p class="yr">2020</p><h3>法國 Novum Design Award</h3>
        <p class="lv">Gold Winner 金獎</p>
        <p>評選涵蓋設計品質、創新性、原創性、技術性與執行力五項標準，金獎為最高等級。</p></article>
      <article class="award rv rv-d2"><p class="yr">2020</p><h3>義大利 A′ Design Award</h3>
        <p class="lv">Silver Winner 銀獎</p>
        <p>歐洲歷史最悠久、規模最大的國際設計競賽之一，為全球設計品質的重要指標。</p></article>
    </div>
    <div class="badges rv rv-d2">
      <img src="assets/brand/award_muse.png" alt="MUSE Design Awards Gold Winner">
      <img src="assets/brand/award_novum.png" alt="Novum Design Award Gold Winner">
    </div>
  </div>
</section>

<section class="sec sec-alt" id="press">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Press &amp; Video</p>
      <h2 class="h-sec rv rv-d1">媒體專訪與影片</h2>
      <p class="lede rv rv-d2" style="text-align:center">幸福空間雜誌報導・設計師親自開箱的空間設計秘訣。</p>
    </div>
    <div class="vids">
''' + vid_html + '''
    </div>
  </div>
</section>
''' + FOOT)

# ---------------------------------------------------------------- 服務與流程
write('service.html',
  head('service.html','服務與收費標準｜易向室內設計 YIXIANG INTERIOR DESIGN',
       '易向室內設計服務項目涵蓋住宅空間、商業空間、建築公共空間、接待中心實品屋與舊屋翻新，並提供免費諮詢與丈量服務。',
       'assets/hero/h15.jpg')
  + page_head('assets/hero/h15.jpg','Service','服務與流程','服務與流程')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow rv">Service</p>
      <h2 class="h-sec rv rv-d1">服務項目</h2>
      <p class="lede rv rv-d2">從住宅到商業空間，從新成屋到舊屋翻新，易向提供完整的設計與工程一條龍服務。</p>
    </div>
    <div class="svc">
      <article class="svc-i rv"><p class="no">01</p><h3>住宅空間</h3><p>依生活動線與收納需求量身規劃，兼顧美感與日常實用。</p></article>
      <article class="svc-i rv rv-d1"><p class="no">02</p><h3>商業空間</h3><p>以品牌調性為核心，打造具識別度且符合營運效率的場域。</p></article>
      <article class="svc-i rv rv-d2"><p class="no">03</p><h3>建築公共空間</h3><p>大廳、交誼廳與公設整體規劃，提升建案整體質感與價值。</p></article>
      <article class="svc-i rv"><p class="no">04</p><h3>接待中心・實品屋</h3><p>掌握銷售節奏與客層想像，以空間敘事創造成交動能。</p></article>
      <article class="svc-i rv rv-d1"><p class="no">05</p><h3>舊屋翻新</h3><p>從管線結構到格局重整，讓老屋重新符合現代生活需求。</p></article>
      <article class="svc-i rv rv-d2"><p class="no">06</p><h3>免費諮詢與丈量</h3><p>初次接觸不收費，先聊需求、看現場，再談設計與預算。</p></article>
    </div>
  </div>
</section>

<section class="sec sec-alt" id="fee">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow rv">Charges</p>
      <h2 class="h-sec rv rv-d1">收費標準</h2>
      <p class="lede rv rv-d2">收費透明，簽約前完整說明。以下為一般情況的計價方式，實際金額依現場條件與設計內容調整。</p>
    </div>
    <div class="fees">
      <article class="fee rv"><p class="no">01</p><h3>設計合約</h3>
        <p class="amt">6,000 – 8,000<small>元 / 坪</small></p>
        <ul><li>住宅依室內面積計價</li><li>依實際施作面積及風格差異不同計算</li><li>商業空間、辦公室需視個案而定</li></ul></article>
      <article class="fee rv rv-d1"><p class="no">02</p><h3>工程合約</h3>
        <p class="amt">個案報價</p>
        <ul><li>依高質感的施工品質</li><li>再依據坪數大小、風格規劃</li><li>施工項目及立面材質的差異</li><li>完整提報工程總預算</li></ul></article>
      <article class="fee rv rv-d2"><p class="no">03</p><h3>諮詢與丈量</h3>
        <p class="amt">免費</p>
        <ul><li>初步需求溝通不收費</li><li>現場丈量與拍照留底不收費</li><li>提供初步專業建議與預算方向</li></ul></article>
    </div>
    <p class="note rv">※ 以上為易向室內設計之計價原則，實際金額以雙方簽訂之設計合約與工程合約為準。</p>
  </div>
</section>

<section class="sec" id="process">
  <div class="wrap-n">
    <div class="sec-head center">
      <p class="eyebrow center rv">Design Flow</p>
      <h2 class="h-sec rv rv-d1">設計流程</h2>
      <p class="lede rv rv-d2" style="text-align:center">六個階段，每一步都留下可以確認的紀錄。</p>
    </div>
    <div class="flow">
      <article class="flow-i rv"><p class="idx">01</p><div><h3>初步溝通</h3><p class="en">Consultation</p>
        <ul><li>瞭解目前房屋狀況及基本生活需求</li><li>討論業主起居習慣、特殊喜好收藏</li><li>提出初步專業建議及工程預算溝通</li><li>風格初步討論</li></ul></div></article>
      <article class="flow-i rv"><p class="idx">02</p><div><h3>現場丈量</h3><p class="en">Site Measurement</p>
        <ul><li>對工程現場進行丈量，並拍照留底</li><li>了解工地現場並初步告知注意事項</li><li>資料蒐集完整後進行平面繪製</li></ul></div></article>
      <article class="flow-i rv"><p class="idx">03</p><div><h3>圖面繪製</h3><p class="en">Drafting</p>
        <ul><li>繪製平面規劃配置圖</li><li>討論平面配置並簽訂設計合約</li></ul></div></article>
      <article class="flow-i rv"><p class="idx">04</p><div><h3>立面及建材討論</h3><p class="en">Materials</p>
        <ul><li>解說立面設計圖設計理念</li><li>提供設計材質的相關樣板及性質討論</li><li>提供工程報價單，並解說內容</li><li>簽訂工程合約</li></ul></div></article>
      <article class="flow-i rv"><p class="idx">05</p><div><h3>進場施工</h3><p class="en">Construction</p>
        <ul><li>現場立面圖放樣，再次確認細節後簽認放樣驗收單</li><li>排定工程進度表進行施工</li><li>施工期間不定期與業主現場溝通</li><li>以嚴謹的態度控管施工品質</li></ul></div></article>
      <article class="flow-i rv"><p class="idx">06</p><div><h3>完成交屋</h3><p class="en">Handover</p>
        <ul><li>相關工程完工後，確認無誤雙方簽認交屋驗收單</li><li>保固期內，非人為因素之損壞提供維修保固</li><li>保固期後若有維修皆可派工處理，酌收工料費用</li></ul></div></article>
    </div>
    <div class="btn-row center rv">
      <a class="btn btn-brand" href="contact.html"><span>預約免費諮詢</span><span>→</span></a>
    </div>
  </div>
</section>
''' + FOOT)

# ---------------------------------------------------------------- 聯絡我們
write('contact.html',
  head('contact.html','聯絡我們｜易向室內設計 YIXIANG INTERIOR DESIGN',
       '易向室內設計台北公司：台北市南京東路二段137號14樓 02-2595-5532；桃園公司：桃園市桃園區經國路719號1樓 03-358-5835。免費諮詢與丈量服務。',
       'assets/hero/h17.jpg')
  + page_head('assets/hero/h17.jpg','Contact','聯絡我們','聯絡我們')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Our Offices</p>
      <h2 class="h-sec rv rv-d1">台北 ・ 桃園 雙據點</h2>
      <p class="lede rv rv-d2" style="text-align:center">初次諮詢與現場丈量皆不收費，歡迎先來電或留下資料。</p>
    </div>
    <div class="offices rv">
      <div class="office">
        <p class="k">Taipei Office</p>
        <h3>台北公司</h3>
        <dl>
          <dt>地址</dt><dd>台北市南京東路二段 137 號 14 樓</dd>
          <dt>電話</dt><dd><a href="tel:0225955532">02-2595-5532</a></dd>
          <dt>信箱</dt><dd><a href="mailto:image238@hotmail.com">image238@hotmail.com</a></dd>
        </dl>
      </div>
      <div class="office">
        <p class="k">Taoyuan Office</p>
        <h3>桃園公司</h3>
        <dl>
          <dt>地址</dt><dd>桃園市桃園區經國路 719 號 1 樓</dd>
          <dt>電話</dt><dd><a href="tel:0333585835">03-358-5835</a></dd>
          <dt>傳真</dt><dd>03-358-0377</dd>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap-n">
    <div class="sec-head center">
      <p class="eyebrow center rv">Enquiry</p>
      <h2 class="h-sec rv rv-d1">諮詢表單</h2>
      <p class="lede rv rv-d2" style="text-align:center">留下需求，我們會在一個工作天內與您聯繫。</p>
    </div>
    <form class="form rv" id="enquiry" novalidate>
      <div class="field"><label for="f-name">姓名 <i>*</i></label>
        <input id="f-name" name="name" required placeholder="您的稱呼"></div>
      <div class="field"><label for="f-tel">聯絡電話 <i>*</i></label>
        <input id="f-tel" name="tel" type="tel" required placeholder="09xx-xxx-xxx"></div>
      <div class="field"><label for="f-mail">Email</label>
        <input id="f-mail" name="email" type="email" placeholder="you@example.com"></div>
      <div class="field"><label for="f-type">需求類型</label>
        <select id="f-type" name="type">
          <option>住宅空間設計</option><option>商業空間設計</option>
          <option>建築公共空間</option><option>接待中心・實品屋</option>
          <option>舊屋翻新</option><option>其他</option>
        </select></div>
      <div class="field"><label for="f-area">坪數</label>
        <input id="f-area" name="area" placeholder="例：35 坪"></div>
      <div class="field"><label for="f-city">房屋所在地</label>
        <input id="f-city" name="city" placeholder="例：桃園市桃園區"></div>
      <div class="field full"><label for="f-msg">需求說明</label>
        <textarea id="f-msg" name="message" placeholder="格局現況、居住成員、風格偏好、預算範圍…"></textarea></div>
      <div class="hp" aria-hidden="true">
        <label for="f-co">公司（請勿填寫）</label>
        <input id="f-co" name="company" tabindex="-1" autocomplete="off">
      </div>
      <div class="field full">
        <button class="btn btn-brand" type="submit" style="justify-content:center"><span>送出諮詢</span></button>
        <p class="note" id="formHint" style="margin-top:14px">
          ※ 送出即表示同意易向室內設計以您留下的聯絡方式與您聯繫。
        </p>
      </div>
    </form>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="maps rv">
      <iframe title="台北公司地圖" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=台北市南京東路二段137號&output=embed"></iframe>
      <iframe title="桃園公司地圖" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=桃園市桃園區經國路719號&output=embed"></iframe>
    </div>
  </div>
</section>
''' + FOOT)

print('done.')
