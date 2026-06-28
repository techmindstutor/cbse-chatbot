import streamlit as st
from chatbot import get_answer

st.set_page_config(
    page_title="CBSE AI Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 CBSE AI Subject Chatbot")
st.markdown("Ask any question from your **AI subject syllabus** (Class 9-12)")

st.divider()

selected_class = st.selectbox(
    "Select Your Class",
    ["class9", "class10", "class11", "class12"],
    format_func=lambda x: x.replace("class", "Class ")
)

question = st.text_area(
    "Your Question",
    placeholder="e.g. What is machine learning? Explain supervised learning.",
    height=100
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Finding answer from your study material..."):
            answer, sources = get_answer(question, selected_class)

        st.success("Answer:")
        st.markdown(answer)

        if sources:
            with st.expander("Source Material"):
                for src in sources:
                    st.caption(f"📄 {src}")

st.divider()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if question and st.button("Save to History"):
    st.session_state.chat_history.append({
        "class": selected_class,
        "question": question
    })

if st.session_state.chat_history:
    st.subheader("Recent Questions")
    for item in reversed(st.session_state.chat_history[-5:]):
        st.caption(f"**{item['class'].replace('class', 'Class ')}** — {item['question']}")