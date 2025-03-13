# 📄 PDF Tool: ตรวจคำผิด & แปลภาษา

📄 **PDF Tool** เป็น **Streamlit Web App** ที่เรัยนไดในงาน **ตรวจคำผิด** และ **แปลภาษา** จากไฟล์ PDF

- 📜 พร้อม **OCR** เพื่อดึงข้อความจาก PDF ที่เป็นภาพ
- 🌍 แปลภาษา **ไทยและอังกฤษ**
- 📥 ดาวน์โหลด PDF ที่แก้ไขหรือแปลแล้ว

---

## 📂 โครงสร้างโฟลเดอร์
```
WORK_NLP/
├── __pycache__/            # ไฟล์แคชของ Python
├── corrected_pdfs/        # โฟลเดอร์เก็บ PDF ที่แก้ไขแล้ว
├── fonts/                 # โฟลเดอร์เก็บไฟล์ฟอนต์
│   ├── THSARABUNNEW.TTF   # ฟอนต์ภาษาไทยสำหรับสร้าง PDF
├── pages/                 # โฟลเดอร์เก็บไฟล์หน้า UI
│   ├── ตรวจคำผิด.py      # หน้า UI สำหรับตรวจคำผิด
│   ├── แปลภาษา.py        # หน้า UI สำหรับแปลภาษา
├── poppler/               # โฟลเดอร์เก็บ Poppler (สำหรับแปลง PDF เป็นภาพ)
├── translated_pdfs/       # โฟลเดอร์เก็บ PDF ที่แปลแล้ว
├── uploads/               # โฟลเดอร์เก็บไฟล์ PDF ที่อัปโหลด
├── venv/                  # Virtual Environment (ควรเพิ่มใน .gitignore)
├── .gitignore             # ไฟล์บอกให้ Git ไม่ติดตาม venv และไฟล์ที่ไม่จำเป็น
├── app.py                 # ไฟล์ Streamlit หน้าแรก
├── pdf_processing.py      # โมดูล OCR, ตรวจคำผิด, แปลภาษา
├── README.md              # คำอธิบายโปรเจกต์
└── requirements.txt       # รายการไลบรารีที่ต้องติดตั้ง
```

---

## 🚀 วิธีติดตั้งและใช้งาน
### 1️⃣ ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ รัน Streamlit Web App
```bash
streamlit run app.py
```
📌 **เปิดแอปที่:** `http://localhost:8501`

---

## ⚙️ ฟังก์ชันของแต่ละไฟล์
📂 **`pages/ตรวจคำผิด.py`** - ตรวจสอบคำผิดในเอกสาร PDF
📂 **`pages/แปลภาษา.py`** - แปลภาษาเอกสาร PDF
📂 **`pdf_processing.py`** - ดึงข้อความ, ตรวจคำผิด, แปลภาษา

---

## 🔗 แหล่งที่มา
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyMuPDF (Fitz) Documentation](https://pymupdf.readthedocs.io/en/latest/)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Google Translate API](https://py-googletrans.readthedocs.io/en/latest/)
- [PyThaiNLP](https://pythainlp.github.io/)
- [LanguageTool](https://languagetool.org/)

---

## ❗ ข้อผิดพลาดที่พบบ่อย & วิธีแก้ไข
### 1️⃣ **ไฟล์ PDF ไม่มีข้อความ (ต้องใช้ OCR)**
**ปัญหา:** โปรแกรมไม่สามารถดึงข้อความจาก PDF ได้เพราะเป็นไฟล์ภาพ
**แนวทางแก้ไข:** ใช้ `pytesseract` หรือ `easyocr` เพื่อทำ OCR

### 2️⃣ **ไม่สามารถแปลภาษาได้**
**ปัญหา:** API ของ Google Translate อาจมีปัญหา หรือไฟล์ไม่มีข้อความ
**แนวทางแก้ไข:** ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต และลองใช้ `deep-translator`

### 3️⃣ **ตรวจคำผิดแล้วไม่มีผลลัพธ์**
**ปัญหา:** โมเดลอาจไม่รู้จักคำบางคำในภาษาไทย
**แนวทางแก้ไข:** ลองใช้ `NorvigSpellChecker` หรือเพิ่ม Dictionary เอง

### 4️⃣ **เกิดปัญหา PermissionError ขณะบันทึกไฟล์**
**ปัญหา:** โปรแกรมไม่มีสิทธิ์เขียนไฟล์ลงในโฟลเดอร์ที่กำหนด
**แนวทางแก้ไข:** ลองรัน `streamlit` ด้วยสิทธิ์ **Administrator** บน Windows

---

🚀 **หากพบปัญหาเพิ่มเติม สามารถแจ้งมาได้เลย!**
