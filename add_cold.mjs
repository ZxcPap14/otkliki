import fs from "node:fs";

const d = JSON.parse(fs.readFileSync("data.json", "utf8"));

function parseLeads(file, ch) {
  const text = fs.readFileSync(file, "utf8");
  const out = [];
  for (const raw of text.split(/\n## /).slice(1)) {
    const head = raw.split("\n")[0].trim();
    if (head.startsWith("Итог")) continue;
    const mail = (raw.match(/E-mail:\s*(\S+@\S+)/) || [])[1];
    const site = (raw.match(/Сайт:\s*(\S+)/) || [])[1] || "";
    const problem = ((raw.match(/Проблема:\s*(.+)/) || [])[1] || "").trim();
    const offer = (raw.match(/Что предлагаем:\s*(.+)/) || [])[1] || "";
    const prices = [...offer.matchAll(/(\d[\d\s]{0,6})\s*₽/g)];
    const price = prices.length
      ? prices[prices.length - 1][1].trim() + " ₽"
      : "—";
    if (!mail) continue;
    out.push({ head: head.replace(/^«|»/g, ""), mail, site, problem, price });
  }
  return out;
}

const lists = [
  { file: "../cold-leads.md", ch: "cold1", skip: [] },
  { file: "../cold-leads2.md", ch: "cold2", skip: ["Торговый Дом Стройбат"] },
];

const seen = new Set(
  d.rows.filter((r) => String(r.id).startsWith("cold")).map((r) => r.id),
);
let n = 0;
for (const { file, ch, skip } of lists) {
  let i = 0;
  for (const l of parseLeads(file, ch)) {
    if (skip.some((s) => l.head.includes(s))) continue;
    i++;
    const id = ch + "-" + i;
    if (seen.has(id)) continue;
    d.rows.push({
      ch: "mail",
      id,
      t: l.head.slice(0, 70),
      p: l.price,
      d: "—",
      s: "нет ответа",
      u: l.site,
      n: (l.problem || "холодное письмо").slice(0, 110),
    });
    n++;
  }
}

d.updated = "2026-11-10 05:40";
fs.writeFileSync("data.json", JSON.stringify(d, null, 1), "utf8");
const byCh = {};
for (const r of d.rows) byCh[r.ch] = (byCh[r.ch] || 0) + 1;
console.log("добавлено", n, "всего", d.rows.length, JSON.stringify(byCh));
