# -*- coding: utf-8 -*-
"""易向室內設計 — 靜態頁產生器。所有頁面共用同一份頁首／頁尾／元件。"""

import hashlib


def asset_ver(path):
    """回傳檔案內容的 8 碼 hash，接在 ?v= 後面當 cache-busting 版本號。
    檔案一變、URL 就變，不依賴任何人記得手動改版號，也不受
    GitHub Pages／Cloudflare Pages 各自的快取策略差異影響。"""
    return hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]


CSS_V = asset_ver('assets/css/style.css')
JS_V = asset_ver('assets/js/main.js')
CFG_V = asset_ver('assets/js/config.js')


NAV = [
    ("index.html",   "Home",    "首頁"),
    ("about.html",   "About",   "關於易向"),
    ("works.html",   "Works",   "作品總覽"),
    ("case.html",    "Case",    "精選案例"),
    ("service.html", "Service", "服務收費"),
    ("process.html", "Process", "設計流程"),
    ("contact.html", "Contact", "聯絡我們"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600'
 '&family=Noto+Serif+TC:wght@400&display=swap" rel="stylesheet">')

SITE = "易向室內設計 YIXIANG INTERIOR DESIGN"



def bg_css(spec):
    """spec = (selector, 檔名)。相對路徑寫在 HTML 的 <style> 裡，
    才會以文件為基準解析；寫在 assets/css/style.css 的 var() 會變成
    相對於 CSS 檔（/assets/css/...），這是 CSS 自訂屬性的已知陷阱。"""
    sel, f = spec
    return ('<style>%s{background-image:url(assets/hero/1600/%s)}'
            '@media(max-width:720px){%s{background-image:url(assets/hero/900/%s)}}</style>'
            % (sel, f, sel, f))


def head(cur, title, desc, og="assets/hero/1600/h05.jpg", preload=None, bg=None):
    css = bg_css(bg) if bg else ''
    if preload:
        sm = preload.replace('/1600/', '/900/')
        pl = ('<link rel="preload" as="image" href="%s" media="(min-width:721px)" fetchpriority="high">'
              '<link rel="preload" as="image" href="%s" media="(max-width:720px)" fetchpriority="high">'
              % (preload, sm))
    else:
        pl = ''
    nav = "\n".join(
        '    <a href="%s"%s><span class="en">%s</span><span class="ch">%s</span></a>'
        % (h, ' class="on"' if h == cur else '', e, c)
        for h, e, c in NAV)
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
{pl}
<link rel="stylesheet" href="assets/css/style.css?v={CSS_V}">
{css}
</head>
<body>

<header class="site-head">
  <a class="brand" href="index.html" aria-label="易向室內設計 首頁">
    <img class="l-white" src="assets/brand/logo-white.png" alt="易向室內設計" width="520" height="125">
    <img class="l-ink" src="assets/brand/logo-ink.png" alt="易向室內設計" width="520" height="125">
  </a>
  <nav class="nav">
{nav}
  </nav>
  <a class="head-cta line-cta" data-line href="#" target="_blank" rel="noopener">
    <span class="ico" aria-hidden="true"></span>LINE 諮詢
  </a>
  <button class="burger" aria-label="選單"><i></i><i></i><i></i></button>
</header>
'''


def page_head(img, eyebrow, h1, crumb):
    return f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow rv in">{eyebrow}</p>
    <h1 class="rv in rv-d1">{h1}</h1>
    <p class="crumb rv in rv-d2"><a href="index.html">首頁</a> ／ {crumb}</p>
  </div>
</section>
'''


def line_band(title="想聊聊您的空間嗎", sub="加 LINE 直接對話，不用填表單。傳張平面圖或現況照片，我們就能給您初步方向。"):
    """LINE 導流區塊 — 取代原本的諮詢表單"""
    return f'''
<section class="sec line-band">
  <div class="wrap-n" style="text-align:center">
    <p class="eyebrow center rv">Let's Talk</p>
    <h2 class="h-sec rv rv-d1">{title}</h2>
    <p class="lede rv rv-d2" style="text-align:center;margin-inline:auto">{sub}</p>
    <div class="line-box rv rv-d3">
      <a class="btn-line" data-line href="#" target="_blank" rel="noopener">
        <span class="ico" aria-hidden="true"></span>
        <span class="tx"><b>加入官方 LINE</b><i data-line-id>@易向室內設計</i></span>
      </a>
      <p class="line-alt">或直接來電　<a href="tel:0333585835">桃園 03-358-5835</a>　·　<a href="tel:0225955532">台北 02-2595-5532</a></p>
    </div>
  </div>
</section>
'''


FOOT = f'''
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div>
        <img class="logo" src="assets/brand/logo-white.png" alt="易向室內設計" width="520" height="125">
        <p>讓家成為情感與心靈的寄託。<br>台北・桃園雙據點，深耕室內設計二十餘年。</p>
      </div>
      <div>
        <p class="foot-h">Sitemap</p>
        <ul class="foot-list">
          <li><a href="about.html">關於易向</a></li>
          <li><a href="works.html">作品總覽</a></li>
          <li><a href="case.html">精選案例</a></li>
          <li><a href="service.html">服務與收費</a></li>
          <li><a href="process.html">設計流程</a></li>
          <li><a href="contact.html">聯絡我們</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Contact</p>
        <ul class="foot-list">
          <li><a href="tel:0225955532">台北 02-2595-5532</a></li>
          <li><a href="tel:0333585835">桃園 03-358-5835</a></li>
          <li><a href="mailto:image238@hotmail.com">image238@hotmail.com</a></li>
          <li><a data-line href="#" target="_blank" rel="noopener">官方 LINE</a></li>
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
  <a class="line" data-line href="#" target="_blank" rel="noopener" aria-label="LINE 諮詢">LINE</a>
  <a href="tel:0333585835" aria-label="撥打電話">撥打電話</a>
</div>

<div class="lb" id="lb">
  <button class="lb-x" id="lbX" aria-label="關閉"></button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="上一件"></button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" id="lbNext" aria-label="下一件"></button>
  <div class="lb-cap"><p class="k" id="lbK"></p><h3 id="lbT"></h3></div>
</div>

<script src="assets/js/config.js?v={CFG_V}"></script>
<script src="assets/js/main.js?v={JS_V}"></script>
</body>
</html>
'''

FLOW = [
    ("01", "初步溝通", "Consultation",
     ["瞭解目前房屋狀況及基本生活需求", "討論業主起居習慣、特殊喜好收藏",
      "提出初步專業建議及工程預算溝通", "風格初步討論"]),
    ("02", "現場丈量", "Site Measurement",
     ["對工程現場進行丈量，並拍照留底", "了解工地現場並初步告知注意事項",
      "資料蒐集完整後進行平面繪製"]),
    ("03", "圖面繪製", "Drafting",
     ["繪製平面規劃配置圖", "討論平面配置並簽訂設計合約"]),
    ("04", "立面及建材討論", "Materials",
     ["解說立面設計圖設計理念", "提供設計材質的相關樣板及性質討論",
      "提供工程報價單，並解說內容", "簽訂工程合約"]),
    ("05", "進場施工", "Construction",
     ["現場立面圖放樣，再次確認細節後簽認放樣驗收單", "排定工程進度表進行施工",
      "施工期間不定期與業主現場溝通", "以嚴謹的態度控管施工品質"]),
    ("06", "完成交屋", "Handover",
     ["相關工程完工後，確認無誤雙方簽認交屋驗收單",
      "保固期內，非人為因素之損壞提供維修保固",
      "保固期後若有維修皆可派工處理，酌收工料費用"]),
]

SERVICES = [
    ("01", "住宅空間", "依生活動線與收納需求量身規劃，兼顧美感與日常實用。"),
    ("02", "商業空間", "以品牌調性為核心，打造具識別度且符合營運效率的場域。"),
    ("03", "建築公共空間", "大廳、交誼廳與公設整體規劃，提升建案整體質感與價值。"),
    ("04", "接待中心・實品屋", "掌握銷售節奏與客層想像，以空間敘事創造成交動能。"),
    ("05", "舊屋翻新", "從管線結構到格局重整，讓老屋重新符合現代生活需求。"),
    ("06", "免費初步諮詢", "初次需求溝通不收費，先了解您的想法與預算方向，再談後續。"),
]

AWARDS = [
    ("2019", "美國 MUSE Design Awards", "Gold Winner 金獎",
     "全球具指標性的國際設計獎項，表彰建築、室內、產品與品牌設計領域之創新與卓越表現。"),
    ("2020", "法國 Novum Design Award", "Gold Winner 金獎",
     "評選涵蓋設計品質、創新性、原創性、技術性與執行力五項標準，金獎為最高等級。"),
    ("2020", "義大利 A′ Design Award", "Silver Winner 銀獎",
     "歐洲歷史最悠久、規模最大的國際設計競賽之一，為全球設計品質的重要指標。"),
]


def flow_html():
    out = []
    for idx, t, en, items in FLOW:
        li = "".join(f"<li>{x}</li>" for x in items)
        out.append(f'''      <article class="flow-i rv"><p class="idx">{idx}</p><div>
        <h3>{t}</h3><p class="en">{en}</p>
        <ul>{li}</ul>
      </div></article>''')
    return "\n".join(out)


def svc_html():
    out = []
    for n, (no, t, d) in enumerate(SERVICES):
        delay = ' rv-d%d' % (n % 3) if n % 3 else ''
        out.append('      <article class="svc-i rv%s"><p class="no">%s</p>'
                   '<h3>%s</h3><p>%s</p></article>' % (delay, no, t, d))
    return "\n".join(out)


def awards_html():
    out = []
    for n, (yr, t, lv, d) in enumerate(AWARDS):
        delay = ' rv-d%d' % n if n else ''
        out.append('      <article class="award rv%s">\n'
                   '        <p class="yr">%s</p><h3>%s</h3>\n'
                   '        <p class="lv">%s</p><p>%s</p></article>' % (delay, yr, t, lv, d))
    return "\n".join(out)


def write(name, body):
    open(name, 'w', encoding='utf-8').write(body)
    print('  ✓', name, f'{len(body):,} bytes')

# ============================================================ 首頁（精簡版）
write('index.html',
  head('index.html', f'{SITE}｜台北室內設計・桃園室內設計',
       '易向室內設計，深耕室內設計二十餘年。台北、桃園雙據點，專營住宅空間、商業空間、接待中心實品屋與舊屋翻新。榮獲美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎、義大利 A′ Design Award 銀獎。',
       preload='assets/hero/1600/h05.jpg', bg=('.hero-bg figure:first-child', 'h05.jpg'))
  + '''
<section class="hero">
  <div class="hero-bg">
    <figure class="on"></figure>
    <figure data-bg="h02.jpg"></figure>
    <figure data-bg="h13.jpg"></figure>
    <figure data-bg="h09.jpg"></figure>
  </div>
  <div class="hero-in">
    <div class="hero-frame">
      <h1>讓家　成為情感與心靈的寄託</h1>
      <p class="sub">Yixiang Interior Design</p>
    </div>
    <p class="tag">台北 ・ 桃園　｜　二十餘年專業經驗</p>
  </div>
  <div class="hero-badges">
    <img src="assets/brand/award_muse.png" alt="MUSE Design Awards 金獎" loading="lazy">
    <img src="assets/brand/award_novum.png" alt="Novum Design Award 金獎" loading="lazy">
  </div>
  <div class="scroll-cue"><span></span>SCROLL</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="philo">
      <div class="philo-fig rv"><img src="assets/hero/1600/h31.jpg"
        srcset="assets/hero/900/h31.jpg 900w, assets/hero/1600/h31.jpg 1600w"
        sizes="(max-width:1080px) 92vw, 46vw" alt="易向室內設計 作品實景" loading="lazy"></div>
      <div class="philo-body">
        <p class="eyebrow rv">About Us</p>
        <h2 class="h-sec rv rv-d1">設計理念 <span class="thin">Philosophy</span></h2>
        <p class="philo-q rv rv-d2">室內設計的真諦不在譁眾取寵，而是來自於居住者<em>發自內心的認同與肯定</em>。</p>
        <div class="rv rv-d3" style="margin-top:32px">
          <p>從事室內設計二十多個年頭，如何讓家成為情感與心靈的寄託，一直是整個設計團隊所秉持的原則。</p>
          <p>注重完美的線條比例，更在乎客戶的生活體驗與需求。</p>
        </div>
        <div class="btn-row rv rv-d4">
          <a class="btn btn-brand" href="about.html"><span>了解易向</span><span>→</span></a>
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

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Selected Works</p>
      <h2 class="h-sec rv rv-d1">精選作品</h2>
      <p class="lede rv rv-d2" style="text-align:center">從奢華新古典到自然人文禪風，每一件作品都始於一次完整的傾聽。</p>
    </div>
    <div class="grid" id="featured"></div>
    <div class="btn-row center rv">
      <a class="btn" href="works.html"><span>瀏覽全部 86 件作品</span><span>→</span></a>
    </div>
  </div>
</section>

<section class="sec-teaser">
  <a class="teaser" href="case.html">
    <img src="assets/case/800/hehui-01.jpg" alt="合輝大璽 現代輕奢住宅" loading="lazy">
    <div class="teaser-tx">
      <p class="k">Featured Project</p>
      <h2>合輝大璽</h2>
      <p class="st">現代輕奢住宅　｜　桃園　｜　約 55 坪</p>
      <span class="more">看完整案例　→</span>
    </div>
  </a>
</section>

<section class="sec sec-dark">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Awards</p>
      <h2 class="h-sec rv rv-d1">國際設計獎項</h2>
    </div>
    <div class="awards">
''' + awards_html() + '''
    </div>
    <div class="btn-row center rv rv-d3">
      <a class="btn btn-light" href="about.html#press"><span>媒體專訪與影片</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)

# ============================================================ 關於易向
VIDS = [("E9b6lGOiFKQ", "【空間設計秘訣開箱】輕工業風格居家設計"),
        ("WYuW_FUWt28", "【空間設計秘訣開箱】莫蘭迪色低調奢華設計專訪"),
        ("QFgFmfa30vI", "【空間設計秘訣開箱】四個年輕人一定要做的設計"),
        ("AegVGxrSr7k", "【直擊設計師的家】收納秘訣大公開・玄關客廳書房篇")]

vid_html = "\n".join(
    '      <article class="vid rv%s">\n'
    '        <div class="vid-fr"><iframe src="https://www.youtube.com/embed/%s" title="%s"\n'
    '          loading="lazy" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"\n'
    '          allowfullscreen></iframe></div>\n'
    '        <h3>%s</h3>\n      </article>'
    % (' rv-d%d' % (n % 3) if n % 3 else '', vid, t, t)
    for n, (vid, t) in enumerate(VIDS))

write('about.html',
  head('about.html', f'關於易向｜{SITE}',
       '易向室內設計深耕二十餘年，榮獲美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎、義大利 A′ Design Award 銀獎。',
       'assets/hero/1600/h11.jpg', bg=('.page-head', 'h11.jpg'))
  + page_head('assets/hero/1600/h11.jpg', 'About Us', '關於易向', '關於易向')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="philo">
      <div class="philo-fig rv"><img src="assets/hero/1600/h31.jpg"
        srcset="assets/hero/900/h31.jpg 900w, assets/hero/1600/h31.jpg 1600w"
        sizes="(max-width:1080px) 92vw, 46vw" alt="易向室內設計 作品實景" loading="lazy"></div>
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
''' + awards_html() + '''
    </div>
    <div class="badges rv rv-d2">
      <img src="assets/brand/award_muse.png" alt="MUSE Design Awards Gold Winner" loading="lazy">
      <img src="assets/brand/award_novum.png" alt="Novum Design Award Gold Winner" loading="lazy">
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
''' + line_band() + FOOT)

# ============================================================ 作品總覽（分頁）
write('works.html',
  head('works.html', f'作品總覽｜{SITE}',
       '易向室內設計作品總覽，收錄奢華新古典風、自然人文禪風、現代素雅休閒風、小坪數溫馨宅與公共空間共 86 件完工實績。',
       'assets/hero/1600/h09.jpg', bg=('.page-head', 'h09.jpg'))
  + page_head('assets/hero/1600/h09.jpg', 'Works', '作品總覽', '作品總覽')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Portfolio</p>
      <h2 class="h-sec rv rv-d1">完工實績 <span class="thin">共 <span id="wcount">86</span> 件</span></h2>
      <p class="lede rv rv-d2" style="text-align:center">點選任一件作品可放大檢視，左右方向鍵可連續瀏覽。</p>
    </div>
    <div class="filters" id="filters"></div>
    <div class="grid" id="allworks"></div>
    <nav class="pager" id="pager" aria-label="作品分頁"></nav>
  </div>
</section>
''' + line_band('看到喜歡的空間了嗎', '加 LINE 告訴我們您的坪數與格局，我們會給您初步的規劃方向與預算範圍。') + FOOT)

# ============================================================ 精選案例
write('case.html',
  head('case.html', f'精選案例 合輝大璽｜{SITE}',
       '合輝大璽・現代輕奢住宅，桃園住宅空間設計，約 55 坪。以淺色木質、石材紋理與柔和曲線為設計語彙，開放式客餐廳整合、弧形天花與大面採光。',
       'assets/case/hehui-01.jpg')
  + '<style>.page-head{background-image:url(assets/case/1200/hehui-01.jpg)}'
    '@media(max-width:720px){.page-head{background-image:url(assets/case/800/hehui-01.jpg)}}</style>'
  + page_head('assets/case/hehui-01.jpg', 'Featured Project', '合輝大璽', '精選案例')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="case-lead">
      <div class="rv">
        <p class="eyebrow">Project Info</p>
        <h2 class="h-sec">合輝大璽 <span class="thin">現代輕奢住宅</span></h2>
        <p class="lede">以淺色木質、石材紋理與柔和曲線為設計語彙，透過開放式客餐廳整合、弧形天花與大面採光，打造兼具舒適感與生活儀式感的現代住宅空間。</p>
      </div>
      <dl class="case-spec rv rv-d1">
        <dt>Type</dt><dd>住宅空間設計</dd>
        <dt>Location</dt><dd>桃園市</dd>
        <dt>Area</dt><dd>約 55 坪</dd>
        <dt>Style</dt><dd>現代輕奢 × 溫潤木質</dd>
      </dl>
    </div>
    <div class="case-tags rv rv-d2" style="justify-content:center;margin-top:38px">
      <span>開放設計</span><span>收納機能</span><span>質感生活</span>
    </div>
  </div>
</section>

<section class="sec sec-alt" style="padding-top:0">
  <div class="wrap">
    <div class="case-grid" id="caseGrid"></div>
  </div>
</section>
''' + line_band('想要類似的規劃嗎', '加 LINE 傳給我們您的平面圖或現況照片，我們會依您的坪數與需求給出初步方向。') + FOOT)

# ============================================================ 服務與收費
write('service.html',
  head('service.html', f'服務項目與收費標準｜{SITE}',
       '易向室內設計服務項目涵蓋住宅空間、商業空間、建築公共空間、接待中心實品屋與舊屋翻新，並提供免費初步諮詢。',
       'assets/hero/1600/h15.jpg', bg=('.page-head', 'h15.jpg'))
  + page_head('assets/hero/1600/h15.jpg', 'Service', '服務與收費', '服務與收費')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow rv">Service</p>
      <h2 class="h-sec rv rv-d1">服務項目</h2>
      <p class="lede rv rv-d2">從住宅到商業空間，從新成屋到舊屋翻新，易向提供完整的設計與工程一條龍服務。</p>
    </div>
    <div class="svc">
''' + svc_html() + '''
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
      <article class="fee rv rv-d2"><p class="no">03</p><h3>初步諮詢</h3>
        <p class="amt">免費</p>
        <ul><li>初步需求溝通不收費</li><li>提供初步專業建議與預算方向</li><li>說明後續設計與工程的計價方式</li></ul></article>
    </div>
    <p class="note rv">※ 以上為易向室內設計之計價原則，實際金額以雙方簽訂之設計合約與工程合約為準。</p>
    <div class="btn-row rv">
      <a class="btn btn-brand" href="process.html"><span>看設計流程</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)

# ============================================================ 設計流程
write('process.html',
  head('process.html', f'設計流程｜{SITE}',
       '易向室內設計的六階段設計流程：初步溝通、現場丈量、圖面繪製、立面及建材討論、進場施工、完成交屋。每一步都留下可確認的紀錄。',
       'assets/hero/1600/h19.jpg', bg=('.page-head', 'h19.jpg'))
  + page_head('assets/hero/1600/h19.jpg', 'Design Flow', '設計流程', '設計流程')
  + '''
<section class="sec">
  <div class="wrap-n">
    <div class="sec-head center">
      <p class="eyebrow center rv">Design Flow</p>
      <h2 class="h-sec rv rv-d1">六個階段</h2>
      <p class="lede rv rv-d2" style="text-align:center">每一步都留下可以確認的紀錄，讓您隨時知道進度走到哪裡。</p>
    </div>
    <div class="flow">
''' + flow_html() + '''
    </div>
    <div class="btn-row center rv">
      <a class="btn btn-brand" href="service.html#fee"><span>看收費標準</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)

# ============================================================ 聯絡我們
write('contact.html',
  head('contact.html', f'聯絡我們｜{SITE}',
       '易向室內設計台北公司：台北市南京東路二段137號14樓 02-2595-5532；桃園公司：桃園市桃園區經國路719號1樓 03-358-5835。加 LINE 免費初步諮詢。',
       'assets/hero/1600/h17.jpg', bg=('.page-head', 'h17.jpg'))
  + page_head('assets/hero/1600/h17.jpg', 'Contact', '聯絡我們', '聯絡我們')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Our Offices</p>
      <h2 class="h-sec rv rv-d1">台北 ・ 桃園 雙據點</h2>
      <p class="lede rv rv-d2" style="text-align:center">初次諮詢不收費，歡迎先加 LINE 或直接來電。</p>
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
''' + line_band('加 LINE 最快', '傳張平面圖或現況照片，我們會先給您初步方向。不用填表單、不用留電話。')
  + '''
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
