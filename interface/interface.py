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
    st.subheader("Calibration Result")
    st.dataframe(calibration_table, use_container_width=True, hide_index=True)

    st.subheader("Scan Information")
    other_metrics_col, scan_time_col = st.columns(2)

    with other_metrics_col:
        st.metric("Scan Range Percent", f"{scan_metrics['scan_range_percent']} %")
        st.metric("Max Exposure", f"{exposure_metrics['max_exposure']} ms")
        st.metric("Max Frame Rate", f"{exposure_metrics['max_frame_rate']} Hz")

    with scan_time_col:
        for i, scan_time in enumerate(scan_metrics["scan_times"], start=1):
            st.metric(f"Estimated Scan Time {i}", f"{scan_time} min")


def render_warning(exposure_metrics: dict) -> None:
    if not exposure_metrics["is_exposure_valid"]:
        st.warning(
            f"Exposure time too high for selected frame rate.\n"
            f"Maximum frame rate for this exposure time is "
            f"{exposure_metrics['max_frame_rate']} Hz."
        )
