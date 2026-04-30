import streamlit as st
from settings import CAMERA_POSITION, SPATIAL_PIXEL, FTT
from src.data_loader import load_data
from src.regression_model import train_regression_model
from src.calculation_helpers import build_calibration_table, get_exposure_metrics, get_scan_metrics
from interface.inputs import render_sidebar_inputs
from interface.results import render_results
from interface.warning import render_warning

st.set_page_config(
    page_title="Camera Calibration Tool",
    page_icon="📷",
    layout="wide"
)


def main():
    st.title("📷 Camera Calibration Tool")
    st.caption("Refactored from original R script by Christoph Butz")

    df = load_data(CAMERA_POSITION)
    model = train_regression_model(df)
    inputs = render_sidebar_inputs()

    calibration_table = build_calibration_table(
        model=model,
        target_fov=inputs["fov"],
        table_position=inputs["table_position"],
        frame_rate=inputs["frame_rate"],
        spatial_pixel=SPATIAL_PIXEL
    )

    exposure_metrics = get_exposure_metrics(
        exposure_time=inputs["exposure_time"],
        frame_rate=inputs["frame_rate"],
        ftt=FTT
    )

    scan_metrics = get_scan_metrics(
        core_length=inputs["core_length"],
        calibration_table=calibration_table
    )

    render_results(calibration_table, scan_metrics, exposure_metrics, inputs)
    render_warning(exposure_metrics)

    with st.expander("Calibration Source Data"):
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
