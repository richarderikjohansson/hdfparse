import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np


def calculate_mr(avk) -> np.ndarray:
    mr = np.array([sum(row) for row in avk])
    return mr


def plot_spectra(filename, data):
    frequency = data["f_backend"] / 1e9
    spectra = data["y"]

    gs = GridSpec(1, 1)
    fig = plt.figure()

    ax = fig.add_subplot(gs[0, 0])
    ax.minorticks_on()
    ax.set_title(f"Spectra from {filename}")
    ax.set_xlabel(r"$\nu$ [GHz]")
    ax.set_ylabel(r"$T_B$ [K]")
    ax.grid(which="both", alpha=0.2)
    ax.plot(frequency, spectra)

    plt.show()


def plot_vmr(filename, data):
    pressure = data["p_grid"] / 1e2
    plen = len(pressure)
    apriori = data["vmr_field"][0, :, 0, 0] * 1e6
    vmr = data["x"][0:plen] * apriori

    gs = GridSpec(1, 1)
    fig = plt.figure()

    ax = fig.add_subplot(gs[0, 0])
    plt.gca().invert_yaxis()
    ax.minorticks_on()
    ax.set_title(f"Volume Mixing Ratio from {filename}")
    ax.set_xlabel(r"VMR [ppmv]")
    ax.set_ylabel(r"Pressure [hPa]")
    ax.grid(which="both", alpha=0.2)
    ax.semilogy(apriori, pressure, color="black", label="apriori")
    ax.semilogy(vmr, pressure, label="Retrived")

    ax.legend()

    plt.show()


def plot_avk(filename, data):
    pressure = data["p_grid"] / 1e2
    plen = len(pressure)
    avk = data["avk"][0:plen, 0:plen]
    mr = calculate_mr(avk)

    gs = GridSpec(1, 1)
    fig = plt.figure()

    ax = fig.add_subplot(gs[0, 0])
    plt.gca().invert_yaxis()
    ax.minorticks_on()
    ax.set_title(f"Averaging Kernels from {filename}")
    ax.set_xlabel(r"AVK [-]")
    ax.set_ylabel(r"Pressure [hPa]")
    ax.grid(which="both", alpha=0.2)
    ax.semilogy(
        mr, pressure, color="red", label="Measurement Response", linewidth=2
    )

    for row in avk:
        ax.semilogy(row, pressure)

    ax.legend()
    plt.show()


def plot_jacobian(filename, data):
    pressure = data["p_grid"] / 1e2
    plen = len(pressure)
    frequency = data["f_backend"] / 1e9
    jacobian = data["jacobian"][:, 0:plen]
    print(len(jacobian))
    X, Y = np.meshgrid(frequency, pressure)

    gs = GridSpec(1, 1)
    fig = plt.figure()
    ax = fig.add_subplot(gs[0, 0])
    ax.set_title(f"Jacobian from {filename}")
    ax.set_ylabel(r"Pressure [hPa]")
    ax.set_xlabel(r"$\nu$ [GHz]")

    plt.gca().invert_yaxis()
    plt.yscale("log")
    cf = ax.contourf(X, Y, jacobian.transpose(), cmap="jet")
    plt.colorbar(cf, ax=ax)
    plt.show()
