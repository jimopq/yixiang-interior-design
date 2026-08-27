# 易向室內設計 — 官網改版（設計提案版）

繁體中文靜態網站。內容、圖片與品牌識別皆取自客戶既有素材：
舊官網 `www.image.net.tw` 與客戶提供的提案簡報 PDF。

---

## 檔案結構

```
image-design-web/
├─ index.html            首頁（首屏／理念／精選作品／案例導引／獎項／LINE）
├─ about.html            關於易向（理念、數字、國際獎項、媒體專訪影片）
├─ works.html            作品總覽（86 件・五類篩選・每頁 12 件分頁・燈箱）
├─ case.html             精選案例 合輝大璽（規格、設計概念、14 張圖庫）
├─ service.html          服務項目與收費標準
├─ process.html          設計流程（六階段）
├─ contact.html          雙據點資訊、LINE、地圖
├─ build.py              ★ 頁面產生器。改版型、改文案都動這支，然後 python3 build.py
├─ data/works.json       ★ 作品資料。新增案子只改這個檔
├─ tools/
│  ├─ make-thumbs.sh     ★ 產生多尺寸縮圖
│  └─ gmail-form-endpoint.gs  （保留備用，目前表單已改為 LINE 導流）
└─ assets/
   ├─ css/style.css      設計系統（單一檔案）
   ├─ js/config.js       ★ 上線設定：LINE 連結
   ├─ js/main.js         互動（選單、輪播、篩選、分頁、燈箱、LINE 灌入）
   ├─ brand/             Logo 與獎項標章
   ├─ hero/  900｜1600   主視覺（首屏與各頁頁首）
   ├─ case/  800｜1200   精選案例圖庫（主目錄 1600 供燈箱）
   └─ works/ 400｜800｜1200  作品封面（主目錄 1600 供燈箱）
```

**所有頁面都由 `build.py` 產生**，頁首、頁尾、導覽列、LINE 區塊只有一份定義。
不要直接改 .html —— 下次跑 build.py 會被蓋掉。

## 本機預覽

`data/works.json` 是用 `fetch` 讀的，直接雙擊 HTML（`file://`）會被瀏覽器擋下。
請用簡易伺服器開啟：

```bash
cd image-design-web && python3 -m http.server 8899
```

然後開 http://localhost:8899

## 設計依據

參考客戶指定的三個網站（揚楊設計、甘丹設計、木寓設計），
歸納出台灣高端設計公司官網的共同語言，並套用到易向的素材上：

1. **英文小標 + 中文主標並置** — 英文是拉開字距的小級數大寫，中文才是真正的標題。三站皆然。
2. **中文字距拉開**（標題 0.16–0.3em）— 這是這類網站最明顯的特徵，歐美模板直接套中文會完全沒有這個味道。
3. **全幅首屏 + 極簡疊字標語，外加一道細框**
4. **獨立的獎項區塊** — 三站都有，易向的國際獎項是強項卻在舊站被藏起來。
5. **作品命名詩意化** — 易向本來就有這個資產（沈博絕麗、步月登雲、月明如晝）。
6. **大量留白 + 極細分隔線 + 近乎無彩度的暖調紙感**

**易向的差異化：品牌紫 `#402063`**（取樣自客戶 Logo）。
三個參考站都是無彩度灰／米白，易向保留紫色但只用在極少量標記
（小標、細線、hover、按鈕），維持同一種克制感的同時保有品牌識別。
獎項區另用金色 `#A6874F`，對應簡報中獎項看板的既有用色。

## 字體

- 中文標題：**Noto Serif TC**（思源宋體）— 開源可商用
- 中文內文：**Noto Sans TC**（思源黑體）— 開源可商用
- 英文展示：**Cormorant Garamond**

三者皆為 Google Fonts，可商用、免授權費。

## 上線前待辦

| 項目 | 說明 |
|---|---|
| **作品原圖** | 舊官網部分作品圖中央有客戶自己加的浮水印，放大後明顯。需向客戶索取無浮水印原檔替換 |
| ~~表單收信~~ | ✅ 程式已完成。到 `assets/js/config.js` 填入收信端即可啟用（見下方三個方案） |
| **影片標題核對** | 四支 YouTube 影片已依縮圖內容對應，建議請客戶再確認一次 |
| **作品分類資料** | 目前每件作品只有「案名 + 風格分類」。若能補上地區、坪數、年份、設計概念（如旗艦案例「合輝大璽」的規格），質感會再上一階 |
| **網域與部署** | 建議 Cloudflare Pages，綁定現有網域 image.net.tw |

