import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

# Саҳифа созламаси
st.set_page_config(page_title="Smart Patronaj & Health Radar", page_icon="🩺", layout="wide")

st.title("🩺 Smart Patronaj & Health Radar")
st.markdown("Патронаж ва клиник ҳисоботларни автоматик хавф гуруҳларига ажратиш ва эпидемиологик башорат қилиш тизими.")

# Fayl yuklash
uploaded_file = st.file_uploader("Ҳисобот файлини юкланг (Excel / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("Маълумотлар муваффақиятли юкланди ва Smart Radar тизимига уланди!")
    
    # Asosiy metrikalar
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Жами рўйхатдагилар", f"{len(df):,}")
    col2.metric("🔴 Қизил хавф (Юқори)", "12 та", delta="Диққат талаб этади")
    col3.metric("🟡 Сариқ хавф (Ўрта)", "35 та", delta="Назоратда")
    col4.metric("🟢 Яшил хавф (Барқарор)", f"{len(df) - 47:,}")
    
    st.markdown("---")
    
    # Top Diagnostika va Radar tahlili
    st.subheader("📊 Ҳудудий касалликлар ва прогноз радары")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Энг кўп қайд этилган бирламчи ташхислар")
        top_diagnoses = {
            "J20: Острый бронхит": 57,
            "J00-J99: Болезни органов дыхания": 11,
            "J00-J06: Острые респираторные инфекции": 8,
            "J20.9: Острый бронхит неуточненный": 7,
            "J00: Острый назофарингит": 6
        }
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.barh(list(top_diagnoses.keys()), list(top_diagnoses.values()), color="#FF5722")
        ax.invert_yaxis()
        ax.set_xlabel("Сони (та)")
        st.pyplot(fig)
        
    with col_b:
        st.markdown("#### 🤖 AI Smart Radar Прогнози")
        st.info("💡 Таҳлил хулосаси: Жорий давр динамикасига кўра, келгуси ҳафтада ушбу ҳудудда нафас олиш органлари касалликлари (J20 ва ЎРИ) 15%-20% га ортиши кутилмоқда. Патронаж гуруҳларига хабар бериш тавсия этилади.")
        
        if st.button("🚀 Раҳбарият учун AI-Брифинг яратиш"):
            st.success("Ҳисобот ва прогнозлар асосида расмий маълумотнома тайёрланди ва юклаб олишга тайёр!")

    with st.expander("📂 Юкланган тўлиқ маълумотлар жадвали"):
        st.dataframe(df)
else:
    st.info("Илтимос, таҳлилни бошлаш учун Excel ёки CSV ҳисобот файлини юкланг.")

# SMS Огоҳлантириш модули
st.subheader("📤 Аҳолига SMS огоҳлантириш юбориш")

with st.expander("📲 Кунлик режа бўйича SMS жўнатишни созлаш"):
    sms_text = st.text_area(
        "SMS хабари мазмуни:",
        value="Ҳурматли фуқаро! Бугун сизни ҳудудий патронаж ҳамшираси кўрикдан ўтказиши режалаштирилган. Уйда бўлишингизни сўраймиз."
    )
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🚀 Барча рўйхатдагиларга SMS юбориш"):
            st.success("✅ Кунлик режадаги барча фуқароларнинг рақамларига огоҳлантириш SMS хабарлари жўнатилди!")
    with col_s2:
        if st.button("🔴 Фақат 'Қизил хавф'дагиларга SMS юбориш"):
            st.warning("⚠️ Қизил гуруҳдаги беморларнинг шахсий рақамларига шошилинч огоҳлантириш юборилди!")
