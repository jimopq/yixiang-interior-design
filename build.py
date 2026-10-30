# -*- coding: utf-8 -*-
"""易向室內設計 — 靜態頁產生器。所有頁面共用同一份頁首／頁尾／元件。"""

import hashlib
import json
_CD = json.load(open('data/cases.json', encoding='utf-8'))
CASES = _CD['cases']
STYLES = _CD.get('styles', [])
FEAT = CASES[0]


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
    ("service.html", "Service", "服務收費"),
    ("process.html", "Process", "設計流程"),
    ("blog.html",    "Blog",    "設計筆記"),
    ("video.html",   "Video",   "影音專區"),
    ("contact.html", "Contact", "聯絡我們"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600'
 '&family=Noto+Serif+TC:wght@400&display=swap" rel="stylesheet">')

SITE = "易向室內設計 IMAGE DESIGN・澤向室內裝修工程有限公司"



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
        % (h, ' class="on"' if (h == cur or (h == 'blog.html' and cur.startswith('blog-')) or (h == 'works.html' and cur.startswith('case-'))) else '', e, c)
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
<link rel="icon" href="assets/brand/favicon.png">
{FONTS}
{pl}
<link rel="stylesheet" href="assets/css/style.css?v={CSS_V}">
{css}
</head>
<body>

<header class="site-head">
  <a class="brand" href="index.html" aria-label="易向室內設計 首頁">
    <img class="l-white" src="assets/brand/mark-white.png" alt="" width="284" height="158">
    <img class="l-ink" src="assets/brand/mark-ink.png" alt="" width="284" height="158">
    <span class="brand-tx"><b>易向室內設計</b><span class="brand-co" aria-label="澤向室內裝修工程有限公司">澤向室內裝修</span></span>
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
      <p class="line-alt"><span class="la-k">直接來電</span><a href="tel:0225955535">台北 02-2595-5535</a><a href="tel:0333585835">桃園 03-358-5835</a></p>
    </div>
  </div>
</section>
'''


FOOT = f'''
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div>
        <img class="logo" src="assets/brand/logo-white-v2.png" alt="易向室內設計" width="992" height="158">
        <p class="co">易向室內設計有限公司<br>澤向室內裝修工程有限公司</p>
        <p>讓家成為情感與心靈的寄託。<br>台北・桃園雙據點，深耕室內設計近三十年。</p>
      </div>
      <div>
        <p class="foot-h">Sitemap</p>
        <ul class="foot-list">
          <li><a href="about.html">關於易向</a></li>
          <li><a href="works.html">作品總覽</a></li>
          <li><a href="service.html">服務與收費</a></li>
          <li><a href="process.html">設計流程</a></li>
          <li><a href="blog.html">設計筆記</a></li>
          <li><a href="video.html">影音專區</a></li>
          <li><a href="awards.html">得獎作品</a></li>
          <li><a href="contact.html">聯絡我們</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-h">Contact</p>
        <ul class="foot-list">
          <li><a href="tel:0225955535">台北 02-2595-5535</a></li>
          <li><a href="tel:0333585835">桃園 03-358-5835</a></li>
          <li><a href="mailto:image238@hotmail.com">image238@hotmail.com</a></li>
          <li><a data-line href="#" target="_blank" rel="noopener">官方 LINE</a></li>
          <li><a href="https://www.facebook.com/profile.php?id=100075962749629" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© 2026 易向室內設計｜澤向室內裝修工程有限公司</span>
      <span>台北市南京東路二段137號14樓 ・ 桃園市桃園區經國路719號1樓</span>
    </div>
  </div>
</footer>

<div class="dock">
  <a class="line" data-line href="#" target="_blank" rel="noopener" aria-label="LINE 諮詢">LINE</a>
  <a href="tel:0225955535" aria-label="撥打電話">撥打電話</a>
</div>

<div class="lb" id="lb">
  <button class="lb-x" id="lbX" aria-label="關閉"></button>
  <div class="lb-col" id="lbCol"></div>
</div>

