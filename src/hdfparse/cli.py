import argparse
from .io import check_if_file_exists, read_file, save_matlab
from .plot import RetFigs, MeasFigs
from tqdm import tqdm


def main():
    """Entry point for the CLI"""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("filename", nargs="+", help="HDF5 file to read")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--measure", action="store_true")
    args = parser.parse_args()

    if args.plot and args.export:
        desc = "Plotting and exporting data"
    elif args.plot and not args.export:
        desc = "Plotting data"
    elif args.export and not args.plot:
        desc = "Exporting data"
    else:
        desc = "Not doing anything"

    for filename in tqdm(args.filename, desc=desc):
        if check_if_file_exists(filename):
            data = read_file(filename=filename, measure=args.measure)

        if data == {}:
            tqdm.write(f"No retrieval found in {filename}")
            continue

        if args.plot:
            if not args.measure:
                obj = RetFigs(filename=filename, data=data)
                obj.plot_spectra()
                obj.plot_vmr()
                obj.plot_avk()
                obj.plot_jacobian()
            else:
                obj = MeasFigs(filename=filename, data=data)
                obj.plot_spectra()

        if args.export:
            save_matlab(filename=filename, data=data)


if __name__ == "__main__":
    main()
