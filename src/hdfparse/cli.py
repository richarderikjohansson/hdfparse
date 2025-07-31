import argparse
from .io import check_if_file_exists, read_file
from .plot import plot_spectra, plot_vmr, plot_avk, plot_jacobian

allowed_units = ["spectra", "vmr", "avk", "jacobian"]


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("filename", type=str, help="HDF5 file to read")
    parser.add_argument("unit", type=str,
                        help="Unit to plot and/or export. Allowed is 'spectra', 'vmr', 'avk' and 'jacobian'")

    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()

    if check_if_file_exists(args.filename):
        data = read_file(args.filename)

    if args.plot:
        match args.unit:
            case "spectra":
                plot_spectra(filename=args.filename, data=data)

            case "vmr":
                plot_vmr(filename=args.filename, data=data)

            case "avk":
                plot_avk(filename=args.filename, data=data)

            case "jacobian":
                plot_jacobian(filename=args.filename, data=data)


if __name__ == "__main__":
    main()
