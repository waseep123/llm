import streamlit as st
from chat import get_answer, add_document

st.set_page_config(page_title="Banking Assistant", layout="centered")

st.title("🏦 Banking Customer Support Chatbot")

# ---- Chat Section ----
with st.form("question_form"):
    question = st.text_input("Ask your banking question:")
    submitted = st.form_submit_button("Get Answer")

if submitted and question:
    with st.spinner("Thinking..."):
        answer = get_answer(question)
        st.markdown("#### 💬 Answer:")
        st.success(answer)

st.markdown("---")

# ---- Add Document Section ----
st.markdown("### ➕ Add a new banking document")

# Initialize session state
if "new_doc" not in st.session_state:
    st.session_state["new_doc"] = ""

# Callback to clear the text area
def clear_doc_text():
    st.session_state["new_doc"] = ""
    st.session_state["doc_added"] = True

# Input area
st.text_area(
    "Add new context document:",
    key="new_doc",
    height=150,
)

# Add Document button
if st.button("Add Document", on_click=clear_doc_text):
    if st.session_state.new_doc.strip():
        add_document(st.session_state.new_doc.strip())


# Show success message only once after clearing
if st.session_state.get("doc_added", False):
    st.success("Document added successfully!")
    st.session_state["doc_added"] = False
