import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from settings import ARROW_DISTANCE, MAX_SCAN_LENGTH


def get_speed_fov_candidates(
        frame_rate: float,
        spatial_pixel: int,
        speed_min: float = 0.05,
        speed_max: float = 10.0,
        step: float = 0.05
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate sample tray speed settings and corresponding usable FOV values.
    """
    speed = np.arange(speed_min, speed_max + step, step)
    usable_fov = (speed / frame_rate) * spatial_pixel
    return speed, usable_fov


def find_nearest_indices(values: np.ndarray, target: float) -> list[int]:
    """
    Find the nearest index and return [previous, current, next].
    """
    idx = int(np.argmin(np.abs(values - target)))
    return [
        max(idx - 1, 0),
        idx,
        min(idx + 1, len(values) - 1)
    ]


def predict_arrow_positions(
        model: LinearRegression,
        fov: float,
        table_position: float
) -> tuple[float, float]:
    """
    Predict Arrow 1 and derive Arrow 2.
    """
    arrow_1 = round(model.predict([[fov, table_position]])[0], 2)
    arrow_2 = round(arrow_1 + ARROW_DISTANCE, 2)
    return arrow_1, arrow_2


def build_calibration_table(
        model: LinearRegression,
        target_fov: float,
        table_position: float,
        frame_rate: float,
        spatial_pixel: int
) -> pd.DataFrame:
    """
    Build the result table with 3 candidate FOVs around the closest match.
    """
    speed, usable_fov = get_speed_fov_candidates(frame_rate, spatial_pixel)
    indices = find_nearest_indices(usable_fov, target_fov)

    results = []
    for i in indices:
        selected_fov = float(usable_fov[i])
        arrow_1, arrow_2 = predict_arrow_positions(model, selected_fov, table_position)

        results.append({
            "Field of View": round(selected_fov, 2),
            "Arrow 1": arrow_1,
            "Arrow 2": arrow_2,
            "Speed": round(float(speed[i]), 2)
        })

    return pd.DataFrame(results)


def get_exposure_metrics(
        exposure_time: float,
        frame_rate: float,
        ftt: float
) -> dict:
    """
    Calculate exposure metrics and validate current exposure time.
    """
    max_exposure = round(((1 / frame_rate) * 1000) - ftt, 2)
    max_frame_rate = round(1 / ((exposure_time + ftt) / 1000), 2)

    return {
        "max_exposure": max_exposure,
        "max_frame_rate": max_frame_rate,
        "is_exposure_valid": exposure_time <= max_exposure
    }


def get_scan_metrics(
        core_length: float,
        calibration_table: pd.DataFrame
) -> dict:
    """
    Assumes the middle row is the best candidate.
    """
    scan_range_percent = round(100 * ((core_length + 110) / MAX_SCAN_LENGTH), 2)

    selected_speed = calibration_table.iloc[1]["Speed"]
    scan_time_min = round(((core_length + 200) / selected_speed) / 60, 2)

    return {
        "scan_range_percent": scan_range_percent,
        "scan_time_min": scan_time_min
    }
