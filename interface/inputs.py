import streamlit as st


def render_sidebar_inputs() -> dict:
    st.sidebar.header("Input Parameters")

    return {
        "table_position": st.sidebar.number_input(
            "Table Position (cm)",
            value=3.13,
            step=0.01
        ),
        "fov": st.sidebar.number_input(
            "Field of View (mm)",
            value=50.0,
            step=0.1
        ),
        "exposure_time": st.sidebar.number_input(
            "Exposure Time (ms)",
            value=100.0,
            step=0.1
        ),
        "frame_rate": st.sidebar.number_input(
            "Frame Rate (Hz)",
            value=9.0,
            step=0.1
        ),
        "core_length": st.sidebar.number_input(
            "Core Length (mm)",
            value=1000.0,
            step=0.1
        )
    }
