import streamlit as st
import os
from pdf_processing import extract_text_from_pdf, translate_text, save_text_to_pdf
from googletrans import LANGUAGES

TRANSLATED_FOLDER = "translated_pdfs"
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

st.set_page_config(page_title="🌍 แปลภาษา", layout="wide")

st.markdown("""
    <style>
        .title-text {
            color: #28a745;
            font-size: 28px;
            text-align: center;
            font-weight: bold;
        }
        .stButton > button {
            background-color: #28a745 !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            width: 100%;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 🔹 หัวข้ออยู่ตรงกลาง
st.markdown("<p class='title-text'>🌍 แปลภาษาเอกสาร PDF</p>", unsafe_allow_html=True)

# 🔹 ปุ่มนำทาง
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav2:
    if st.button("🏠 กลับไปหน้าแรก"):
        st.switch_page("app.py")
    if st.button("🔍 ไปที่หน้า 'ตรวจคำผิด'"):
        st.switch_page("pages/ตรวจคำผิด.py")

lang_options = {f"{lang_name} ({lang_code})": lang_code for lang_code, lang_name in LANGUAGES.items()}
selected_lang = st.selectbox("📌 เลือกภาษาที่ต้องการแปล:", list(lang_options.keys()))

uploaded_files = st.file_uploader("📎 อัปโหลดไฟล์ PDF ของคุณ", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_path = os.path.join(TRANSLATED_FOLDER, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ อัปโหลดไฟล์สำเร็จ: `{uploaded_file.name}`")

        with st.spinner("📖 กำลังอ่านไฟล์..."):
            extracted_lines = extract_text_from_pdf(pdf_path)

        if not extracted_lines:
            st.error("⚠️ ไม่พบข้อความในไฟล์ PDF ⚠️")
        else:
            with st.spinner("🌍 กำลังแปลภาษา..."):
                if extracted_lines and isinstance(extracted_lines, list) and any(extracted_lines):
                    translated_lines = translate_text(extracted_lines, target_lang=lang_options[selected_lang])
                else:
                    translated_lines = ["⚠️ ไม่พบข้อความให้แปล ⚠️"]

            st.markdown(f"## 🌍 ข้อความที่ถูกแปล ({selected_lang})")
            st.text_area("📜 ข้อความที่แปลแล้ว", "\n".join(translated_lines), height=200)

            # 🔽 บันทึกเป็น PDF
            translated_pdf_path = os.path.join(TRANSLATED_FOLDER, f"translated_{uploaded_file.name}")
            save_text_to_pdf("\n".join(translated_lines), translated_pdf_path)

            # 🔽 ให้ดาวน์โหลดเป็น PDF
            with open(translated_pdf_path, "rb") as file:
                st.download_button("⬇️ ดาวน์โหลด PDF ที่แปลแล้ว", file, file_name=f"translated_{uploaded_file.name}", mime="application/pdf")
