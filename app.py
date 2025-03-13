import streamlit as st

# ตั้งค่าธีมแบบมินิมอล
st.set_page_config(page_title="📄 PDF Tool", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #222831;  /* สีพื้นหลังเข้ม */
            color: #eeeeee;  /* สีตัวอักษร */
            text-align: center;
        }
        .title-text {
            color: #00adb5;  /* สีเทอร์ควอยซ์ */
            font-size: 28px;  /* ลดขนาดตัวอักษร */
            text-align: center;
            font-weight: bold;
        }
        .subtitle-text {
            color: #eeeeee;
            font-size: 18px;  /* ลดขนาดตัวอักษรของคำอธิบาย */
            text-align: center;
        }
        .stSidebar {
            background-color: #393e46 !important;  /* สี Sidebar เข้ม */
            color: white !important;
        }
        .stButton > button {
            background-color: #00adb5 !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            width: 100%;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 🔹 แสดงชื่อแอปให้อยู่ตรงกลาง
st.markdown("<p class='title-text'>📄 PDF Tool: ตรวจคำผิด & แปลภาษา</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>🌟 เลือกเมนูที่ต้องการ</p>", unsafe_allow_html=True)

# 🔹 เพิ่มปุ่มลิงก์ไปหน้าอื่น
col1, col2, col3 = st.columns([1, 2, 1])  # ให้ปุ่มอยู่ตรงกลาง

with col2:
    if st.button("🔍 ไปที่หน้า 'ตรวจคำผิด'"):
        st.switch_page("ตรวจคำผิด.py")  # ✅ เปิดหน้าตรวจคำผิด
    if st.button("🌍 ไปที่หน้า 'แปลภาษา'"):
        st.switch_page("แปลภาษา.py")  # ✅ เปิดหน้าแปลภาษา