<script src="assets/js/config.js?v={CFG_V}"></script>
<script src="assets/js/main.js?v={JS_V}"></script>
</body>
</html>
'''

FLOW = [
    ("01", "先聊聊", "Consultation",
     ["聽您說說現在的房子，和每天是怎麼生活的", "起居習慣、喜歡的東西、想收藏的物件，都可以聊",
      "我們會先給一些專業建議，也一起把預算的方向抓出來", "順便聊聊喜歡的風格，不用急著決定"]),
    ("02", "到現場看看", "Site Measurement",
     ["到現場丈量、拍照，把每個尺寸都記清楚", "看看現場狀況，先告訴您哪些地方要特別留意",
      "資料齊全後，就開始畫平面圖"]),
    ("03", "把家畫出來", "Drafting",
     ["繪製平面配置圖，把動線和收納先安排好", "一起討論平面配置，確定方向後簽訂設計合約"]),
    ("04", "挑材質、談細節", "Materials",
     ["用立面圖跟您說明每一面牆的想法", "拿實際的材質樣板給您摸摸看、比比看",
      "提供工程報價單，一項一項說清楚", "確認沒問題後簽訂工程合約"]),
    ("05", "開工了", "Construction",
     ["先在現場放樣，再一次確認細節後請您簽認", "排好進度表，按部就班施工",
      "施工期間會常常跟您在現場碰面、更新進度", "每個環節都盯著品質，不馬虎"]),
    ("06", "交屋，開始新生活", "Handover",
     ["完工後一起驗收，確認沒問題再簽認交屋",
      "保固期內，非人為因素的損壞我們負責修",
      "保固期後若需要維修也可以找我們，只酌收工料費"]),
]

SERVICES = [
    ("01", "住宅空間", "從您每天怎麼走、東西放哪裡開始想，讓家好看，也好住。"),
    ("02", "客變設計", "預售屋交屋前先把格局、水電和建材調整好，省下交屋後再拆再做的辛苦與花費。"),
    ("03", "舊屋翻新", "從管線到格局一起整理，讓住了很多年的老房子，重新跟上現在的生活。"),
    ("04", "商業空間", "把品牌的個性放進空間裡，讓客人一進門就有感覺，也讓團隊工作起來更順手。"),
    ("05", "建築公共空間", "大廳、交誼廳與公設一起規劃，讓住戶每天回家的路都舒服。"),
    ("06", "接待中心・實品屋", "用空間說故事，讓來看房的人想像得到住進去的樣子。"),
    ("07", "免費初步諮詢", "第一次聊天不收費。先聽聽您的想法和預算，再一起決定接下來怎麼走。"),
]

AWARDS = [
    ("2020", "義大利 A′ Design Award", "Silver Winner 銀獎",
     "歐洲歷史最久、規模最大的設計競賽之一。一個台灣的家，在這裡被世界看見。"),
    ("2019", "美國 MUSE Design Awards", "Gold Winner 金獎",
     "跨越建築、室內與品牌設計的國際獎項。得獎的那個家，叫「木的從容」。"),
    ("2020", "法國 Novum Design Award", "Gold Winner 金獎",
     "從設計品質到施工執行力一起評。金獎是最高等級，我們很珍惜。"),
    ("", "ADA 第八屆亞洲設計獎", "獲獎作品",
     "亞洲各地的住宅與商業空間一起比。能入列，是對我們日常工作的一種肯定。"),
    ("", "北京創新中國設計獎", "獲獎作品",
     "聚焦華人設計圈的創新表現。謝謝評審，也謝謝願意把家交給我們的屋主。"),
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
        wide = ' wide' if n == len(SERVICES) - 1 and len(SERVICES) % 3 == 1 else ''
        out.append('      <article class="svc-i%s rv%s"><p class="no">%s</p>'
                   '<h3>%s</h3><p>%s</p></article>' % (wide, delay, no, t, d))
    return "\n".join(out)


AWARD_LINK = {"義大利 A′ Design Award": "awards.html#ada", "美國 MUSE Design Awards": "awards.html#muse",
              "法國 Novum Design Award": "awards.html#novum"}

def awards_html():
    out = []
    for n, (yr, t, lv, d) in enumerate(AWARDS):
        delay = ' rv-d%d' % n if n else ''
        href = AWARD_LINK.get(t)
        tag = 'a' if href else 'article'
        more = '<span class="more">看得獎作品　→</span>' if href else ''
        out.append('      <%s class="award rv%s%s"%s>\n'
                   '        <p class="yr">%s</p><h3>%s</h3>\n'
                   '        <p class="lv">%s</p><p>%s</p>%s</%s>'
                   % (tag, delay, ' award-top' if n == 0 else '', (' href="%s"' % href) if href else '',
                      yr, t, lv, d, more, tag))
    return "\n".join(out)


def write(name, body):
    open(name, 'w', encoding='utf-8').write(body)
    print('  ✓', name, f'{len(body):,} bytes')

# ============================================================ 首頁近期作品
# 業主指定的順序：侘寂溫馨四案 → 莫蘭迪古典（個案頁）→ 古典餘韻（完工實績，點開看同類燈箱）
HOME_FEAT = ['misty-garden', 'south-wind', 'youlin', 'xinghui', 'morandi', 'w:63']
HOME_RHYTHM = ['g-a', 'g-b', 'g-c', 'g-d', 'g-e', 'g-e']

def home_featured():
    works = {w['id']: w for w in json.load(open('data/works.json', encoding='utf-8'))['works']}
    bys = {c['slug']: c for c in CASES}
    out = []
    for n, key in enumerate(HOME_FEAT):
        cls = HOME_RHYTHM[n % len(HOME_RHYTHM)] + (' rv-d%d' % (n % 3 + 1) if n > 1 else '')
        lazy = '' if n < 2 else ' loading="lazy"'
        if key.startswith('w:'):
            w = works[key[2:]]
            f = w['img'].split('/')[-1]; d = w['img'][:-len(f)]
            out.append('      <a class="card card-case %s rv" href="works.html#works" data-id="%s">'
                       '<div class="ph"><img src="%s800/%s" srcset="%s400/%s 400w, %s800/%s 800w, %s1200/%s 1200w" '
                       'sizes="(max-width:720px) 92vw, (max-width:1080px) 46vw, 28vw" alt="%s｜%s"%s decoding="async">'
                       '<div class="card-txt"><h3>%s</h3><p class="m">%s</p></div></div>'
                       '<p class="card-meta">%s</p></a>'
                       % (cls, w['id'], d, f, d, f, d, f, d, f, w['title'], w['catName'], lazy,
                          w['title'], w['catName'], w['catName']))
        else:
            c = bys[key]; dd = c['dir']; f = c['cover']
            meta = '　·　'.join(x for x in (c.get('area'), c.get('ping')) if x) or c.get('style', '')
            out.append('      <a class="card card-case %s rv" href="case-%s.html">'
                       '<div class="ph"><img src="%s/800/%s" srcset="%s/800/%s 800w, %s/1200/%s 1200w" '
                       'sizes="(max-width:720px) 92vw, (max-width:1080px) 46vw, 28vw" alt="%s %s"%s decoding="async">'
                       '<div class="card-txt"><h3>%s</h3><p class="m">%s</p></div></div>'
                       '<p class="card-meta">%s</p></a>'
                       % (cls, c['slug'], dd, f, dd, f, dd, f, c['name'], c['sub'], lazy,
                          c['name'], c['style'], meta))
    return '\n'.join(out)

# ============================================================ 首頁（精簡版）
write('index.html',
  head('index.html', f'{SITE}｜台北室內設計・桃園室內設計',
       '易向室內設計（澤向室內裝修工程有限公司），深耕室內設計近三十年。台北、桃園雙據點，專營住宅空間、客變設計、舊屋翻新、商業空間與接待中心實品屋。榮獲美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎、義大利 A′ Design Award 銀獎。',
       preload='assets/hero/1600/h05.jpg', bg=('.hero-bg figure:first-child', 'h05.jpg'))
  + '''
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"易向室內設計","legalName":"澤向室內裝修工程有限公司","alternateName":"IMAGE DESIGN","url":"https://www.image.net.tw/","email":"image238@hotmail.com","telephone":["02-2595-5535","03-358-5835"],"address":[{"@type":"PostalAddress","streetAddress":"南京東路二段137號14樓","addressLocality":"台北市","addressCountry":"TW"},{"@type":"PostalAddress","streetAddress":"桃園區經國路719號1樓","addressLocality":"桃園市","addressCountry":"TW"}],"award":["2020 義大利 A′ Design Award 銀獎","2019 美國 MUSE Design Awards 金獎","2020 法國 Novum Design Award 金獎","ADA 第八屆亞洲設計獎","北京創新中國設計獎"]}
</script>
<section class="hero">
  <div class="hero-bg">
    <figure class="on"></figure>
    <figure data-bg="h02.jpg"></figure>
    <figure data-bg="h13.jpg"></figure>
    <figure data-bg="h09.jpg"></figure>
  </div>
  <div class="hero-in">
    <div class="hero-frame">
      <h1>讓家<span class="h-sp">　</span><br class="m-br">成為情感與心靈的寄託</h1>
      <p class="sub">Image Design</p>
    </div>
    <p class="tag"><span>台北 ・ 桃園</span><span class="tag-sep">　｜　</span><span>近三十年，陪很多家庭把家住成自己的樣子</span></p>
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
      <div class="philo-fig rv"><img src="assets/philo/home-award.jpg"
        alt="易向室內設計 A' Design Award 銀獎作品" loading="lazy" width="715" height="715"></div>
      <div class="philo-body">
        <p class="eyebrow rv">About Us</p>
        <h2 class="h-sec rv rv-d1">設計理念 <span class="thin">Philosophy</span></h2>
        <p class="philo-q rv rv-d2">好的設計不用張揚，<em>住進去的人覺得舒服、覺得這就是家</em>，才是我們最在意的事。</p>
        <div class="rv rv-d3" style="margin-top:32px">
          <p>做室內設計快三十年了，我們一直相信，家是情感與心靈安放的地方。每一次規劃，都是先聽您怎麼生活，再把空間慢慢調整成您的樣子。</p>
          <p>線條與比例我們很講究，但更在乎的，是您每天回到家時的那份自在。</p>
        </div>
        <div class="btn-row rv rv-d4">
          <a class="btn btn-brand" href="about.html"><span>了解易向</span><span>→</span></a>
        </div>
      </div>
    </div>
    <div class="stats rv">
      <div><p class="n"><small class="pre">近</small>30<small>年</small></p><p class="k">專業經驗</p></div>
      <div><p class="n">數百<small>件</small></p><p class="k">完工實績</p></div>
      <div><p class="n">10<span class="plus">+</span></p><p class="k">國際設計獎・雜誌報導</p></div>
      <div><p class="n"><small class="pre">近</small>1000<small>位</small></p><p class="k">服務客戶</p></div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Recent Works</p>
      <h2 class="h-sec rv rv-d1">近期作品</h2>
      <p class="lede rv rv-d2" style="text-align:center">從侘寂溫馨到奢華新古典，每一個家都是從一次好好的聊天開始的。</p>
    </div>
    <div class="grid" id="featured">
