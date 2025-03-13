import streamlit as st
import os
import pandas as pd
from pdf_processing import extract_text_from_pdf, correct_text, save_text_to_pdf

UPLOAD_FOLDER = "uploads"
CORRECTED_FOLDER = "corrected_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CORRECTED_FOLDER, exist_ok=True)

st.set_page_config(page_title="📝 ตรวจสอบคำผิด", layout="wide")

st.markdown("""
    <style>
        .title-text {
            color: #ff5733;
            font-size: 28px;
            text-align: center;
            font-weight: bold;
        }
        .subtitle-text {
            color: #eeeeee;
            font-size: 18px;
            text-align: center;
        }
        .stButton > button {
            background-color: #ff5733 !important;
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
st.markdown("<p class='title-text'>📝 ตรวจสอบคำผิดในเอกสาร PDF</p>", unsafe_allow_html=True)

# 🔹 ปุ่มนำทาง
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav2:
    if st.button("🏠 กลับไปหน้าแรก"):
        st.switch_page("app.py")
    if st.button("🌍 ไปที่หน้า 'แปลภาษา'"):
        st.switch_page("pages/แปลภาษา.py")

uploaded_files = st.file_uploader("📎 อัปโหลดไฟล์ PDF ของคุณ", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ อัปโหลดไฟล์สำเร็จ: `{uploaded_file.name}`")

        with st.spinner("📖 กำลังอ่านไฟล์..."):
            extracted_lines = extract_text_from_pdf(pdf_path)

        if not extracted_lines:
            st.error("⚠️ ไม่พบข้อความในไฟล์ PDF ⚠️")
        else:
            with st.spinner("🔍 กำลังตรวจคำผิด..."):
                corrected_lines, error_list = correct_text(extracted_lines)

            # แบ่ง UI ครึ่งหน้า
            col1, col2 = st.columns(2)

            # 🔴 ด้านซ้าย: แสดงคำผิดที่พบ
            with col1:
                st.markdown("## 🛑 รายการคำผิดที่ตรวจพบ")
                if error_list:
                    df_errors = pd.DataFrame(error_list, columns=["บรรทัดที่", "คำผิด", "ตัวเลือกทั้งหมด"])
                    st.dataframe(df_errors)
                else:
                    st.success("✅ ไม่มีคำผิด!")

            # 🟢 ด้านขวา: ข้อความที่แก้ไขอัตโนมัติ
            with col2:
                st.markdown("## ✅ ข้อความที่ถูกแก้ไขอัตโนมัติ")
                for line_no, error, suggestions in error_list:
                    if suggestions:
                        corrected_lines[line_no - 1] = corrected_lines[line_no - 1].replace(error, suggestions[0])

                corrected_text = "\n".join(corrected_lines)
                st.text_area("📜 ข้อความที่ถูกแก้ไข", corrected_text, height=300)

                # 🔽 บันทึกเป็น PDF แล้วให้ดาวน์โหลด
                corrected_pdf_path = os.path.join(CORRECTED_FOLDER, f"corrected_{uploaded_file.name}")
                save_text_to_pdf(corrected_text, corrected_pdf_path)

                with open(corrected_pdf_path, "rb") as file:
                    st.download_button("⬇️ ดาวน์โหลด PDF ที่แก้ไขแล้ว", file, file_name=f"corrected_{uploaded_file.name}", mime="application/pdf")
