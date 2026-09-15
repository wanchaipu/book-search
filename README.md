# ค้นหาหนังสือ (Book Search)

เว็บค้นหาทะเบียนหนังสือ — static site ไฟล์เดียว ไม่ต้องมี backend/DB

ข้อมูลมาจาก Google Sheet **"25680502-ลงทะเบียนหนังสือ ชั้น 2-3 (ล่าสุด)"** แผ่นแรก (ชั้น 2)

## โครงสร้าง

| ไฟล์ | หน้าที่ |
|------|--------|
| `index.html` | หน้าค้นหา (ค้นหลายคำ, กรองตามหมายเหตุ/สำนักพิมพ์, ไฮไลต์คำ, แชร์ลิงก์ผลค้นได้ `?q=`) |
| `data/books.csv` | ข้อมูลดิบ export จากชีต |
| `data/books.json` | ข้อมูลที่หน้าเว็บโหลด (สร้างจาก CSV) |
| `scripts/build.py` | แปลง CSV → JSON |

## อัปเดตข้อมูลจากชีต

1. Google Sheet → เลือกแผ่นแรก → ไฟล์ → ดาวน์โหลด → CSV
2. บันทึกทับ `data/books.csv`
3. `python3 scripts/build.py`
4. commit + push

## รันบนเครื่อง

```bash
python3 -m http.server 8000
# เปิด http://localhost:8000
```

(เปิดด้วย `file://` ตรงๆ ไม่ได้ เพราะหน้าเว็บ fetch `data/books.json`)