''' + home_featured() + '''
    </div>
    <div class="btn-row center rv">
      <a class="btn" href="works.html"><span>瀏覽全部作品</span><span>→</span></a>
    </div>
  </div>
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
      <a class="btn btn-light" href="video.html"><span>媒體專訪與影片</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)


# ============================================================ 幸福空間雜誌報導
# 內頁掃描來自舊站 /msg2；每篇各自一組燈箱，點縮圖直向翻閱。
PRESS = [
    ("retire",   "框塑古典　生活愜意退休寓所", 2,
     "退休生活自然是要過得愜意自在。居住台北的屋主，兒女皆成家立業，退休後在桃園買下這間頂級大宅，結合社區內完善多元的公共設施，以招待所、度假中心為設計概念，打造出休閒、社交兼具的退休宅。"),
    ("wood",     "木的藝術層次　鋪陳自然人文宅邸", 2,
     "藝術佳作端放櫃體兩側展示層架，透過背牆處光暈投射，在玄關處揭開藝術人文宅邸的序幕。木化石電視牆搭配刻溝規劃的沙發背牆，日光敞朗中，特意不成套的沙發組與木製貴妃椅，描繪隨興不拘泥的人文風尚。"),
    ("soft",     "剛柔交替　重塑人文大宅風華", 2,
     "開闊的無隔間設計，讓動線多向悠遊，並以精采、多材質拼接的牆面做為序曲，低彩度客訂家具搭配烘焙拿鐵色短毛毯，讓每一個步伐、每一次停留，都是讚嘆。"),
    ("humanist", "人文時尚　華美的空間饗宴", 2,
     "玄關地坪鋪設夏目樹石，仿古的質感刻劃出場域力度，銀箔端景牆則與人造皮革鞋櫃相互輝映，交織耀眼光芒。"),
    ("light",    "質感入室　鋪敘大宅光感奢華", 3, ""),
    ("bold",     "大膽打造　完美獨特", 2, ""),
    ("profile",  "Design Notes　設計師專訪・黃瑞楨", 1,
     "幸福空間設計師專欄：易向室內設計總監黃瑞楨談如何以人文觀點，為每個家找到屬於自己的樣子。"),
]

def press_html():
    out = []
    for slug, title, cnt, ex in PRESS:
        d = 'assets/press/%s' % slug
        t = title.replace('　', ' ')
        pages = []
        for i in range(1, cnt + 1):
            pages.append(
                '        <a class="card rv%s" href="%s/1600/%02d.jpg" data-full="%s/1600/%02d.jpg" data-title="%s｜幸福空間雜誌 第 %d 頁">'
                '<div class="ph"><img src="%s/800/%02d.jpg" srcset="%s/800/%02d.jpg 800w, %s/1200/%02d.jpg 1200w, %s/1600/%02d.jpg 1600w" '
                'sizes="(max-width:720px) 92vw, (max-width:1080px) 46vw, 30vw" alt="%s 雜誌內頁 %d" loading="lazy" decoding="async"></div></a>'
                % (' rv-d%d' % i if i > 1 else '', d, i, d, i, t, i,
                   d, i, d, i, d, i, d, i, t, i))
        extra = ('        <p>%s</p>\n' % ex) if ex else ''
        out.append('    <article class="press-a rv" id="press-%s">\n'
                   '      <div class="press-tx">\n'
                   '        <p class="k">幸福空間雜誌</p>\n'
                   '        <h3>%s</h3>\n'
                   '%s'
                   '        <p class="hint">點圖翻閱雜誌內頁 →</p>\n'
                   '      </div>\n'
                   '      <div class="press-pg%s" data-lightbox>\n'
                   '%s\n'
                   '      </div>\n'
                   '    </article>' % (slug, title, extra, ' one' if cnt == 1 else '', "\n".join(pages)))
    return "\n".join(out)

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
       '易向室內設計（澤向室內裝修工程有限公司）深耕近三十年，榮獲美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎、義大利 A′ Design Award 銀獎。',
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
        <p class="philo-q rv rv-d2">好的設計不用張揚，<em>住進去的人覺得舒服、覺得這就是家</em>，才是我們最在意的事。</p>
        <div class="rv rv-d3" style="margin-top:32px">
          <p>做室內設計快三十年了，我們一直相信，家是情感與心靈安放的地方。每一次規劃，都是先聽您怎麼生活，再把空間慢慢調整成您的樣子。</p>
          <p>多聊一點、多想一步。我們把人放在設計的中心，空間自然就會有溫度。</p>
          <p>收納與美感不必二選一，一點巧思加上扎實的施工，就能讓家人每天多一些自在的互動。</p>
          <p>線條與比例我們很講究，但不會把自己的喜好硬套在您身上，也不會拿學院派的理論說服您。您的生活怎麼過，家就怎麼長。</p>
        </div>
      </div>
    </div>
    <div class="stats rv">
      <div><p class="n"><small class="pre">近</small>30<small>年</small></p><p class="k">專業經驗</p></div>
      <div><p class="n">數百<small>件</small></p><p class="k">完工實績</p></div>
      <div><p class="n">10<span class="plus">+</span></p><p class="k">國際設計獎・雜誌報導</p></div>
      <div><p class="n"><small class="pre">近</small>1000<small>位</small></p><p class="k">服務客戶</p></div>
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

