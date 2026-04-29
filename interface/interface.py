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
        exposure_metrics: dict,
        inputs: dict
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

    candidate_id = calibration_table["Calibration Candidate"].tolist()
    selected_candidate = st.selectbox("Select Calibration Candidate", candidate_id)
    selected_row = calibration_table[
        calibration_table["Calibration Candidate"] == selected_candidate
        ].iloc[0]

    selected_fov = float(selected_row["Field of View"])
    selected_speed = float(selected_row["Speed"])
    selected_arrow_1 = float(selected_row["Arrow 1"])
    selected_arrow_2 = float(selected_row["Arrow 2"])

    scan_description_text = (
        f"spectral_binning: 2, "
        f"fov: {selected_fov:.2f}, "
        f"aperture: 1.9, "
        f"exposure: {inputs['exposure_time']:.1f}, "
        f"speed: {selected_speed:.2f}, "
        f"frame_rate: {inputs['frame_rate']:.1f}, "
        f"table_position: {inputs['table_position']:.2f}, "
        f"arrow_1: {selected_arrow_1:.2f}, "
        f"arrow_2: {selected_arrow_2:.2f}, "
        f"scanning_range: {inputs['core_length']:.1f}"
    )

    st.subheader("Scan Description")
    st.code(scan_description_text, language="python")


def render_warning(exposure_metrics: dict) -> None:
    if not exposure_metrics["is_exposure_valid"]:
        st.warning(
            f"Exposure time too high for selected frame rate.\n"
            f"Maximum frame rate for this exposure time is "
            f"{exposure_metrics['max_frame_rate']} Hz."
        )
