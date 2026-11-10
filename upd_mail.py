import json

d = json.load(open("data.json", encoding="utf-8"))
upd = [
    ("spdelo", "не доставлено — 554 нет пользователя", "bounce 10.11"),
    ("mebel-postavka", "не доставлено — 550 relay not permitted", "bounce 10.11"),
    ("akkumbel", "отказ — «ничего не надо делать»", "ответ 10.11 15:30, Левитин М."),
]
for key, status, note in upd:
    for r in d["rows"]:
        if key in str(r.get("u", "")):
            r["s"] = status
            r["n"] = note
            print(r["id"], r["t"], "->", status)
d["updated"] = "2026-11-10 12:40"
json.dump(d, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
