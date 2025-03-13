import numpy as np
import fitz  # PyMuPDF
import language_tool_python
from googletrans import Translator
from pythainlp.tokenize import word_tokenize
from pythainlp.spell import NorvigSpellChecker, spell
from pdf2image import convert_from_path
import pytesseract
import easyocr
import re  # 🔥 เพิ่ม regex สำหรับกรองอักขระสุ่ม
import os

# 🔥 อัปเดตใหม่: ใช้ ReportLab และกำหนด path ฟอนต์ที่ถูกต้อง
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ตั้งค่า Tesseract OCR (เฉพาะ Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# โหลดตัวตรวจคำผิดภาษาไทย
thai_spell_checker = NorvigSpellChecker()
# โหลดโมดูลตรวจคำผิดภาษาอังกฤษ
tool = language_tool_python.LanguageTool('en-US')
translator = Translator()

# 🔥 อัปเดตใหม่: เพิ่ม path ฟอนต์เพื่อรองรับภาษาไทย-อังกฤษ
FONT_PATH = "fonts/THSarabunNew.ttf"
POPPLER_PATH = r"C:\Users\User\poppler-24.08.0\Library\bin"  # 🔥 อัปเดต path Poppler

def clean_ocr_text(text):
    """ กรองอักขระที่ไม่ใช่ภาษาไทยหรืออังกฤษออก """
    cleaned_text = re.sub(r"[^ก-ฮa-zA-Z0-9\s.,\n]", "", text)  # 🔥 เอาเฉพาะภาษาไทย อังกฤษ และตัวเลข
    return cleaned_text

def extract_text_from_pdf(pdf_path, force_ocr=False):
    """ อ่านข้อความจาก PDF และใช้ OCR ถ้าจำเป็น (รองรับไทย-อังกฤษเท่านั้น) """
    doc = fitz.open(pdf_path)
    text = []
    
    if not force_ocr:  # ✅ ใช้ PyMuPDF ดึงข้อความถ้าได้
        for page in doc:
            page_text = page.get_text("text").strip()
            if page_text:
                text.extend(page_text.split("\n"))
                return text  # ✅ ถ้าพบข้อความ → คืนค่าเลย (ไม่ใช้ OCR)

    # ❌ ถ้าถูกบังคับใช้ OCR → แปลง PDF เป็นรูปภาพ
    images = convert_from_path(pdf_path, dpi=400, poppler_path=POPPLER_PATH)  # 🔥 เพิ่ม DPI
    reader = easyocr.Reader(['th', 'en'])

    for img in images:
        img_array = np.array(img)  # 🔥 แปลง PIL เป็น numpy array

        # 🔥 ใช้ pytesseract OCR กับ --psm 11 เพื่อรองรับเอกสารแบบตาราง และให้เน้นไทย+อังกฤษ
        ocr_text = pytesseract.image_to_string(img, lang="tha+eng", config="--psm 11 --oem 3").strip()

        if len(ocr_text) < 10:  # 🔥 ถ้า pytesseract อ่านไม่ได้ ใช้ easyocr
            ocr_result = reader.readtext(img_array, detail=1)
            filtered_text = [text for (bbox, text, confidence) in ocr_result if confidence > 0.7]  # 🔥 ใช้ threshold 70%
            ocr_text = "\n".join(filtered_text)

        # 🔥 กรองข้อความให้สะอาดขึ้น (ลบอักขระที่ไม่ใช่ไทย-อังกฤษ)
        ocr_text = clean_ocr_text(ocr_text)

        text.extend(ocr_text.split("\n"))

    return text

def detect_language(text):
    """ ตรวจจับภาษาไทยหรืออังกฤษ """
    return "th" if any("ก" <= ch <= "ฮ" or "๐" <= ch <= "๙" for ch in text) else "en"

def correct_text(lines):
    """ ตรวจคำผิดทั้งภาษาไทยและอังกฤษ """
    corrected_lines = []
    error_list = []

    for line_no, line in enumerate(lines, start=1):
        lang = detect_language(line)
        corrected_line = line

        if lang == "en":
            matches = tool.check(line)
            for match in matches:
                if match.replacements:
                    error_word = line[match.offset: match.offset + match.errorLength]
                    corrections = match.replacements
                    error_list.append((line_no, error_word, corrections))
        else:
            words = word_tokenize(line)
            unknown_words = [word for word in words if word not in spell(word)]
            for word in unknown_words:
                corrected_word = thai_spell_checker.correct(word)
                if corrected_word != word:
                    error_list.append((line_no, word, [corrected_word]))

        corrected_lines.append(corrected_line)

    return corrected_lines, error_list

def translate_text(lines, target_lang="th"):
    """ แปลข้อความไปยังภาษาที่ต้องการ """
    if not lines or not isinstance(lines, list):  # 🔥 ตรวจสอบว่ามีค่า และเป็น list
        return ["⚠️ ไม่พบข้อความให้แปล ⚠️"]

    if all(not isinstance(line, str) or line.strip() == "" for line in lines):  # 🔥 ตรวจสอบว่าทุกบรรทัดเป็นข้อความ
        return ["⚠️ ไม่พบข้อความให้แปล ⚠️"]

    text = " ".join(lines).replace("\n", " ")  # รวมเป็นประโยคเดียว
    translated = translator.translate(text, dest=target_lang)
    return translated.text.split("\n")  # แบ่งเป็นบรรทัด


def save_text_to_pdf(text, output_path, font_path=FONT_PATH):
    """ บันทึกข้อความลง PDF โดยให้ขึ้นบรรทัดใหม่อัตโนมัติ """
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"ไม่พบฟอนต์: {font_path} กรุณาตรวจสอบว่าฟอนต์อยู่ในโฟลเดอร์ที่ถูกต้อง")

    pdfmetrics.registerFont(TTFont("CustomFont", font_path))

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "CustomFont"
    styles["Normal"].fontSize = 18
    styles["Normal"].leading = 25

    formatted_text = Paragraph(text.replace("\n", "<br/>"), styles["Normal"])
    doc.build([formatted_text])