<section class="sec" id="license">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">License</p>
      <h2 class="h-sec rv rv-d1">專業證照</h2>
      <p class="lede rv rv-d2" style="text-align:center">設計與施工都由內政部登記在案的專業技術人員負責，您的家交給有證照的人。</p>
    </div>
    <article class="press-a rv" style="border-top:0;padding-top:0">
      <div class="press-tx">
        <p class="k">內政部核發</p>
        <h3>建築物室內裝修專業技術人員登記證</h3>
        <p>登記資格：專業設計技術人員、專業施工技術人員<br>登記證字號：內營室技字第 40EC021327 號<br>有效期限：民國 116 年 4 月 27 日</p>
        <p class="hint">點圖放大檢視 →</p>
      </div>
      <div class="press-pg one" data-lightbox style="max-width:520px">
        <a class="card rv" href="assets/cert/license-1600.jpg" data-full="assets/cert/license-1600.jpg" data-title="建築物室內裝修專業技術人員登記證｜內政部">
          <div class="ph" style="aspect-ratio:707/1000"><img src="assets/cert/license-900.jpg" srcset="assets/cert/license-900.jpg 900w, assets/cert/license-1600.jpg 1600w" sizes="(max-width:720px) 92vw, 520px" alt="建築物室內裝修專業技術人員登記證" loading="lazy" decoding="async"></div>
        </a>
      </div>
    </article>
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
    <div class="btn-row center rv">
      <a class="btn btn-brand" href="video.html#press"><span>翻閱幸福空間雜誌報導</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)



# ============================================================ 得獎作品
# 三個國際獎項的得獎作品與證書，圖來自舊站 /news/1501、1502、1503。
AWARD_PAGES = [
    ("ada", "2020", "義大利 A′ Design Award", "Silver Winner 銀獎", "Essence of Excellence・住宅空間",
     "一個台北的家，用木皮、鍍鈦與石材把日常收得安靜而有層次。這件作品在義大利 A′ Design Award 的室內空間類拿下銀獎，也是我們第一次在歐洲最大的設計競賽裡，被世界看見。",
     ["得獎證書與媒體頁", "得獎證書與媒體頁", "餐廳", "餐廳", "客廳", "主臥", "書房臥室"]),
    ("muse", "2019", "美國 MUSE Design Awards", "Gold Winner 金獎", "Composed Charms of Woods・木的從容",
     "屋主想要一個像木頭一樣溫潤、不喧嘩的家。我們用木作、線板與一點點藍，把客餐廳、書房和每個房間都安排得剛剛好。這件作品獲得美國 MUSE Design Awards 室內設計金獎。",
     ["得獎證書", "客廳", "客廳", "餐廳", "餐廳", "主臥", "次臥", "次臥", "書房臥室"]),
    ("novum", "2020", "法國 Novum Design Award", "Gold Winner 金獎", "Essence of Excellence・新古典住宅",
     "線板、雕刻與水晶燈把古典說得從容，灰白色調讓大宅有了現代的呼吸。法國 Novum Design Award 從設計品質到施工執行力一起評分，這件作品拿到最高等級的金獎。",
     ["得獎證書", "客廳", "玄關", "走道", "書房", "客廳", "客餐廳", "主臥", "書房臥室"]),
]

def award_page_html():
    out = []
    for slug, yr, t, lv, work, lead, caps in AWARD_PAGES:
        d = 'assets/awards/%s' % slug
        cards = []
        for i, cap in enumerate(caps, 1):
            cards.append(
                '      <a class="card g-w rv%s" href="%s/%02d.jpg" data-full="%s/%02d.jpg" data-title="%s｜%s">'
                '<div class="ph"><img src="%s/800/%02d.jpg" srcset="%s/800/%02d.jpg 800w, %s/1200/%02d.jpg 1200w" '
                'sizes="(max-width:720px) 92vw, (max-width:1080px) 46vw, 30vw" alt="%s %s" loading="lazy" decoding="async"></div></a>'
                % (' rv-d%d' % (i % 3) if i % 3 else '', d, i, d, i, t, cap, d, i, d, i, d, i, t, cap))
        out.append('''<section class="award-sec" id="%s">
  <div class="wrap">
    <div class="award-lead rv">
      <p class="eyebrow center">%s</p>
      <h2 class="h-sec">%s</h2>
      <p class="lv">%s</p>
      <p class="lede" style="margin-inline:auto;text-align:center"><b>%s</b><br>%s</p>
    </div>
    <div class="case-grid grid" data-lightbox>
%s
    </div>
  </div>
</section>''' % (slug, yr, t, lv, work, lead, "\n".join(cards)))
    return "\n".join(out)

write('awards.html',
  head('awards.html', f'得獎作品｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）得獎作品：義大利 A′ Design Award 銀獎、美國 MUSE Design Awards 金獎、法國 Novum Design Award 金獎的完整作品與證書。',
       'assets/awards/muse/02.jpg', bg=('.page-head', 'h27.jpg'))
  + page_head('assets/hero/1600/h27.jpg', 'Awards', '得獎作品', '<a href="about.html#awards">國際設計獎項</a> ／ 得獎作品')
  + award_page_html()
  + line_band('也想要一個被看見的家嗎', '加 LINE 傳張平面圖或現況照片，我們會先給您初步方向，不收費。') + FOOT)