## 分支

| 分支 | 用途 |
|---|---|
| `main` | **正式版**。robots.txt 允許索引、含 sitemap，給 Cloudflare Pages 用 |
| `preview` | **提案預覽版**。全站 `noindex,nofollow` + robots.txt Disallow，給 GitHub Pages 用 |

預覽網址：https://jimopq.github.io/yixiang-interior-design/

`preview` 加了 noindex 是為了避免預覽站被搜尋引擎索引，與客戶正式站
image.net.tw 內容重複而互相稀釋排名。

**不要把 `preview` 合併回 `main`** —— 那會把 noindex 帶進正式站。
要更新預覽站，方向是相反的：

```bash
git checkout preview && git merge main && git push && git checkout main
```

客戶確認後、正式站上線時，可以直接刪掉 `preview` 分支並把 repo 轉回私有：

```bash
gh repo edit --visibility private --accept-visibility-change-consequences
```

## 部署（Cloudflare Pages）

程式碼已在私有 repo：**https://github.com/jimopq/yixiang-interior-design**

1. Cloudflare Dashboard → **Workers & Pages** → Create → **Pages** → Connect to Git
2. 授權 GitHub，選 `yixiang-interior-design`
3. 設定：
   - Framework preset：**None**
   - Build command：**留空**
   - Build output directory：**`/`**
4. Save and Deploy，約一分鐘後會拿到 `xxx.pages.dev` 網址
5. 確認沒問題後 → Custom domains → 綁 `www.image.net.tw`

之後只要 `git push`，Cloudflare 會自動重新部署。

### 已內含的上線設定

| 檔案 | 作用 |
|---|---|
| `_headers` | 靜態資源長快取、HTML 即時更新、基本安全標頭 |
| `_redirects` | 舊 Joomla 網址 301 導向新頁面，保住既有 SEO 排名 |
| `robots.txt` / `sitemap.xml` | 搜尋引擎索引 |


---

## LINE 設定

網站的名單收集已改為**直接導向 LINE 官方帳號**，不再使用表單。
頁首按鈕、每頁底部的 CTA 區塊、頁尾連結、手機底部固定列，全部吃同一個設定值。

在 `assets/js/config.js`：

```js
lineUrl: '',   // 例：https://lin.ee/xxxxxxx
lineId: '',    // 顯示用文字，例：@image-design
```

`lineUrl` 從 LINE Official Account Manager →「增加好友人數」取得。

**留空也不會壞**：所有 LINE 按鈕會自動改成撥打電話（`fallbackTel`），
並在 CTA 區塊下方顯示一行設定提醒。設定好之後提醒會自己消失。

---

## 圖片

這是這個站最重的部分，所以做了多尺寸切換。

| 用途 | 尺寸 | 說明 |
|---|---|---|
| 格線縮圖 | 400 / 800 / 1200 | 由 `srcset` 交給瀏覽器依螢幕與 DPR 挑 |
| 頁首／首屏大圖 | 900 / 1600 | 手機吃 900，桌機吃 1600 |
| 燈箱 | 1600（主目錄） | 使用者點開才載入 |

**新增作品的流程：**

1. 把原圖丟進 `assets/works/`，命名 `cover-<id>.jpg`
2. 執行 `bash tools/make-thumbs.sh`
3. 在 `data/works.json` 的 `works` 陣列加一筆
4. `python3 build.py`

### 兩個踩過的坑，改動時要注意

**srcset 的階梯不能有斷層。** 桌機視網膜下卡片是 409px、DPR 2，需要約 818px。
若最大階只到 800，瀏覽器會直接跳去抓 1600 原圖（約 300KB／張）。
`sizes` 宣告成 28vw 讓它落在 800 這一階，實測初始載入從 1804KB 降到 387KB。

**CSS 自訂屬性裡的相對路徑，是相對於 CSS 檔而不是 HTML。**
把 `--bg:url(assets/hero/...)` 寫在 HTML、在 `assets/css/style.css` 裡用 `var(--bg)`，
瀏覽器會解析成 `/assets/css/assets/hero/...` 而整個主視覺變黑。
所以頁首背景改用 `build.py` 寫進 HTML `<head>` 的 `<style>` 區塊。
