import streamlit as st

from graph import agent
from utils import load_dataset, get_dataset_metadata
from response_formatter import format_response

st.set_page_config(
    page_title="Time-Series Analysis Agent",
    layout="wide"
)

st.title("📈 Time-Series Analysis Agent")

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

# Upload only once
if uploaded_file is not None:

    if "df" not in st.session_state:

        df = load_dataset(uploaded_file)

        st.session_state.df = df
        st.session_state.metadata = get_dataset_metadata(df)

        st.success("Dataset uploaded successfully.")

# Main Interface
if "df" in st.session_state:

    st.subheader("Dataset Preview")
    st.dataframe(st.session_state.df.head())

    st.divider()

    user_query = st.text_input(
        "Ask a question about your dataset"
    )

    if st.button("Analyze"):

        if not user_query.strip():

            st.warning("Please enter a question.")

        else:

            state = {
                "query": user_query,
                "metadata": st.session_state.metadata,
                "dataframe": st.session_state.df
            }

            with st.spinner("Analyzing..."):

                result = agent.invoke(state)

            # Guardrail
            if "tool_results" not in result:

                message = result["guardrail_result"].message

                if not message:
                    message = (
                        "I can only answer questions related to the uploaded "
                        "time-series dataset."
                    )

                st.warning(message)
                st.stop()

            tool_results = result["tool_results"]

            # -----------------------
            # Final Answer
            # -----------------------

            st.subheader("Answer")

            responses = format_response(
                        tool_results,
                        result["plan"]
                    )

            for response in responses:

                st.success(response)

            # -----------------------
            # Visualization
            # -----------------------

            for tool in tool_results:

                if tool.chart:

                    for figure in tool.chart:

                        st.plotly_chart(
                            figure,
                            use_container_width=True
                        )

            # -----------------------
            # Developer Details
            # -----------------------

            with st.expander("Analysis Plan"):

                st.json(
                    result["plan"].model_dump()
                )

            with st.expander("Tool Results"):

                for tool in tool_results:

                    st.json(
                        tool.model_dump()
                    )