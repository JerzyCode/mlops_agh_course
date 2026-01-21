import base64
import io
from typing import Annotated, List, Optional

import matplotlib.pyplot as plt
from fastmcp import FastMCP

mcp = FastMCP("visualization-server")


@mcp.tool()
def line_plot(
    x_data: Annotated[
        List[float], "List of X numbers. Provide ONLY raw numbers, NO python code."
    ],
    y_data: Annotated[
        List[float],
        "List of Y numbers. Provide ONLY raw numbers. Calculate values before sending.",
    ],
    title: Optional[str] = "Line Plot",
    x_label: Optional[str] = "X-axis",
    y_label: Optional[str] = "Y-axis",
    legend: bool = False,
) -> str:
    """Creates a line plot. Data must be pre-calculated numerical lists."""
    plt.switch_backend("Agg")
    plt.figure(figsize=(10, 6))

    plt.plot(x_data, y_data, label=f"{y_label} vs {x_label}")

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if legend:
        plt.legend()

    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)
