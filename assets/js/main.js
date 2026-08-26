/* 易向室內設計 — 前端互動 */
(function () {
  'use strict';
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- 頁首：捲動後轉為紙底 ---- */
  var head = $('.site-head');
  if (head) {
    var hero = $('.hero') || $('.page-head');
    var solid = function () {
      var trip = hero ? Math.min(hero.offsetHeight - 90, window.innerHeight * 0.72) : 40;
      head.classList.toggle('solid', window.scrollY > trip);
    };
    solid();
    window.addEventListener('scroll', solid, { passive: true });
    window.addEventListener('resize', solid);
  }

  /* ---- 行動選單 ---- */
  var burger = $('.burger'), nav = $('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.classList.toggle('x', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open'); burger.classList.remove('x');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---- 進場動畫 ---- */
  var io = 'IntersectionObserver' in window
    ? new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' })
    : null;
  var reveal = function (root) {
    $$('.rv', root || document).forEach(function (el) {
      if (io) io.observe(el); else el.classList.add('in');
    });
  };
  reveal();

  /* ---- 首屏輪播 ---- */
  var bg = $('.hero-bg');
  if (bg) {
    var figs = $$('figure', bg), i = 0;
    if (figs.length) {
      figs[0].classList.add('on');
      if (figs.length > 1) setInterval(function () {
        figs[i].classList.remove('on');
        i = (i + 1) % figs.length;
        figs[i].classList.add('on');
      }, 6200);
    }
  }

  /* ---- 作品資料 ---- */
  var DATA = null;
  var load = function (cb) {
    if (DATA) return cb(DATA);
    fetch('data/works.json')
      .then(function (r) { return r.json(); })
      .then(function (d) { DATA = d; cb(d); })
      .catch(function () { cb({ categories: [], works: [] }); });
  };

  var cardHTML = function (w, cls, lazy) {
    return '<a class="card ' + cls + ' rv" href="#" data-id="' + w.id + '">' +
             '<div class="ph"><img src="' + w.img + '" alt="' + w.title + '｜' + w.catName + '"' +
             (lazy ? ' loading="lazy"' : '') + ' decoding="async"></div>' +
             '<div class="card-txt">' +
               '<p class="k">' + w.catEn + '</p>' +
               '<h3>' + w.title + '</h3>' +
               '<p class="m">' + w.catName + '</p>' +
             '</div>' +
           '</a>';
  };

  /* ---- 首頁精選（刻意不等分的版面節奏） ---- */
  var feat = $('#featured');
  if (feat) {
    var rhythm = ['g-a', 'g-b', 'g-c', 'g-d', 'g-e', 'g-e', 'g-d', 'g-c'];
    load(function (d) {
      var list = d.works.filter(function (w) { return w.featured; }).slice(0, 8);
      feat.innerHTML = list.map(function (w, n) {
        return cardHTML(w, rhythm[n % rhythm.length] + (n > 1 ? ' rv-d' + ((n % 3) + 1) : ''), n > 2);
      }).join('');
      reveal(feat); bindCards(feat, list);
    });
  }

  /* ---- 作品總覽 ---- */
  var all = $('#allworks'), filters = $('#filters');
  if (all) {
    load(function (d) {
      if (filters) {
        filters.innerHTML =
          '<button class="on" data-c="all"><span class="en">All</span>全部作品</button>' +
          d.categories.map(function (c) {
            return '<button data-c="' + c.slug + '"><span class="en">' + c.en + '</span>' + c.name + '</button>';
          }).join('');
      }
      var draw = function (c) {
        var list = c === 'all' ? d.works : d.works.filter(function (w) { return w.cat === c; });
        all.innerHTML = list.map(function (w, n) { return cardHTML(w, 'g-w' + (n % 3 ? ' rv-d' + (n % 3) : ''), n > 5); }).join('');
        reveal(all); bindCards(all, list);
        var n = $('#wcount'); if (n) n.textContent = list.length;
      };
      draw('all');
      if (filters) filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); draw(b.dataset.c);
      });
    });
  }


  /* ---- 旗艦案例圖庫 ---- */
  var strip = $('#caseStrip');
  if (strip) {
    load(function (d) {
      var f = d.flagship; if (!f) return;
      var g = f.gallery.map(function (src, n) {
        return { id: 'c' + n, img: src, title: f.name, catName: f.sub, catEn: 'Featured Project' };
      });
      strip.innerHTML = g.slice(0, 14).map(function (w, n) {
        return '<button data-n="' + n + '" aria-label="' + f.name + ' 第 ' + (n + 1) + ' 張">' +
               '<img src="' + w.img + '" alt="' + f.name + '" loading="lazy"></button>';
      }).join('');
      strip.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        open(g, g[+b.dataset.n].id);
      });
      var z = $('#caseZoom');
      if (z) z.addEventListener('click', function () { open(g, g[0].id); });
    });
  }

  /* ---- 燈箱 ---- */
  var lb = $('#lb'), lbImg = $('#lbImg'), lbK = $('#lbK'), lbT = $('#lbT');
  var pool = [], cur = 0;

  var show = function (n) {
    if (!pool.length) return;
    cur = (n + pool.length) % pool.length;
    var w = pool[cur];
    lbImg.src = w.img; lbImg.alt = w.title;
    lbK.textContent = w.catEn; lbT.textContent = w.title + '｜' + w.catName;
  };
  function open(list, id) {
    pool = list;
    var n = 0; for (var j = 0; j < list.length; j++) if (list[j].id === id) { n = j; break; }
    show(n); lb.classList.add('on'); document.body.style.overflow = 'hidden';
  }
  var close = function () { lb.classList.remove('on'); document.body.style.overflow = ''; lbImg.src = ''; };

  function bindCards(root, list) {
    $$('.card', root).forEach(function (c) {
      c.addEventListener('click', function (e) { e.preventDefault(); open(list, c.dataset.id); });
    });
  }

  if (lb) {
    $('#lbX').addEventListener('click', close);
    $('#lbPrev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
    $('#lbNext').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  /* ---- 諮詢表單 ---- */
  var CFG = window.SITE_CONFIG || {};
  var form = $('#enquiry');

  var LABEL = { name:'姓名', tel:'聯絡電話', email:'Email', type:'需求類型',
                area:'坪數', city:'房屋所在地', message:'需求說明' };

  function fieldOf(el) { return el.closest('.field'); }

  function setErr(el, msg) {
    var f = fieldOf(el); if (!f) return;
    var m = $('.msg', f);
    if (!m) { m = document.createElement('p'); m.className = 'msg'; f.appendChild(m); }
    m.textContent = msg || '';
    f.classList.toggle('err', !!msg);
    el.setAttribute('aria-invalid', msg ? 'true' : 'false');
  }

  function validate() {
    var bad = null;
    var name = $('#f-name'), tel = $('#f-tel'), mail = $('#f-mail');
    [name, tel, mail].forEach(function (el) { if (el) setErr(el, ''); });

    if (name && !name.value.trim()) { setErr(name, '請留下您的稱呼'); bad = bad || name; }
    var t = tel ? tel.value.replace(/[\s()-]/g, '') : '';
    if (tel && !t) { setErr(tel, '請留下聯絡電話'); bad = bad || tel; }
    else if (tel && !/^\+?\d{8,15}$/.test(t)) { setErr(tel, '電話格式看起來不太對，請再確認'); bad = bad || tel; }
    if (mail && mail.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.value.trim())) {
      setErr(mail, 'Email 格式看起來不太對'); bad = bad || mail;
    }
    return bad;
  }

  function collect() {
    var d = {};
    ['name','tel','email','type','area','city','message'].forEach(function (k) {
      var el = form.elements[k];
      if (el) d[k] = (el.value || '').trim();
    });
    return d;
  }

  /* 沒設定收信服務時的退路：開啟郵件軟體並帶入所有欄位 */
  function mailtoFallback(d) {
    var body = Object.keys(LABEL).map(function (k) {
      return LABEL[k] + '：' + (d[k] || '—');
    }).join('\n') + '\n\n— 由官網諮詢表單送出';
    var url = 'mailto:' + (CFG.contactEmail || '') +
      '?subject=' + encodeURIComponent((CFG.mailSubject || '官網諮詢') + '｜' + (d.name || '')) +
      '&body=' + encodeURIComponent(body);
    window.location.href = url;
  }

  function done(msg, sub) {
    var box = document.createElement('div');
    box.className = 'form-done';
    box.innerHTML = '<p class="k">Thank You</p><h3>' + msg + '</h3><p>' + sub + '</p>';
    form.replaceWith(box);
  }

  if (form) {
    /* 未設定收信服務時，顯示提醒（設定好之後這行會自動消失） */
    var hint = $('#formHint');
    if (hint && !CFG.appsScriptUrl && !CFG.web3formsKey && !CFG.formspreeUrl) {
      hint.textContent = '※ 目前尚未接上收信服務，按下送出會改為開啟您的郵件軟體。'
                       + '設定方式見 assets/js/config.js。';
    }

    form.addEventListener('input', function (e) {
      if (fieldOf(e.target) && fieldOf(e.target).classList.contains('err')) setErr(e.target, '');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      /* 蜜罐：真人看不到這個欄位，被填了就是機器人 */
      if (form.elements.company && form.elements.company.value) return;

      var bad = validate();
      if (bad) { bad.focus(); return; }

      var d = collect();
      var btn = $('button[type=submit]', form);
      var lbl = $('span', btn) || btn;
      var old = lbl.textContent;

      if (!CFG.appsScriptUrl && !CFG.web3formsKey && !CFG.formspreeUrl) {
        mailtoFallback(d); return;
      }

      var url, payload, headers = { 'Accept': 'application/json' };
      if (CFG.appsScriptUrl) {
        url = CFG.appsScriptUrl;
        payload = JSON.stringify(Object.assign({ _page: location.pathname }, d));
        /* Apps Script 不處理 CORS preflight，用 text/plain 讓它維持
           「簡單請求」，瀏覽器就不會先送 OPTIONS。doPost 一樣讀得到內容。 */
        headers['Content-Type'] = 'text/plain;charset=utf-8';
      } else if (CFG.web3formsKey) {
        url = 'https://api.web3forms.com/submit';
        payload = JSON.stringify(Object.assign({
          access_key: CFG.web3formsKey,
          subject: (CFG.mailSubject || '官網諮詢') + '｜' + d.name,
          from_name: '易向室內設計官網',
          botcheck: ''
        }, d));
        headers['Content-Type'] = 'application/json';
      } else {
        url = CFG.formspreeUrl;
        payload = JSON.stringify(d);
        headers['Content-Type'] = 'application/json';
      }

      btn.disabled = true; lbl.textContent = '傳送中…';

      fetch(url, { method: 'POST', headers: headers, body: payload })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (j) {
            if (!r.ok || j.success === false) {
              var e = new Error(j.message || ('HTTP ' + r.status)); e.api = true; throw e;
            }
            return j;
          });
        })
        .then(function () {
          done('已收到您的諮詢', '我們會在一個工作天內與您聯繫。若急件請直接來電 03-358-5835。');
        })
        .catch(function (err) {
          /* 設定錯誤時留線索給維護的人，但不干擾訪客 */
          if (window.console) console.warn('[表單] 送出失敗：' + err.message);

          btn.disabled = false; lbl.textContent = old;

          /* 保險：詢問內容絕不因為設定失誤而消失，一鍵改用郵件送出 */
          var h = $('#formHint');
          if (h) {
            h.innerHTML = '※ 系統送出失敗，但您填的內容都還在。'
              + '<button type="button" class="link" id="mailFB">改用郵件寄出</button>'
              + '，或直接來電 <a href="tel:0333585835">03-358-5835</a>。';
            var fb = $('#mailFB', h);
            if (fb) fb.addEventListener('click', function () { mailtoFallback(collect()); });
          }
        });
    });
  }
})();
