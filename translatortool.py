#C:\miniconda\Conda_install\AI\Language translator\translatortool
import streamlit as st
from googletrans import Translator, LANGUAGES

st.set_page_config(page_title="Universal Translator", layout="wide")

translator = Translator()
lang_name_to_code = {name.title(): code for code, name in LANGUAGES.items()}
lang_names = sorted(lang_name_to_code.keys())

if "saved_translations" not in st.session_state:
    st.session_state.saved_translations = []
if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

st.sidebar.title("Translation History")
if st.session_state.saved_translations:
    for i, saved in enumerate(reversed(st.session_state.saved_translations)):
        st.sidebar.markdown(f"**{i+1}.** {saved}")
else:
    st.sidebar.write("No saved translations yet.")

st.markdown(
    "<h1 style='font-family: time new roman; color:rgb(32, 53, 177); text-align: center;'>TRANSIRRA </h1>",
    unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Input")
    input_text = st.text_area("", height=200)

with col2:
    st.subheader("Output")
    output_text_placeholder = st.empty()

col3, col4 = st.columns(2)
with col3:
    src_lang_display = st.selectbox("From", ["Auto Detect"] + lang_names)
with col4:
    dest_lang_display = st.selectbox("To", lang_names)

col_translate, col_save, col_clear = st.columns(3)

if col_translate.button("Translate"):
    if input_text.strip():
        try:
            src_lang_code = "auto" if src_lang_display == "Auto Detect" else lang_name_to_code[src_lang_display]
            dest_lang_code = lang_name_to_code[dest_lang_display]
            translated = translator.translate(input_text, src=src_lang_code, dest=dest_lang_code)
            detected_lang = LANGUAGES.get(translated.src, translated.src)
            output_text = f"{translated.text} (Detected: {detected_lang.title()})"
            output_text_placeholder.markdown(output_text)
            st.session_state.last_translation = output_text
        except Exception as e:
            output_text_placeholder.error(f"Translation failed: {e}")
    else:
        output_text_placeholder.warning("Please enter text to translate.")

if col_save.button("Save"):
    if st.session_state.last_translation:
        st.session_state.saved_translations.append(
            f"{st.session_state.last_translation}"
        )
    else:
        st.warning("No translation to save.")

if col_clear.button("Clear"):
    st.session_state.saved_translations.clear()
    st.session_state.last_translation = ""
    output_text_placeholder.empty()
    st.rerun()