# ============================================================ 影音專區
write('video.html',
  head('video.html', f'影音專區｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）影音專區：設計師親自開箱的空間設計秘訣、媒體專訪與幸福空間雜誌報導。',
       'assets/hero/1600/h15.jpg', bg=('.page-head', 'h15.jpg'))
  + page_head('assets/hero/1600/h15.jpg', 'Video', '影音專區', '影音專區')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Press &amp; Video</p>
      <h2 class="h-sec rv rv-d1">設計師開箱・媒體專訪</h2>
      <p class="lede rv rv-d2" style="text-align:center">把設計時在想什麼、住進去之後怎麼用，直接說給您聽。</p>
    </div>
    <div class="vids">
''' + vid_html + '''
    </div>
  </div>
</section>

<section class="sec sec-alt" id="press">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Magazine</p>
      <h2 class="h-sec rv rv-d1">幸福空間雜誌報導</h2>
      <p class="lede rv rv-d2" style="text-align:center">這幾年被雜誌記錄下來的家。點任一張內頁，就能像翻雜誌一樣往下看。</p>
    </div>
    <div class="press-list">
''' + press_html() + '''
    </div>
  </div>
</section>
''' + line_band('看完影片，想聊聊自己的家嗎', '加 LINE 傳張平面圖或現況照片，我們會先給您初步方向，不收費。') + FOOT)

# ============================================================ 作品總覽（分頁）
# ============================================================ 精選案例
# 資料在 data/cases.json：案名、規格、材質、設計概念與已排序的圖庫。
# 索引頁 case.html 列出全部；每案產生 case-<slug>.html。

def case_img(c, f, eager=False, alt=''):
    d = c['dir']
    return ('<img src="%s/800/%s" srcset="%s/800/%s 800w, %s/1200/%s 1200w" '
            'sizes="(max-width:720px) 92vw, (max-width:1080px) 46vw, 30vw" alt="%s"%s decoding="async">'
            % (d, f, d, f, d, f, alt, '' if eager else ' loading="lazy"'))

def case_card(c, n):
    meta = '　·　'.join(x for x in (c.get('area'), c.get('ping')) if x) or c.get('style', '')
    # 地區與坪數放在照片下方，不壓在照片上，長輩在手機上也看得清楚
    return ('      <a class="card card-case g-w rv%s" href="case-%s.html" data-cat="%s">'
            '<div class="ph">%s<div class="card-txt"><h3>%s</h3><p class="m">%s</p></div></div>'
            '<p class="card-meta">%s</p></a>'
            % (' rv-d%d' % (n % 3) if n % 3 else '', c['slug'], ' '.join(c.get('cats', [])),
               case_img(c, c['cover'], eager=n < 6, alt=c['name'] + ' ' + c['sub']),
               c['name'], c['style'], meta))

def case_gallery(c):
    out = []; last = None; n = 0
    for g in c['gallery']:
        if g.get('room') and g['room'] != last:
            out.append('      <h3 class="room-h">%s</h3>' % g['room']); last = g['room']
        out.append('      <a class="card g-w rv%s" href="%s/1200/%s" data-full="%s/1200/%s" data-title="%s">'
                   '<div class="ph">%s</div></a>'
                   % (' rv-d%d' % (n % 3) if n % 3 else '', c['dir'], g['f'], c['dir'], g['f'],
                      c['name'] + '｜' + (g.get('room') or c['sub']),
                      case_img(c, g['f'], eager=n < 3, alt='%s %s 第 %d 張' % (c['name'], g.get('room', ''), n + 1))))
        n += 1
    return "\n".join(out)

CASE_LB = line_band('想要類似的規劃嗎', '加 LINE 傳給我們您的平面圖或現況照片，我們會依您的坪數與需求給出初步方向。')

CASE_LEDE = "每一個家，都從一次好好的傾聽開始。走進這些空間，看看光線、材質與日常，是怎麼被溫柔地安放。"
INDEX_BODY = """
<section class="sec" id="cases">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Case Studies</p>
      <h2 class="h-sec rv rv-d1" id="ctitle">精選案例</h2>
      <p class="lede rv rv-d2" id="clede" data-default="%s" style="text-align:center">%s</p>
    </div>
    <div class="filters" id="cfilters">
      <button class="on" data-c="all" data-name="精選案例"><span class="en">All</span>全部案例</button>
%s
    </div>
    <div class="grid" id="casegrid">
%s
    </div>
  </div>
</section>
""" % (CASE_LEDE, CASE_LEDE,
       "\n".join('      <button data-c="%s" data-name="%s" data-desc="%s"><span class="en">%s</span>%s</button>'
                 % (st['slug'], st['name'], st['desc'], st['en'], st['name']) for st in STYLES),
       "\n".join(case_card(c, n) for n, c in enumerate(CASES)))


WORKS_BODY = '''
<section class="sec sec-alt" id="works">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Portfolio</p>
      <h2 class="h-sec rv rv-d1" id="wtitle">完工實績</h2>
      <p class="lede rv rv-d2" style="text-align:center">歷年完工的作品都在這裡。點選任一件即可放大，往下滑就能一口氣看完同系列的空間。</p>
    </div>
    <div class="filters" id="filters"></div>
    <div class="grid" id="allworks"></div>
    <nav class="pager" id="pager" aria-label="作品分頁"></nav>
  </div>
</section>
'''

# 作品總覽 = 上半部精選案例（四種風格、每案一頁）＋下半部歷年完工實績（舊站 86 件）
write('works.html',
  head('works.html', f'作品總覽｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）作品總覽：侘寂溫馨、輕奢優雅、現代木質、奢華新古典四種風格的精選案例，以及歷年完工實績。',
       CASES[0]['dir'] + '/1200/' + CASES[0]['cover'], bg=('.page-head', 'h09.jpg'))
  + page_head('assets/hero/1600/h09.jpg', 'Works', '作品總覽', '作品總覽')
  + INDEX_BODY + WORKS_BODY + CASE_LB + FOOT)

# 舊網址 case.html 轉到合併後的作品總覽
write('case.html', '''<!DOCTYPE html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8"><title>作品總覽｜''' + SITE + '''</title>
<meta name="robots" content="noindex"><link rel="canonical" href="works.html">
<meta http-equiv="refresh" content="0;url=works.html#cases"><script>location.replace("works.html#cases")</script>
</head><body><a href="works.html#cases">作品總覽</a></body></html>
''')

CASE_BODY = """
<section class="sec">
  <div class="wrap">
    <div class="case-lead">
      <div class="rv">
        <p class="eyebrow">Project Info</p>
        <h2 class="h-sec">%(name)s <span class="thin">%(sub)s</span></h2>
        <p class="lede">%(concept)s</p>
      </div>
      <dl class="case-spec rv rv-d1">%(spec)s</dl>
    </div>
%(mat)s
  </div>
</section>

<section class="sec sec-alt" style="padding-top:0">
  <div class="wrap">
    <div class="case-grid grid" data-lightbox>
%(gallery)s
    </div>
    %(nav)s
  </div>
</section>
"""

for n, c in enumerate(CASES):
    prev_ = CASES[n - 1] if n > 0 else None
    next_ = CASES[n + 1] if n < len(CASES) - 1 else None
    spec = [('地區', c['area']), ('格局', c.get('layout', '')), ('坪數', c['ping']), ('風格', c['style'])]
    nav = '<nav class="case-nav rv">'
    nav += ('<a class="prev" href="case-%s.html"><span class="k">上一案</span><b>%s</b></a>' % (prev_['slug'], prev_['name'])) if prev_ else '<span></span>'
    nav += '<a class="all" href="works.html#cases">全部案例</a>'
    nav += ('<a class="next" href="case-%s.html"><span class="k">下一案</span><b>%s</b></a>' % (next_['slug'], next_['name'])) if next_ else '<span></span>'
    nav += '</nav>'
    body = CASE_BODY % dict(
        name=c['name'], sub=c['sub'], concept=c['concept'],
        spec="".join('<dt>%s</dt><dd>%s</dd>' % kv for kv in spec if kv[1]),
        mat=('    <div class="case-mat rv rv-d2">\n      <p class="k">Materials　使用材質</p>\n      <div class="case-tags">%s</div>\n    </div>'
             % "".join('<span>%s</span>' % m for m in c['materials'])) if c.get('materials') else '',
        gallery=case_gallery(c), nav=nav)
    write('case-%s.html' % c['slug'],
      head('case-%s.html' % c['slug'], '%s｜%s｜作品總覽｜%s' % (c['name'], c['sub'], SITE),
           '%s・%s，%s %s，%s。%s' % (c['name'], c['sub'], c['area'], c['ping'], c['style'], c['concept'][:60]),
           c['dir'] + '/1200/' + c['cover'])
      + '<style>.page-head{background-image:url(%s/1200/%s)}@media(max-width:720px){.page-head{background-image:url(%s/800/%s)}}</style>'
        % (c['dir'], c['cover'], c['dir'], c['cover'])
      + page_head('', 'Case Study', c['name'], '<a href="works.html#cases">作品總覽</a> ／ ' + c['name'])
      + body + CASE_LB + FOOT)

# ============================================================ 服務與收費
write('service.html',
  head('service.html', f'服務項目與收費標準｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）服務項目涵蓋住宅空間、客變設計、舊屋翻新、商業空間、建築公共空間與接待中心實品屋，並提供免費初步諮詢。',
       'assets/hero/1600/h15.jpg', bg=('.page-head', 'h15.jpg'))
  + page_head('assets/hero/1600/h15.jpg', 'Service', '服務與收費', '服務與收費')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow rv">Service</p>
      <h2 class="h-sec rv rv-d1">服務項目</h2>
      <p class="lede rv rv-d2">不管是新家、老屋，還是還在蓋的預售屋，從設計到施工我們都會陪您走完。</p>
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
      <p class="lede rv rv-d2">每個家的需求不同，費用也會有些差異。下面是我們大致的計價方式，給您先參考；實際費用等丈量、聊過之後，會再一項一項跟您說清楚。</p>
    </div>
    <div class="fees">
      <article class="fee rv"><p class="no">01</p><h3>初步諮詢</h3>
        <p class="amt">免費</p>
        <ul><li>第一次聊天不收費</li><li>先給您專業建議和預算方向</li><li>把後續設計與工程怎麼計價說清楚</li></ul></article>
      <article class="fee rv rv-d1"><p class="no">02</p><h3>設計合約</h3>
        <p class="amt">6,000 – 8,000<small>元 / 坪</small></p>
        <ul><li>住宅依室內面積計價</li><li>實際施作面積與風格不同，費用會有差</li><li>商業空間、辦公室另外依個案討論</li></ul></article>
      <article class="fee rv rv-d2"><p class="no">03</p><h3>工程合約</h3>
        <p class="amt">個案報價</p>
        <ul><li>以高質感的施工品質為前提</li><li>依坪數大小與風格規劃估算</li><li>施工項目和立面材質不同，價格也不同</li><li>會給您一份完整的工程總預算</li></ul></article>
    </div>
    <p class="note rv">※ 以上為易向室內設計（澤向室內裝修工程有限公司）之計價原則，實際金額以雙方簽訂之設計合約與工程合約為準。</p>
    <div class="btn-row rv">
      <a class="btn btn-brand" href="process.html"><span>看設計流程</span><span>→</span></a>
    </div>
  </div>
</section>
''' + line_band() + FOOT)

