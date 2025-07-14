import streamlit as st
from utils.summarizer import extract_text_from_pdf, summarize_text
from utils.ask import answer_question
from utils.challenge import generate_questions
import time
import streamlit as st


# Create a placeholder block for loading screen
loading_placeholder = st.empty()

# Show the loading message inside the placeholder
loading_placeholder.markdown("""
    <div style='text-align: center; padding-top: 150px;'>
        <h2 style='color: #0366d6;'>🚀 Loading Smart Assistant...</h2>
        <p>Please wait while we prepare everything for you.</p>
    </div>
""", unsafe_allow_html=True)

# Simulate a delay (while your backend is initializing)
time.sleep(2)  # You can reduce/increase this as needed

# Once loading is done, clear the placeholder
loading_placeholder.empty()


st.set_page_config(page_title="Smart Research Assistant", layout="wide")

# Sidebar
with st.sidebar:
    st.title("📘 Smart Assistant")
    uploaded_file = st.file_uploader("📤 Upload your PDF file", type=["pdf"])
    mode = st.radio("🧠 Choose Mode:", ["Ask Anything", "Challenge Me"])
    st.markdown("---")
    st.caption("Made with ❤️ for intelligent research support")

st.title("📄 Research Summarization Assistant")
st.info("📘 Upload a research PDF from the sidebar, and select a mode to get started.\n\n"
        "• **Ask Anything**: Ask natural questions and get document-based answers.\n"
        "• **Challenge Me**: Practice with logic-based questions and evaluate your answers.")


# Main area
if uploaded_file:
    with st.spinner("📥 Uploading and processing file..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📝 Extracting and summarizing..."):
        document_text = extract_text_from_pdf("temp.pdf")
        summary = summarize_text(document_text)

    with st.expander("📋 Summary", expanded=True):
        st.write(summary)

    # Ask Anything Mode
    if mode == "Ask Anything":
        st.subheader("🔍 Ask a Question")
        user_question = st.text_input("💬 Your Question:")
        if user_question:
            with st.spinner("Thinking..."):
                response = answer_question(user_question, document_text)
                st.success(f"✅ Answer: {response['answer']}")
                st.info(f"🧾 Justification: {response['justification']}")

    # Challenge Mode
    elif mode == "Challenge Me":
        st.subheader("🧠 Challenge Yourself")
        with st.spinner("Generating questions..."):
            questions = generate_questions(document_text)

        for i, q in enumerate(questions, 1):
            st.markdown(f"**Q{i}. {q['question']}**")
            user_ans = st.text_input(f"Your Answer to Q{i}:", key=f"q{i}")
            if user_ans:
                if user_ans.lower() in q['answer'].lower():
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct Answer: {q['answer']}")
