import streamlit as st
import pandas as pd


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


def render_results(
        calibration_table: pd.DataFrame,
        scan_metrics: dict,
        exposure_metrics: dict
) -> None:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Calibration Result")
        st.dataframe(calibration_table, use_container_width=True)

    with col2:
        st.subheader("Scan Info")
        st.metric("Scan Range Percent", f"{scan_metrics['scan_range_percent']} %")
        st.metric("Estimated Scan Time", f"{scan_metrics['scan_time_min']} min")
        st.metric("Max Allowed Exposure", f"{exposure_metrics['max_exposure']} ms")
        st.metric("Max Frame Rate", f"{exposure_metrics['max_frame_rate']} Hz")


def render_warning(exposure_metrics: dict) -> None:
    if not exposure_metrics["is_exposure_valid"]:
        st.warning(
            f"Exposure time too high for selected frame rate.\n"
            f"Maximum frame rate for this exposure time is "
            f"{exposure_metrics['max_frame_rate']} Hz."
        )