# ============================================================ 設計流程
write('process.html',
  head('process.html', f'設計流程｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）的六階段設計流程：初步溝通、現場丈量、圖面繪製、立面及建材討論、進場施工、完成交屋。每一步都留下可確認的紀錄。',
       'assets/hero/1600/h19.jpg', bg=('.page-head', 'h19.jpg'))
  + page_head('assets/hero/1600/h19.jpg', 'Design Flow', '設計流程', '設計流程')
  + '''
<section class="sec">
  <div class="wrap-n">
    <div class="sec-head center">
      <p class="eyebrow center rv">Design Flow</p>
      <h2 class="h-sec rv rv-d1">六個階段</h2>
      <p class="lede rv rv-d2" style="text-align:center">每一步都會跟您確認、留下紀錄，您隨時都知道家走到哪裡了。</p>
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
       '易向室內設計（澤向室內裝修工程有限公司）台北公司：台北市南京東路二段137號14樓 02-2595-5535；桃園公司：桃園市桃園區經國路719號1樓 03-358-5835。加 LINE 免費初步諮詢。',
       'assets/hero/1600/h17.jpg', bg=('.page-head', 'h17.jpg'))
  + page_head('assets/hero/1600/h17.jpg', 'Contact', '聯絡我們', '聯絡我們')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Our Offices</p>
      <h2 class="h-sec rv rv-d1">台北 ・ 桃園 雙據點</h2>
      <p class="lede rv rv-d2" style="text-align:center">第一次聊聊不收費。加 LINE 或直接打電話來，我們都在。</p>
    </div>
    <div class="offices rv">
      <div class="office">
        <p class="k">Taipei Office</p>
        <h3>台北公司</h3>
        <dl>
          <dt>地址</dt><dd>台北市南京東路二段 137 號 14 樓</dd>
          <dt>電話</dt><dd><a href="tel:0225955535">02-2595-5535</a></dd>
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
        <figure class="office-fig">
          <img src="assets/office/taoyuan-700.jpg"
            srcset="assets/office/taoyuan-700.jpg 700w, assets/office/taoyuan.jpg 1200w"
            sizes="(max-width:720px) 92vw, 42vw" width="1200" height="900"
            alt="易向室內設計 桃園公司外觀，經國路 719 號" loading="lazy">
          <figcaption>桃園公司外觀</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>
''' + line_band('加 LINE 最快', '傳張平面圖或現況照片，我們會先給您初步方向。不用填表單、不用留電話。')
  + FOOT)

