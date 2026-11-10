import fs from "node:fs";
const d = JSON.parse(fs.readFileSync("data.json", "utf8"));
const chats = [
  "freelancers_point",
  "FreelanceWebmasters",
  "webjobagregator",
  "it_and_freelance_chat",
  "frilancru",
  "udalenka_chat_vakansii",
  "freelance_and_udalenka_chat",
  "infomarket_chat",
  "chat_frilanserov",
  "flexta_chat",
  "feyhoa_event_hunt",
  "k_design_k_chat",
  "chat_tochka_la",
  "prezentation10",
  "chat23232",
];
let n = 0;
for (const c of chats) {
  const id = "@" + c;
  if (d.rows.some((r) => r.ch === "tg" && r.id === id)) continue;
  d.rows.push({
    ch: "tg",
    id,
    t: "своё объявление в чате",
    p: "500–1500 ₽",
    d: "—",
    s: "нет ответа",
    u: "https://t.me/" + c,
    n: "предложение услуг",
  });
  n++;
}
d.updated = "2026-11-10 04:10";
fs.writeFileSync("data.json", JSON.stringify(d, null, 1), "utf8");
console.log("добавлено", n, "всего", d.rows.length);
