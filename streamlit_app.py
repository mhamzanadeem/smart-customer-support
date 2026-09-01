import os

import requests

import streamlit as st

from dotenv import load_dotenv


load_dotenv()


API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000",
)


st.set_page_config(

    page_title=(
        "Smart Support Agent"
    ),

    page_icon="🤖",
)


st.title(
    "🤖 Smart Customer Support"
)


st.caption(
    "RAG + LangGraph + "
    "OpenAI Agents SDK"
)


thread_id = st.text_input(
    "Thread ID",
    value="demo-thread",
)


query = st.text_area(

    "Customer question",

    placeholder=(
        "Example: I get AUTH-401 "
        "when calling the API. "
        "What should I do?"
    ),
)


if (
    st.button(
        "Ask Support",
        type="primary",
    )
    and query.strip()
):

    with st.spinner(
        "Running support workflow..."
    ):

        response = requests.post(

            f"{API_URL}/api/chat",

            json={
                "query":
                    query,

                "thread_id":
                    thread_id,
            },

            timeout=90,
        )


    if response.ok:

        data = response.json()


        st.subheader(
            "Answer"
        )

        st.write(
            data["answer"]
        )


        if data.get(
            "escalated"
        ):

            st.warning(

                f"Escalated: "
                f"{data.get('ticket_id')}"
            )


        with st.expander(
            "Retrieved sources"
        ):

            for src in data.get(
                "sources",
                [],
            ):

                st.markdown(

                    f"**{src['title']}** "
                    f"— similarity="
                    f"{src.get('similarity')}"
                )

                st.write(
                    src["content"]
                )


        with st.expander(
            "LangGraph trace"
        ):

            st.write(
                data.get(
                    "trace",
                    [],
                )
            )


    else:

        st.error(
            response.text
        )