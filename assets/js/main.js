/* 易向室內設計 — 前端互動 */
(function () {
  'use strict';
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var CFG = window.SITE_CONFIG || {};

  /* ---- LINE 連結：全站統一由設定檔灌入 ---- */
  (function line() {
    var url = (CFG.lineUrl || '').trim();
    var tel = 'tel:' + (CFG.fallbackTel || '');
    $$('[data-line]').forEach(function (a) {
      if (url) {
        a.href = url;
      } else {
        /* 尚未設定 LINE：改成撥打電話，避免死連結 */
        a.href = tel;
        a.removeAttribute('target');
        a.classList.add('no-line');
      }
    });
    if (CFG.lineId) $$('[data-line-id]').forEach(function (e) { e.textContent = CFG.lineId; });
    if (!url) $$('.line-box').forEach(function (b) {
      var p = document.createElement('p');
      p.className = 'line-note';
      p.textContent = '※ 官方 LINE 連結尚未設定，按鈕暫時改為撥打電話。設定方式見 assets/js/config.js。';
      b.appendChild(p);
    });
  })();

  /* ---- 頁首 ---- */
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
    var setMenu = function (on) {
      nav.classList.toggle('open', on);
      burger.classList.toggle('x', on);
      if (head) head.classList.toggle('nav-open', on);
      document.body.style.overflow = on ? 'hidden' : '';
      burger.setAttribute('aria-expanded', on ? 'true' : 'false');
    };
    burger.setAttribute('aria-expanded', 'false');
    burger.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) setMenu(false);
    });
  }

  /* ---- 進場動畫 ---- */
  var io = 'IntersectionObserver' in window
    ? new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' })
    : null;
  var reveal = function (root) {
    $$('.rv', root || document).forEach(function (el) { if (io) io.observe(el); else el.classList.add('in'); });
  };
  reveal();

  /* 手機判斷用 innerWidth，不用 matchMedia —— 某些內嵌／模擬環境下
     兩者量到的寬度不一致，innerWidth 才是實際排版寬度。 */
  var isSmall = function () { return (window.innerWidth || 1200) <= 720; };

  /* ---- 首屏輪播：第一張直接載入，其餘等閒置再抓 ---- */
  var bg = $('.hero-bg');
  if (bg) {
    var figs = $$('figure', bg), i = 0;
    /* 手機只輪播兩張：每張約 90KB，四張在行動網路上不值得 */
    if (isSmall() && figs.length > 2) {
      figs.slice(2).forEach(function (f) { f.remove(); });
      figs = figs.slice(0, 2);
    }
    var start = function () {
      /* 行內樣式的相對路徑以文件為基準，不會踩到 CSS 變數的解析陷阱 */
      var dir = isSmall() ? 'assets/hero/900/' : 'assets/hero/1600/';
      figs.forEach(function (f) {
        if (f.dataset.bg) f.style.backgroundImage = 'url(' + dir + f.dataset.bg + ')';
      });
      if (figs.length > 1) setInterval(function () {
        figs[i].classList.remove('on');
        i = (i + 1) % figs.length;
        figs[i].classList.add('on');
      }, 6200);
    };
    if (figs.length > 1) {
      if (window.requestIdleCallback) requestIdleCallback(start, { timeout: 2500 });
      else setTimeout(start, 1600);
    }
  }

  /* ---- 作品資料 ---- */
  var DATA = null;
  var load = function (cb) {
    if (DATA) return cb(DATA);
    fetch('data/works.json').then(function (r) { return r.json(); })
      .then(function (d) { DATA = d; cb(d); })
      .catch(function () { cb({ categories: [], works: [] }); });
  };

  /* 由 1600px 原圖推導出 400/800/1200 三階。
     格線刻意不提供 1600 —— 視網膜螢幕上 30vw×2≈840px，若最大階只有 800
     瀏覽器會直接跳去抓 1600 原圖（約 300KB）。1200 這一階就是為了補這個斷層。
     原圖只留給燈箱在使用者點開時才載入。 */
  function srcset(img) {
    var f = img.split('/').pop();
    var dir = img.slice(0, img.length - f.length);
    return {
      s800: dir + '800/' + f,
      set: dir + '400/' + f + ' 400w, ' + dir + '800/' + f + ' 800w, ' + dir + '1200/' + f + ' 1200w'
    };
  }

    /* 略為保守地宣告尺寸：桌機視網膜下 28vw×2≈784px 會落在 800 這一階，
     若照實寫 30vw 會變成 840px 而跳去抓 1200，多花近一倍流量卻看不出差別。 */
  var SIZES = '(max-width:720px) 92vw, (max-width:1080px) 46vw, 28vw';

  function cardHTML(w, cls, eager) {
    var v = srcset(w.img);
    return '<a class="card ' + cls + ' rv" href="#" data-id="' + w.id + '">' +
             '<div class="ph"><img src="' + v.s800 + '" srcset="' + v.set + '" sizes="' + SIZES + '"' +
               ' alt="' + w.title + '｜' + w.catName + '"' +
               (eager ? '' : ' loading="lazy"') + ' decoding="async"></div>' +
             '<div class="card-txt">' +
               '<p class="k">' + w.catEn + '</p><h3>' + w.title + '</h3>' +
               '<p class="m">' + w.catName + '</p>' +
             '</div></a>';
  }

  /* ---- 首頁精選 ---- */
  var feat = $('#featured');
  if (feat) {
    var rhythm = ['g-a', 'g-b', 'g-c', 'g-d', 'g-e', 'g-e'];
    load(function (d) {
      var list = d.works.filter(function (w) { return w.featured; }).slice(0, 6);
      feat.innerHTML = list.map(function (w, n) {
        return cardHTML(w, rhythm[n % rhythm.length] + (n > 1 ? ' rv-d' + ((n % 3) + 1) : ''), n < 2);
      }).join('');
      reveal(feat); bindCards(feat, list);
    });
  }

  /* ---- 作品總覽：篩選 + 分頁 ---- */
  var all = $('#allworks'), filters = $('#filters'), pager = $('#pager');
  var PER = 12;
  if (all) {
    load(function (d) {
      var cat = 'all', page = 1, list = [];

      if (filters) {
        filters.innerHTML =
          '<button class="on" data-c="all"><span class="en">All</span>全部作品</button>' +
          d.categories.map(function (c) {
            return '<button data-c="' + c.slug + '"><span class="en">' + c.en + '</span>' + c.name + '</button>';
          }).join('');
      }

      function draw() {
        list = cat === 'all' ? d.works : d.works.filter(function (w) { return w.cat === cat; });
        var pages = Math.max(1, Math.ceil(list.length / PER));
        if (page > pages) page = pages;
        var slice = list.slice((page - 1) * PER, page * PER);

        all.innerHTML = slice.map(function (w, n) {
          return cardHTML(w, 'g-w' + (n % 3 ? ' rv-d' + (n % 3) : ''), n < 3);
        }).join('');
        /* 燈箱吃整個篩選結果，不只這一頁：點一張就能往下滑完同類全部 */
        reveal(all); bindCards(all, list);

        var t = $('#wtitle');
        if (t) {
          var c = null;
          for (var k = 0; k < d.categories.length; k++) if (d.categories[k].slug === cat) c = d.categories[k];
          t.textContent = c ? c.name : '完工實績';
        }
        drawPager(pages);
      }

      function drawPager(pages) {
        if (!pager) return;
        if (pages < 2) { pager.innerHTML = ''; return; }
        var h = '<button class="pg-arrow" data-p="' + (page - 1) + '"' +
                (page === 1 ? ' disabled' : '') + ' aria-label="上一頁"></button>';
        for (var p = 1; p <= pages; p++) {
          h += '<button class="pg-n' + (p === page ? ' on' : '') + '" data-p="' + p + '">' + p + '</button>';
        }
        h += '<button class="pg-arrow next" data-p="' + (page + 1) + '"' +
             (page === pages ? ' disabled' : '') + ' aria-label="下一頁"></button>';
        pager.innerHTML = h;
      }

      draw();

      if (filters) filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); cat = b.dataset.c; page = 1; draw();
      });

      if (pager) pager.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b || b.disabled) return;
        page = +b.dataset.p; draw();
        var top = all.getBoundingClientRect().top + window.scrollY - 120;
        window.scrollTo({ top: top, behavior: 'smooth' });
      });
    });
  }

  /* ---- 精選案例：四種風格分類（靜態卡片，前端只做顯示切換） ---- */
  var cf = $('#cfilters'), cg = $('#casegrid');
  if (cf && cg) cf.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    $$('button', cf).forEach(function (x) { x.classList.remove('on'); });
    b.classList.add('on');
    var c = b.dataset.c;
    $$('.card', cg).forEach(function (k) {
      var on = c === 'all' || (' ' + (k.dataset.cat || '') + ' ').indexOf(' ' + c + ' ') >= 0;
      k.classList.toggle('hide', !on);
      if (on) k.classList.add('in');
    });
    var t = $('#ctitle'); if (t) t.textContent = b.dataset.name || '完整案例';
    var l = $('#clede'); if (l) l.textContent = b.dataset.desc || l.dataset.default || '';
  });

  /* ---- 精選案例圖庫：HTML 已靜態輸出，這裡只接燈箱 ---- */
  $$('[data-lightbox]').forEach(function (root) {
    var list = $$('.card[data-full]', root).map(function (a, n) {
      return { id: 'g' + n, img: a.dataset.full, title: a.dataset.title.split('｜')[0],
               catName: a.dataset.title.split('｜')[1] || '', catEn: 'Case Study' };
    });
    $$('.card[data-full]', root).forEach(function (a, n) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(list, 'g' + n); });
    });
  });

  /* ---- 燈箱：從點到的那張開始，直向排到底，一口氣往下滑 ---- */
  var lb = $('#lb'), lbCol = $('#lbCol');

  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function open(list, id) {
    if (!lb || !lbCol) return;
    var n = 0; for (var j = 0; j < list.length; j++) if (list[j].id === id) { n = j; break; }
    var order = list.slice(n).concat(list.slice(0, n));
    var last = null;
    lbCol.innerHTML = order.map(function (w, i) {
      var h = '';
      if (w.catName && w.catName !== last) { h = '<h3 class="lb-h">' + esc(w.catName) + '</h3>'; last = w.catName; }
      return h + '<figure><img src="' + w.img + '" alt="' + esc(w.title) + '"' +
             (i < 2 ? '' : ' loading="lazy"') + ' decoding="async">' +
             '<figcaption><p class="k">' + esc(w.catEn) + '</p><h3>' + esc(w.title) +
             (w.catName ? '｜' + esc(w.catName) : '') + '</h3></figcaption></figure>';
    }).join('');
    lb.scrollTop = 0;
    lb.classList.add('on'); document.body.style.overflow = 'hidden';
  }
  var close = function () {
    lb.classList.remove('on'); document.body.style.overflow = '';
    lbCol.innerHTML = '';
  };

  function bindCards(root, list) {
    $$('.card', root).forEach(function (c) {
      c.addEventListener('click', function (e) { e.preventDefault(); open(list, c.dataset.id); });
    });
  }

  if (lb) {
    $('#lbX').addEventListener('click', close);
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lbCol) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.classList.contains('on') && e.key === 'Escape') close();
    });
  }
})();