print('done.')

# ============================================================ 設計筆記（部落格）
# 內容依據：客戶既有的服務項目、設計流程、收費標準與 YouTube 影片主題。
# 沒有出現在客戶素材裡的具體案例、數字、承諾一律不寫。
POSTS = [
 dict(slug="blog-pre-sale-customization", date="2026-09-18", cat="客變設計", en="Pre-sale Customization",
  title="預售屋客變，交屋前最值得花的一次時間",
  excerpt="牆還沒砌、管線還沒埋，這時候改格局幾乎不用拆。客變能改什麼、什麼時候要決定、常見的三個取捨。",
  cover="assets/case/1200/hehui-05.jpg", cover_sm="assets/case/800/hehui-05.jpg",
  body='''
<p>買預售屋的人常以為裝潢是交屋之後的事。但有一個時間點，比交屋後任何一次裝修都划算，就是建商開放「客變」的那幾週。</p>
<h2>客變改的是還沒蓋出來的東西</h2>
<p>客變是在建商施工前，依住戶需求調整格局、水電位置與部分建材。牆還沒砌、管線還沒埋，改動幾乎不需要拆除。同樣一道牆，客變階段是「不要砌」，交屋後就是「打掉再補」，差的是拆除費、清運費、重做的工資，還有工期。</p>
<h2>通常能改的三類</h2>
<ul>
<li><strong>格局</strong>：非結構的隔間牆可以取消或移位。常見的是把封閉廚房打開成餐廚一體、兩房併成一大房。</li>
<li><strong>水電</strong>：插座、開關、給排水與冷氣排水的位置。這一項最容易被低估，交屋後想加一個插座，牆面就要重新切割修補。</li>
<li><strong>建材退換</strong>：建商標配的地磚、廚具、衛浴可以退掉折價，換成自己選的。</li>
</ul>
<h2>什麼時候要決定</h2>
<p>客變有期限，通常在結構體施工前，建商會通知一段時間讓住戶提交變更。這段時間往往只有幾週，而完整的客變需要先有平面規劃，才知道牆要不要動、插座要放哪裡。所以收到建商通知再開始找設計師，時間會非常趕。比較好的順序是簽約後就先討論，客變期一到直接提交。</p>
<h2>三個常見的取捨</h2>
<p><strong>退建材不一定划算。</strong>建商的折讓金額通常低於市價，退掉之後自己買不見得便宜，要算過再決定。</p>
<p><strong>開放式格局要顧到油煙與冷氣。</strong>餐廚打通很受歡迎，但抽油煙機的能力和冷氣的坪數配置要一起看。</p>
<p><strong>不要為了「以後可能」多留。</strong>每個位置都多留一組插座，牆面會很亂。依實際的家具配置決定，比憑想像保險。</p>
<p>易向的客變服務從平面規劃開始，會把水電點位與家具位置一起畫出來，再協助整理成建商要的變更文件。初步諮詢不收費，若您剛簽約，歡迎在客變期之前先聊聊。</p>
'''),
 dict(slug="blog-storage-entry-living-study", date="2026-09-10", cat="收納規劃", en="Storage Planning",
  title="玄關、客廳、書房：收納要先想動線，再想櫃子",
  excerpt="收納做不好，通常不是櫃子不夠，是東西放的位置跟人的動線對不上。從進門到坐下，三個空間的收納怎麼想。",
  cover="assets/hero/1600/h13.jpg", cover_sm="assets/hero/900/h13.jpg", video="AegVGxrSr7k",
  body='''
<p>很多人一提到收納就想到「多做幾個櫃子」。但實際住進去之後，最常出現的狀況是櫃子很多、東西還是堆在外面。問題通常不在容量，在位置。</p>
<h2>玄關：東西在哪裡脫，就在哪裡收</h2>
<p>進門的前三步會發生的事：脫鞋、放鑰匙、掛外套、放包。這四樣東西的收納若不在進門的動線上，就會落在最近的一張椅子上。玄關櫃的重點不是做多大，是鞋子有沒有地方換、常穿的那幾雙能不能不彎腰就拿到、鑰匙和包有沒有一個固定的平台。</p>
<p>如果玄關深度不夠，可以用一道矮櫃兼坐凳，或把鞋櫃做成懸空，下方留放常穿鞋的空間，視覺上也不會壓迫。</p>
<h2>客廳：先決定要藏什麼，再決定要露什麼</h2>
<p>客廳是全家共用的空間，收納的東西最雜：遙控器、充電線、小孩的玩具、雜誌、備用的抱枕毯子。全部關進櫃子，客廳會很冷；全部露出來，會很亂。</p>
<p>做法是分兩層。天天用、不好看的東西（線材、遙控器、玩具）進抽屜或有門的櫃體；願意讓人看到的東西（書、擺件、植物）放開放層架。電視櫃通常是最好的分界，下方封閉、上方開放。</p>
<h2>書房：桌面淨空靠的是牆面</h2>
<p>書房的收納要解決兩件事：書和文件的量，以及桌面能不能保持乾淨。書櫃做整面牆通常比做兩個獨立的櫃子有效率，也比較不會有零碎的畸零角。桌面則要有一個「暫放區」，不然文件會一直累積在桌上。</p>
<p>如果書房也是工作室或客房，收納要能把工作的東西完整收起來，空間才能切換。這種情況下有門的櫃子會比開放層架實用。</p>
<h2>從設計師自己的家看</h2>
<p>這集影片是易向設計師打開自己家的玄關、客廳與書房，逐一說明當初為什麼這樣規劃。實際住過的空間，比示範屋更能看出哪些收納真的有用。</p>
'''),
 dict(slug="blog-morandi-quiet-luxury", date="2026-09-02", cat="風格解析", en="Style Notes",
  title="莫蘭迪色的低調奢華：把彩度降下來，把質感放上去",
  excerpt="灰調的色彩為什麼耐看、怎麼跟石材與金屬搭配、以及莫蘭迪色最常被做壞的一種方式。",
  cover="assets/works/1200/cover-103.jpg", cover_sm="assets/works/800/cover-103.jpg", video="WYuW_FUWt28",
  body='''
<p>莫蘭迪色這幾年在住宅設計裡很常見。名字來自義大利畫家 Giorgio Morandi，他的靜物畫用的都是加了灰的色彩：灰粉、灰藍、灰綠、米灰。這些顏色彩度低、明度中等，彼此放在一起不會搶。</p>
<h2>為什麼耐看</h2>
<p>高彩度的顏色第一眼很吸引人，但天天看會累。低彩度的顏色沒有那個第一眼，卻能讓空間裡的其他東西被看見：木紋的走向、石材的紋理、光線在牆面上的變化。莫蘭迪色的作用是退到後面當背景，讓材質站到前面。</p>
<h2>跟材質怎麼搭</h2>
<p>因為顏色本身安靜，材質就要有表情。常見的搭法是：</p>
<ul>
<li><strong>石材</strong>：帶灰白紋理的大理石或石英石，跟灰調的牆面同一個色溫，紋理會變成主角。</li>
<li><strong>金屬</strong>：拉絲的鈦金或古銅，用在門框、櫃體收邊或燈具，份量要少，是點不是面。</li>
<li><strong>木質</strong>：偏灰或偏白的木皮比黃木好搭，避免色溫打架。</li>
<li><strong>布料</strong>：絨布、亞麻這類有毛面的材質，能讓低彩度的顏色有深淺變化。</li>
</ul>
<h2>最常被做壞的方式</h2>
<p>整個空間全部用同一個灰調，沒有明暗、沒有材質變化。結果不是低調，是平。莫蘭迪色需要對比才會立起來：淺灰牆配深色的櫃體、霧面的牆配亮面的石材、粉灰的沙發配一盞黑鐵的燈。彩度可以低，明暗差不能沒有。</p>
<h2>設計師專訪</h2>
<p>這集影片是易向設計師以一個實際完成的案子，說明莫蘭迪色在住宅裡怎麼配、材質怎麼選。</p>
'''),
]

