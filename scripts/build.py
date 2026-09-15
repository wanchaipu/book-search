#!/usr/bin/env python3
"""แปลง data/books.csv (export จาก Google Sheet แผ่นแรก) → data/books.json

ใช้:  python3 scripts/build.py [path/to/books.csv]
"""
import csv, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "books.csv"

FIELDS = {  # หัวคอลัมน์ในชีต → key ใน JSON
    "เลขทะเบียน": "id",
    "ชื่อเรื่อง": "title",
    "รหัสหนังสือ": "call",
    "ตู้เก็บ": "shelf",
    "หมายเหตุ": "note",
    "ชื่อผู้แต่ง": "author",
    "ประเภท": "type",
    "รูป": "img",
}

IMG_DIR = ROOT / "images"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

def image_for(b):
    """คอลัมน์ "รูป" ในชีต (URL / ลิงก์ Google Drive) มาก่อน, ไม่มีก็หา images/<เลขทะเบียน>.jpg"""
    url = b.get("img", "")
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?.*?id=)([\w-]{20,})", url)
    if m:
        return f"https://drive.google.com/thumbnail?id={m.group(1)}&sz=w600"
    if url.startswith("http"):
        return url
    for ext in IMG_EXT:
        p = IMG_DIR / f"{b['id']}{ext}"
        if b["id"] and p.exists():
            return f"images/{p.name}"
    return ""

def clean(s):
    s = " ".join((s or "").split())
    # ชีตบางแถวครอบชื่อเรื่องด้วย "..." ทั้งก้อน
    if len(s) > 1 and s[0] == '"' and s[-1] == '"' and s.count('"') == 2:
        s = s[1:-1].strip()
    return s

with src.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.reader(f))

header = [h.strip() for h in rows[0]]
books = []
for r in rows[1:]:
    b = {key: "" for key in FIELDS.values()}
    for i, h in enumerate(header):
        if h in FIELDS and i < len(r):
            b[FIELDS[h]] = clean(r[i])
    b["img"] = image_for(b)
    if b["id"] or b["title"]:
        books.append(b)

out = ROOT / "data" / "books.json"
out.write_text(json.dumps(books, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(books)} books ({sum(1 for b in books if b['img'])} with image) → {out.relative_to(ROOT)}")
