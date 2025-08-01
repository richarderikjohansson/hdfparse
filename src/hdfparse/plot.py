import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from .io import mk_figsdir, Path
import matplotlib as mpl


def calculate_mr(avk) -> np.ndarray:
    mr = np.array([sum(row) for row in avk])
    return mr


class Figures:
    def __init__(self, filename: str, data: dict):
        self.figsdir = mk_figsdir(filename=filename)
        self.filename = Path(filename).name
        self.data = data

    def plot_spectra(self):
        frequency = self.data["f_backend"] / 1e9
        spectra = self.data["y"]
        fit = self.data["yf"]

        gs = GridSpec(1, 1)
        fig = plt.figure()

        ax = fig.add_subplot(gs[0, 0])
        ax.minorticks_on()
        ax.set_title(f"Spectra from {self.filename}")
        ax.set_xlabel(r"$\nu$ [GHz]")
        ax.set_ylabel(r"$T_B$ [K]")
        ax.grid(which="both", alpha=0.2)
        ax.plot(frequency, spectra, label="Measurement", color="black")
        ax.plot(frequency, fit, label="Fit", color="red")
        plt.savefig(self.figsdir / "spectra.pdf")
        plt.close()

    def plot_vmr(self):
        pressure = self.data["p_grid"] / 1e2
        plen = len(pressure)
        apriori = self.data["vmr_field"][0, :, 0, 0] * 1e6
        vmr = self.data["x"][0:plen] * apriori

        gs = GridSpec(1, 1)
        fig = plt.figure()

        ax = fig.add_subplot(gs[0, 0])
        plt.gca().invert_yaxis()
        ax.minorticks_on()
        ax.set_title(f"Volume Mixing Ratio from {self.filename}")
        ax.set_xlabel(r"VMR [ppmv]")
        ax.set_ylabel(r"Pressure [hPa]")
        ax.grid(which="both", alpha=0.2)
        ax.semilogy(apriori, pressure, color="black", label="apriori")
        ax.semilogy(vmr, pressure, label="Retrived")
        ax.legend()
        plt.savefig(self.figsdir / "vmr.pdf")
        plt.close()

    def plot_avk(self):
        pressure = self.data["p_grid"] / 1e2
        plen = len(pressure)
        avk = self.data["avk"][0:plen, 0:plen]
        mr = calculate_mr(avk)

        my_map = mpl.colormaps.get_cmap("jet")
        cmapv = np.linspace(0, 1, len(pressure))
        sm = plt.cm.ScalarMappable(
            cmap=my_map,
            norm=plt.Normalize(
                vmin=pressure[0],
                vmax=pressure[-1]
            )
        )

        gs = GridSpec(1, 1)
        fig = plt.figure()

        ax = fig.add_subplot(gs[0, 0])
        plt.gca().invert_yaxis()
        ax.minorticks_on()
        ax.set_title(f"Averaging Kernels from {self.filename}")
        ax.set_xlabel(r"AVK [-]")
        ax.set_ylabel(r"Pressure [hPa]")
        ax.grid(which="both", alpha=0.2)
        ax.semilogy(
            mr,
            pressure,
            color="red",
            label="Measurement Response",
            linewidth=2,
        )

        for i, row in enumerate(avk):
            ax.semilogy(row, pressure, color=my_map(cmapv[i]))

        plt.colorbar(
            sm,
            ax=ax,
            label="Pressure Level [hPa]"
        )

        ax.legend()
        plt.savefig(self.figsdir / "avk_line.pdf")
        plt.close()

        X, Y = np.meshgrid(pressure, pressure)
        plims = (max(pressure), min(pressure))
        gs = GridSpec(1, 1)

        fig = plt.figure()
        ax = fig.add_subplot(gs[0, 0])
        ax.set_xlim(plims)
        ax.set_ylim(plims)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylabel(r"Pressure [hPa]")
        ax.set_xlabel(r"Pressure [hPa]")
        ax.set_title(f"Averaging Kernels from {self.filename}")
        cf = ax.contourf(X, Y, avk, cmap="jet")
        plt.colorbar(cf, ax=ax, label="Averaging Kernels")
        fig.savefig(self.figsdir / "avk_cf.pdf")
        plt.close()

    def plot_jacobian(self):
        pressure = self.data["p_grid"] / 1e2
        plen = len(pressure)
        frequency = self.data["f_backend"] / 1e9
        jacobian = self.data["jacobian"][:, 0:plen]
        X, Y = np.meshgrid(frequency, pressure)

        gs = GridSpec(1, 1)
        fig = plt.figure()
        ax = fig.add_subplot(gs[0, 0])
        ax.set_title(f"Jacobian from {self.filename}")
        ax.set_ylabel(r"Pressure [hPa]")
        ax.set_xlabel(r"$\nu$ [GHz]")

        plt.gca().invert_yaxis()
        plt.yscale("log")
        cf = ax.contourf(X, Y, jacobian.transpose(), cmap="jet")
        plt.colorbar(cf, ax=ax)
        plt.savefig(self.figsdir / "jacobian.pdf")
        plt.close()