def post_card(p_, n):
    return ('      <a class="post-card rv%s" href="%s.html">'
            '<div class="ph"><img src="%s" srcset="%s 800w, %s 1200w" sizes="(max-width:720px) 92vw, 46vw" alt="%s" loading="lazy"></div>'
            '<div class="post-meta"><span>%s</span><time datetime="%s">%s</time></div>'
            '<h2>%s</h2><p>%s</p><span class="more">閱讀全文　→</span></a>'
            % (' rv-d%d' % (n % 3) if n % 3 else '', p_['slug'], p_['cover_sm'], p_['cover_sm'], p_['cover'],
               p_['title'], p_['cat'], p_['date'], p_['date'].replace('-', '.'), p_['title'], p_['excerpt']))

write('blog.html',
  head('blog.html', f'設計筆記｜{SITE}',
       '易向室內設計（澤向室內裝修工程有限公司）的設計筆記：客變、收納、風格與居家規劃的實用觀點。',
       'assets/hero/1600/h21.jpg', bg=('.page-head', 'h21.jpg'))
  + page_head('assets/hero/h21.jpg', 'Blog', '設計筆記', '設計筆記')
  + '''
<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="eyebrow center rv">Journal</p>
      <h2 class="h-sec rv rv-d1">設計筆記</h2>
      <p class="lede rv rv-d2" style="text-align:center">把我們在案場與客戶討論時最常被問到的事，寫成一篇一篇的短文。</p>
    </div>
    <div class="post-grid">
''' + "\n".join(post_card(p_, n) for n, p_ in enumerate(POSTS)) + '''
    </div>
  </div>
</section>
''' + line_band() + FOOT)

for n, p_ in enumerate(POSTS):
    others = [q for q in POSTS if q is not p_][:2]
    video = ('''
    <div class="post-video"><div class="vid-fr"><iframe src="https://www.youtube.com/embed/%s" title="%s"
      loading="lazy" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe></div></div>
''' % (p_['video'], p_['title'])) if p_.get('video') else ''
    write(p_['slug'] + '.html',
      head(p_['slug'] + '.html', f"{p_['title']}｜{SITE}", p_['excerpt'], p_['cover'])
      + '''
<article class="post">
  <header class="post-head">
    <div class="wrap-n">
      <p class="crumb rv in"><a href="index.html">首頁</a> ／ <a href="blog.html">設計筆記</a> ／ %s</p>
      <p class="eyebrow rv in rv-d1">%s</p>
      <h1 class="rv in rv-d2">%s</h1>
      <p class="post-meta rv in rv-d3"><time datetime="%s">%s</time><span>易向室內設計｜澤向室內裝修工程有限公司</span></p>
    </div>
  </header>
  <figure class="post-cover rv in">
    <img src="%s" srcset="%s 800w, %s 1200w" sizes="(max-width:1080px) 100vw, 1080px" alt="%s" fetchpriority="high">
  </figure>
  <div class="wrap-n post-body">
%s%s
  </div>
</article>

<section class="sec sec-alt">
  <div class="wrap">
    <p class="eyebrow rv">More</p>
    <h2 class="h-sec rv rv-d1">其他筆記</h2>
    <div class="post-grid">
%s
    </div>
  </div>
</section>
''' % (p_['cat'], p_['en'], p_['title'], p_['date'], p_['date'].replace('-', '.'),
       p_['cover_sm'], p_['cover_sm'], p_['cover'], p_['title'], p_['body'], video,
       "\n".join(post_card(q, i) for i, q in enumerate(others)))
      + line_band() + FOOT)
