from openai import OpenAI
import streamlit as st

st.set_page_config(page_icon="🤖", page_title="TLC UvA Chatbot")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🤖 TLC UvA Chatbot")
st.sidebar.title("🤖 TLC UvA Chatbot")
st.sidebar.info("""
                The **TLC UvA Chatbot** is maintained by the TLC-FMG AI Team at the University of Amsterdam. Please reach out to [tlc-fmg@uva.nl](mailto:tlc-fmg@uva.nl) with feedback and/or questions.
                \n\n
                We do not save any identifiable information. Our code base is public [here](https://github.com/saurabh-khanna/tlc-chatbot).
                """)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Define personas
personas = {
    "": "No persona selected",
    "Academic Advisor": "You are an academic advisor who provides guidance on academic matters, course selections, and career advice.",
    "Research Assistant": "You are a research assistant who helps with research-related queries, finding resources, and providing insights on methodologies.",
    "Administrative Support": "You are an administrative support assistant who helps with administrative tasks, university policies, and procedures.",
    "Technical Support": "You are a technical support specialist who assists with technical issues, software tools, and IT-related queries.",
    "Teacher": "You are a teacher at the University of Amsterdam who teaches classrooms, grades assessments, and provides educational support to students.",
    "Custom": "You can define your own persona here."
}

# Sample prompts from a teacher's perspective
sample_prompts = [
    "What are the requirements for the new research grant?",
    "Can you help me with my course syllabus?",
    "How do I access the university's online resources?",
    "What is the procedure for submitting grades?",
    "Can you assist me with technical issues in the lab?",
    "How can I improve student engagement in my online classes?",
    "What are the best practices for grading assessments?",
    "How do I request a teaching assistant for my course?",
    "Can you provide resources for professional development?",
    "What are the guidelines for conducting exams online?",
    "How can I integrate more interactive activities in my lectures?",
    "What support is available for curriculum development?",
    "How do I handle academic dishonesty in my classroom?",
    "What are the university's policies on student accommodations?",
    "How can I collaborate with other faculty members on research projects?"
]

with st.sidebar.form(key='persona_prompt_form'):
    selected_persona = st.selectbox("Choose a persona", options=list(personas.keys()), index=0)
    custom_persona = ""
    if selected_persona == "Custom":
        custom_persona = st.text_area("Define your custom persona")

    selected_prompt = st.selectbox("Select a sample prompt", [""] + sample_prompts)
    submit_button = st.form_submit_button(label='Apply')

if submit_button:
    if selected_prompt:
        st.session_state["sample_prompt"] = selected_prompt

# Display sample prompt in the chat input
if "sample_prompt" in st.session_state:
    prompt = st.session_state["sample_prompt"]
    del st.session_state["sample_prompt"]
else:
    prompt = st.chat_input("Ask me anything...")

# Display messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and generate response
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Define persona
    if selected_persona == "Custom" and custom_persona:
        persona = custom_persona
    else:
        persona = personas[selected_persona]

    # Add persona as the initial system message if any persona is selected
    messages = [{"role": "system", "content": f"You are a chatbot designed to assist faculty at the University of Amsterdam. {persona}"}] if selected_persona else []
    messages.extend(st.session_state["messages"])

    # Generate response with persona
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state["messages"].append({"role": "assistant", "content": response})
