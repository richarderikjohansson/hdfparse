import argparse
from .io import check_if_file_exists, read_file, save_matlab
from .plot import Figures

allowed_units = ["spectra", "vmr", "avk", "jacobian"]


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("filename", type=str, help="HDF5 file to read")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()

    if check_if_file_exists(args.filename):
        data = read_file(args.filename)

    if args.plot:
        obj = Figures(filename=args.filename, data=data)
        obj.plot_spectra()
        obj.plot_vmr()
        obj.plot_avk()
        obj.plot_jacobian()

    if args.export:
        save_matlab(filename=args.filename, data=data)


if __name__ == "__main__":
    main()
