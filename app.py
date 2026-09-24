import streamlit as st
from pathlib import Path

from intent_module import detect_intent
from retrieval_module import (
    load_interactions,
    retrieve_similar_email
)
from reply_module import generate_reply
from tone_module import (
    improve_tone,
    TONES
)
from summary_module import (
    summarize_conversation
)
from utils import save_reply


st.set_page_config(
    page_title="Intelligent Email Assistant",
    page_icon="✉️",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("✉️ Intelligent Email Assistant")

st.caption(
    "AI-powered customer email analysis and "
    "reply generation using Ollama"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    tone = st.selectbox(
        "Reply Tone",
        TONES,
        index=1
    )

    st.markdown("### AI Model")

    st.code(
        "Ollama + Qwen",
        language="text"
    )

    st.markdown("### Workflow")

    st.markdown(
        """
        1. Customer Input
        2. Intent Detection
        3. Similar Email Search
        4. AI Reply Generation
        5. Tone Improvement
        6. Conversation Summary
        7. Save Reply
        """
    )


# =========================================================
# CUSTOMER INPUT
# =========================================================

st.subheader("1️⃣ Customer Email")


col1, col2 = st.columns(2)


with col1:

    customer_name = st.text_input(
        "Customer Name",
        placeholder="e.g. Adarsh"
    )


with col2:

    subject = st.text_input(
        "Email Subject",
        placeholder="e.g. Delivery Delay"
    )


customer_email = st.text_area(
    "Customer Email",
    height=180,
    placeholder="Enter the customer's email here..."
)


process = st.button(
    "🚀 Analyze Email & Generate Reply",
    type="primary",
    use_container_width=True
)


# =========================================================
# PROCESS EMAIL
# =========================================================

if process:

    # -----------------------------
    # Validation
    # -----------------------------

    if not customer_name.strip():

        st.error(
            "Please enter the customer name."
        )

        st.stop()


    if not subject.strip():

        st.error(
            "Please enter the email subject."
        )

        st.stop()


    if not customer_email.strip():

        st.error(
            "Please enter the customer email."
        )

        st.stop()


    try:

        # =================================================
        # INTENT DETECTION
        # =================================================

        with st.spinner(
            "Detecting customer intent with Ollama..."
        ):

            intent = detect_intent(
                customer_email
            )

        st.session_state["intent"] = intent


        # =================================================
        # SIMILAR EMAIL RETRIEVAL
        # =================================================

        with st.spinner(
            "Searching historical emails..."
        ):

            df = load_interactions()

            result = retrieve_similar_email(
                customer_email,
                subject,
                df
            )

        st.session_state["retrieval"] = result


        # =================================================
        # AI REPLY GENERATION
        # =================================================

        with st.spinner(
            "Generating professional reply..."
        ):

            reply = generate_reply(
                customer_email,
                result["previous_reply"],
                customer_name
            )

        st.session_state["reply"] = reply


        # =================================================
        # TONE IMPROVEMENT
        # =================================================

        with st.spinner(
            f"Improving reply using {tone.lower()} tone..."
        ):

            improved_reply = improve_tone(
                reply,
                tone
            )

        st.session_state[
            "improved_reply"
        ] = improved_reply

        st.session_state[
            "tone"
        ] = tone


        # =================================================
        # SUMMARY
        # =================================================

        with st.spinner(
            "Generating conversation summary..."
        ):

            summary = summarize_conversation(
                customer_email,
                improved_reply
            )

        st.session_state[
            "summary"
        ] = summary


        st.success(
            "Email analysis completed successfully!"
        )


    except Exception as e:

        st.error(
            f"Unable to process the email.\n\n"
            f"Error: {e}"
        )


# =========================================================
# RESULTS
# =========================================================

if "intent" in st.session_state:

    st.divider()

    st.subheader(
        "2️⃣ Analysis Results"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Detected Intent",
            st.session_state["intent"]
        )


    with col2:

        similarity = (
            st.session_state[
                "retrieval"
            ]["similarity"]
        )

        st.metric(
            "Similarity Score",
            f"{similarity:.3f}"
        )


    with col3:

        st.metric(
            "Selected Tone",
            st.session_state["tone"]
        )


    # =====================================================
    # SIMILAR EMAIL
    # =====================================================

    st.subheader(
        "3️⃣ Similar Historical Email"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "**Previous Email**"
        )

        st.info(
            st.session_state[
                "retrieval"
            ]["previous_email"]
        )


    with col2:

        st.markdown(
            "**Previous Reply**"
        )

        st.info(
            st.session_state[
                "retrieval"
            ]["previous_reply"]
        )


    # =====================================================
    # AI REPLY
    # =====================================================

    st.subheader(
        "4️⃣ AI Generated Reply"
    )


    final_reply = st.text_area(
        "Final Reply",
        value=st.session_state[
            "improved_reply"
        ],
        height=250
    )


    # =====================================================
    # SUMMARY
    # =====================================================

    st.subheader(
        "5️⃣ Conversation Summary"
    )


    summary = st.text_area(
        "50-Word Summary",
        value=st.session_state[
            "summary"
        ],
        height=120
    )


    # =====================================================
    # SAVE
    # =====================================================

    st.subheader(
        "6️⃣ Save Conversation"
    )


    if st.button(
        "💾 Save Reply to generated_reply.txt"
    ):

        path = save_reply(
            customer_email,
            final_reply,
            st.session_state["intent"],
            st.session_state["tone"],
            summary
        )

        st.success(
            "Reply saved successfully!"
        )


        file_path = Path(path)


        if file_path.exists():

            st.download_button(
                "⬇️ Download Generated Reply",
                data=file_path.read_text(
                    encoding="utf-8"
                ),
                file_name="generated_reply.txt",
                mime="text/plain",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()
