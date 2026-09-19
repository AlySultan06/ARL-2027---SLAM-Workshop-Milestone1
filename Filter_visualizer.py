import matplotlib.pyplot as plt
import numpy as np


def gaussian_pdf(x, mean, variance):
    """Calculates 1D Gaussian Probability Density Function values."""
    return (1.0 / np.sqrt(2.0 * np.pi * variance)) * np.exp(
        -0.5 * ((x - mean) ** 2) / variance
    )


def plot_1d_gaussians(
    x_pred, P_pred, z, R, x_upd, P_upd, state_idx=0, label="Position X"
):
    """Plots 1D Gaussian distributions for a single state variable slice."""

    mu_pred, var_pred = x_pred[state_idx, 0], P_pred[state_idx, state_idx]
    mu_meas, var_meas = z[state_idx, 0], R[state_idx, state_idx]
    mu_upd, var_upd = x_upd[state_idx, 0], P_upd[state_idx, state_idx]

    x_axis = np.linspace(min(mu_pred, mu_meas) - 6, max(mu_pred, mu_meas) + 6, 1000)

    pdf_pred = gaussian_pdf(x_axis, mu_pred, var_pred)
    pdf_meas = gaussian_pdf(x_axis, mu_meas, var_meas)
    pdf_upd = gaussian_pdf(x_axis, mu_upd, var_upd)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    # Distributions
    ax.plot(
        x_axis,
        pdf_pred,
        color="#007bff",
        linewidth=2.5,
        linestyle="--",
        label=f"Prediction: N({mu_pred:.2f}, {var_pred:.2f})",
    )
    ax.fill_between(x_axis, pdf_pred, color="#007bff", alpha=0.15)

    ax.plot(
        x_axis,
        pdf_meas,
        color="#dc3545",
        linewidth=2.5,
        linestyle=":",
        label=f"Measurement: N({mu_meas:.2f}, {var_meas:.2f})",
    )
    ax.fill_between(x_axis, pdf_meas, color="#dc3545", alpha=0.15)

    ax.plot(
        x_axis,
        pdf_upd,
        color="#28a745",
        linewidth=3.0,
        linestyle="-",
        label=f"Correction: N({mu_upd:.2f}, {var_upd:.2f})",
    )
    ax.fill_between(x_axis, pdf_upd, color="#28a745", alpha=0.25)

    # Mean lines
    ax.axvline(mu_pred, color="#007bff", linestyle="--", alpha=0.6)
    ax.axvline(mu_meas, color="#dc3545", linestyle=":", alpha=0.6)
    ax.axvline(mu_upd, color="#28a745", linestyle="-", alpha=0.8)

    ax.set_title(
        f"1D Gaussian Probability Density Fusion ({label})",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel(f"{label} (meters)", fontsize=11)
    ax.set_ylabel("Probability Density f(x)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", frameon=True, facecolor="white")

    plt.tight_layout()
    plt.show()
