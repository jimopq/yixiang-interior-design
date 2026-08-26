/**
 * 易向室內設計 — 官網諮詢表單收信後端
 * 用 Google Apps Script 當表單的收信端，不需要任何第三方服務或帳號。
 *
 * ── 部署步驟（約 2 分鐘）─────────────────────────────────────────
 *  1. 開 https://script.google.com  →  新專案
 *  2. 把這整個檔案的內容貼進去，覆蓋原本的 myFunction
 *  3. 改下面的 TO（要收信的信箱）
 *  4. 右上角「部署」→「新增部署作業」
 *       類型：網頁應用程式
 *       執行身分：我
 *       誰可以存取：★ 任何人 ★（這項一定要選，否則網站呼叫不到）
 *  5. 按「部署」，第一次會要求授權 → 允許
 *  6. 複製它給的「網頁應用程式網址」
 *       （形如 https://script.google.com/macros/s/AKfy..../exec）
 *  7. 貼到 assets/js/config.js 的 appsScriptUrl
 * ────────────────────────────────────────────────────────────
 *
 * 額度：一般 Gmail 帳號每天 100 封，遠超過官網詢問量。
 */

/** 收件人（可用逗號分隔多個信箱） */
var TO = 'f27920903@gmail.com';

/** 信件主旨前綴 */
var SUBJECT_PREFIX = '【官網諮詢】易向室內設計';

/** 欄位順序與中文名稱 */
var FIELDS = [
  ['name',    '姓名'],
  ['tel',     '聯絡電話'],
  ['email',   'Email'],
  ['type',    '需求類型'],
  ['area',    '坪數'],
  ['city',    '房屋所在地'],
  ['message', '需求說明']
];

function doPost(e) {
  try {
    var d = {};
    if (e && e.postData && e.postData.contents) {
      d = JSON.parse(e.postData.contents);
    }

    /* 蜜罐：真人看不到這欄，被填了就當機器人，安靜丟棄 */
    if (d.company) return json({ success: true });

    if (!String(d.name || '').trim() && !String(d.tel || '').trim()) {
      return json({ success: false, message: '缺少必要欄位' });
    }

    var lines = FIELDS.map(function (f) {
      return f[1] + '：' + (String(d[f[0]] || '').trim() || '—');
    });

    lines.push('');
    lines.push('──────────────');
    lines.push('送出時間：' + Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy/MM/dd HH:mm:ss'));
    lines.push('來源：' + (d._page || '官網諮詢表單'));

    var name = String(d.name || '').trim() || '訪客';

    var opts = {
      to: TO,
      subject: SUBJECT_PREFIX + '｜' + name,
      body: lines.join('\n'),
      name: '易向室內設計官網'
    };
    /* 客戶有留 Email 的話，直接在信件裡按「回覆」就能回給他 */
    if (isEmail(d.email)) opts.replyTo = String(d.email).trim();

    MailApp.sendEmail(opts);

    return json({ success: true });

  } catch (err) {
    return json({ success: false, message: String(err) });
  }
}

/** 讓人可以用瀏覽器打開網址確認部署成功 */
function doGet() {
  return json({ success: true, message: '易向室內設計表單收信端運作中' });
}

function isEmail(v) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(v || '').trim());
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
