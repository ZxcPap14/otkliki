import json, pathlib

d = pathlib.Path(__file__).parent
data = json.loads((d / "data.json").read_text(encoding="utf-8"))

HTML = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Отклики — Денис Казанцев</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0d1117;color:#e6edf3;font:15px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
header{padding:22px 18px 14px;border-bottom:1px solid #21262d;position:sticky;top:0;background:#0d1117;z-index:2}
h1{margin:0 0 4px;font-size:19px;font-weight:650}
.sub{color:#8b949e;font-size:13px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 10px}
.stat{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:7px 11px;font-size:13px}
.stat b{font-size:17px;display:block;font-variant-numeric:tabular-nums}
.filters{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
button{cursor:pointer;font:inherit;font-size:13px;padding:6px 11px;border-radius:999px;border:1px solid #30363d;background:#161b22;color:#c9d1d9}
button.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
input{width:100%;max-width:340px;padding:7px 11px;border-radius:8px;border:1px solid #30363d;background:#0d1117;color:#e6edf3;font:inherit;font-size:14px}
main{padding:10px 18px 60px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:720px}
th{text-align:left;color:#8b949e;font-weight:500;font-size:12px;text-transform:uppercase;letter-spacing:.04em;padding:8px 8px;border-bottom:1px solid #21262d}
td{padding:9px 8px;border-bottom:1px solid #161b22;vertical-align:top}
tr:hover td{background:#11161d}
a{color:#58a6ff;text-decoration:none}
a:hover{text-decoration:underline}
.tag{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;white-space:nowrap}
.ch-fj{background:#132a1d;color:#56d364}.ch-fj-msg{background:#1c2b3a;color:#79c0ff}
.ch-mail{background:#2b2213;color:#e3b341}.ch-tg{background:#1e2430;color:#a5d6ff}
.s-none{background:#1c2128;color:#8b949e}.s-refused{background:#3d1a1a;color:#ff7b72}
.price{white-space:nowrap;font-variant-numeric:tabular-nums}
.note{color:#8b949e;font-size:12.5px;display:block;margin-top:2px}
.empty{padding:30px;color:#8b949e}
</style></head><body>
<header>
  <h1>Отклики и письма</h1>
  <div class="sub">обновлено <span id="upd"></span></div>
  <div class="stats" id="stats"></div>
  <div class="filters" id="filters"></div>
  <input id="q" placeholder="поиск по заказу, id, заметке…">
</header>
<main><table>
<thead><tr><th>Канал</th><th>Куда</th><th>Цена</th><th>Срок</th><th>Статус</th></tr></thead>
<tbody id="rows"></tbody>
</table><div class="empty" id="empty" hidden>Ничего не найдено</div></main>
<script>
const DATA = __DATA__;
const CH = {"fj":"сайт: отклик","fj-msg":"сайт: письмо","mail":"e-mail","tg":"telegram"};
const ST = {"нет ответа":"ждём","отказ":"отказ","ответ":"ответ"};
let ch = "все", st = "все";
document.getElementById("upd").textContent = DATA.updated;
const counts = {
  всего: DATA.rows.length,
  "ждём": DATA.rows.filter(r=>r.s==="нет ответа").length,
  "отказ": DATA.rows.filter(r=>r.s==="отказ").length,
  "e-mail": DATA.rows.filter(r=>r.ch==="mail").length,
  "telegram": DATA.rows.filter(r=>r.ch==="tg").length
};
document.getElementById("stats").innerHTML = Object.entries(counts)
  .map(([k,v])=>`<div class="stat"><b>${v}</b>${k}</div>`).join("");
const F = [["ch","все","все"],["ch","fj","сайт: отклик"],["ch","fj-msg","сайт: письмо"],["ch","mail","e-mail"],["ch","tg","telegram"],
           ["st","все","статус: любой"],["st","нет ответа","ждём"],["st","отказ","отказ"]];
const fbox = document.getElementById("filters");
fbox.innerHTML = F.map(([k,v,l],i)=>`<button data-k="${k}" data-v="${v}" class="${(k==="ch"&&ch===v)||(k==="st"&&st===v)?"on":""}">${l}</button>`).join("");
fbox.onclick = e => { const b=e.target.closest("button"); if(!b) return;
  if(b.dataset.k==="ch") ch=b.dataset.v; else st=b.dataset.v; render(); };
document.getElementById("q").oninput = render;
function render(){
  [...fbox.children].forEach(b=>b.classList.toggle("on",
    (b.dataset.k==="ch"&&ch===b.dataset.v)||(b.dataset.k==="st"&&st===b.dataset.v)));
  const q = document.getElementById("q").value.trim().toLowerCase();
  const rows = DATA.rows.filter(r=>(ch==="все"||r.ch===ch)&&(st==="все"||r.s===st)&&
    (!q||(r.t+" "+r.id+" "+r.n).toLowerCase().includes(q)));
  document.getElementById("rows").innerHTML = rows.map(r=>`<tr>
    <td><span class="tag ch-${r.ch}">${CH[r.ch]}</span></td>
    <td><a href="${r.u}" target="_blank" rel="noopener">${r.t}</a><span class="note">#${r.id}${r.n?" · "+r.n:""}</span></td>
    <td class="price">${r.p}</td><td>${r.d}</td>
    <td><span class="tag ${r.s==="нет ответа"?"s-none":"s-refused"}">${ST[r.s]||r.s}</span></td></tr>`).join("");
  document.getElementById("empty").hidden = rows.length>0;
}
render();
</script></body></html>"""

out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(d / "index.html").write_text(out, encoding="utf-8")
print("index.html:", len(out), "байт, строк:", len(data["rows"]))
