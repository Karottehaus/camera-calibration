import streamlit as st


def render_warning(exposure_metrics: dict) -> None:
    if not exposure_metrics["is_exposure_valid"]:
        st.warning(
            f"Exposure time too high for selected frame rate.\n"
            f"Maximum frame rate for this exposure time is "
            f"{exposure_metrics['max_frame_rate']} Hz."
        )
