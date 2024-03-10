from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize


class RadarChartConfig(NamedTuple):
    angles: List[float]
    colors: List[str]
    highest_score: Optional[int] = None
    gridlines: bool = True
    label_offset: float = -0.05
    legend: bool = True
    legend_bbox_to_anchor: tuple = (0.7, 1.3)
    normalize: bool = True
    radial_labels: bool = True
    theta_direction: int = -1
    theta_offset: float = np.pi / 2
    yticklabels: bool = True


def draw_radar_chart(
    ax: plt.Axes,
    values: np.ndarray,
    config: RadarChartConfig,
    label: str,
) -> None:
    angles = config.angles
    colors = config.colors
    highest_score = config.highest_score
    gridlines = config.gridlines
    label_offset = config.label_offset
    normalize = config.normalize
    radial_labels = config.radial_labels
    theta_direction = config.theta_direction
    theta_offset = config.theta_offset
    yticklabels = config.yticklabels

    if normalize:
        vmin = 0
        vmax = max(values)
        norm = Normalize(vmin=vmin, vmax=vmax)
        values = norm(values)

    ax.fill(angles, values, color=colors[0], alpha=0.25)
    ax.plot(angles, values, color=colors[0], linewidth=2)

    if radial_labels:
        ax.set_rlabel_position(180)
        ax.set_yticks([])

        if highest_score is not None:
            ax.set_ylim(top=highest_score)

            if gridlines:
                for y in np.arange(0, highest_score + 1, 1):
                    if y != highest_score:
                        ax.plot(
                            angles,
                            [y] * len(angles),
                            color="gray",
                            linewidth=0.5,
                            linestyle=":",
                        )

                        if yticklabels:
                            ax.text(
                                angles[0],
                                y + 0.2,
                                str(int(y)),
                                color="black",
                                size=9,
                                horizontalalignment="center",
                                verticalalignment="center",
                            )

    ax.set_theta_offset(theta_offset)
    ax.set_theta_direction(theta_direction)

    if label is not None:
        ax.plot(angles, [0] * len(angles), color="gray", linewidth=0.5, linestyle="--")
        ax.text(
            angles[0],
            0.5,
            label,
            size=10,
            horizontalalignment="center",
            verticalalignment="center",
            color="black",
            transform=ax.transData.transform((0, 0)),
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
        )

    ax.spines["polar"].set_visible(False)


def save_combined_radar_chart(
    categories: Dict[str, Dict[str, Any]],
    save_path: str | Path,
    config: Optional[RadarChartConfig] = None,
) -> None:
    categories = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in categories.items()}
    if not all(categories.values()):
        raise Exception("No data to plot")

    labels = np.array(
        list(next(iter(categories.values())).keys())
    )  # We use the first category to get the keys
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[
        :1
    ]  # Add the first angle to the end of the list to ensure the polygon is closed

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    if config is None:
        config = RadarChartConfig(
            angles=angles,
            colors=[
                "#1f77b4",
                "#ff7f0e",
                "#2ca02c",
                "#d62728",
                "#9467bd",
                "#8c564b",
                "#e377c2",
                "#7f7f7f",
                "#bcbd22",
                "#17becf",
            ],
            highest_score=7,
            gridlines=True,
            label_offset=-0.05,
            legend=True,
            legend_bbox_to_anchor=(0.7, 1.3),
            normalize=True,
            radial_labels=True,
            theta_direction=-1,
            theta_offset=np.pi / 2,
            yticklabels=True,
        )

    cmap = plt.cm.get_cmap("nipy_spectral", len(categories))  # type: ignore
    colors = [cmap(i) for i in range(len(categories
