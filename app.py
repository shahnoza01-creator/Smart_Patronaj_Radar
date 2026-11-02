import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------------------
# SMS ЮБОРИШ ФУНКЦИЯСИ (Infinireach Gateway)
# ---------------------------------------------------------
API_KEY = "smsrelay_ed695179dc0ed5a5d5a4d918a51db476f1cdb7da61abd9424112a2b9b2831360"
DEVICE_ID = "3f1ce526-f753-4086-9962-74420517bd38"

def send_real_sms(phone_number, message_text):
    """Шошилинч ва режадаги реал SMS хабарларни телефонга юбориш"""
    url = "https://app.infinireach.io/api/v1/sms/send"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "deviceId": DEVICE_ID,
        "phone": phone_number,
        "message": message_text
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        try:
            return response.json()
        except:
            return {
                "status": "error", 
                "status_code": response.status_code,
                "raw_response": response.text
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# STREAMLIT ИЛОВАСИ ВЕБ-ИНТЕРФЕЙСИ
# ---------------------------------------------------------
st.set_page_config(page_title="Smart Patronaj & Health Radar", layout="wide")

st.title("🏥 Smart Patronaj & Health Radar")
st.write("Аҳоли саломатлигини мониторинг қилиш ва реал SMS огоҳлантириш тизими")

# 1. Файл юклаш бўлими
uploaded_file = st.file_uploader("Беморлар рўйхати (Excel ёки CSV) файлини юкланг", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.subheader("📊 Юкланган беморлар маълумотлари")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Файлни ўқишда хатолик: {e}")
else:
    st.info("Илтимос, таҳлилни бошлаш учун Excel ёки CSV ҳисобот файлини юкланг.")

st.divider()

# 2. SMS Огоҳлантириш модули
st.subheader("📲 Аҳолига SMS огоҳлантириш юбориш")

with st.expander("💬 Кунлик режа ва SMS матнини созлаш"):
    target_phone = st.text_input("Қабул қилувчи телефон рақами:", value="+998912446445")
    
    sms_text = st.text_area(
        "SMS хабари мазмуни:",
        value="Ҳурматли фуқаро! Бугун сизни ҳудудий патронаж ҳамшираси кўрикдан ўтказиши режалаштирилган. Уйда бўлишингизни сўраймиз."
    )

col_s1, col_s2 = st.columns(2)

with col_s1:
    if st.button("📲 Барча рўйхатдагиларга SMS юбориш"):
        with st.spinner("SMS юборилмоқда..."):
            res = send_real_sms(target_phone, sms_text)
            st.success(f"✅ Кунлик режадаги фуқаро ({target_phone}) рақамига SMS сўрови юборилди!")
            st.json(res)

with col_s2:
    if st.button("🔴 Фақат 'Қизил хавф'дагиларга SMS юбориш"):
        urgent_msg = "ШОШИЛИНЧ: Саломатлигингизни текшириш учун патронаж кўригига тайёр туринг ёки шифокорга мурожаат қилинг!"
        with st.spinner("Шошилинч SMS юборилмоқда..."):
            res = send_real_sms(target_phone, urgent_msg)
            st.warning("⚠️ Қизил гуруҳдаги бемор рақамига шошилинч SMS сўрови юборилди!")
            st.json(res)
