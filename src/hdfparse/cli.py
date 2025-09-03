import argparse
from .io import read_file, save_matlab
from .plot import RetFigs, MeasFigs
from .util import count_files
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor


def plot_task(progress, task_id, args, actual_files):
    """Plotting task

    Args:
        progress: which progress it is assigned to
        task_id: ID of the task
        args: parsed input arguments
        actual_files: files that have the necessary data
    """
    if not args.measure:
        for file in actual_files:
            data = read_file(file, args.measure)
            obj = RetFigs(filename=file, data=data)
            obj.plot_spectra()
            obj.plot_vmr()
            obj.plot_avk()
            obj.plot_jacobian()
            progress.update(task_id, advance=1)
    else:
        for file in actual_files:
            data = read_file(file, args.measure)
            obj = MeasFigs(filename=file, data=data)
            obj.plot_spectra()
            progress.update(task_id, advance=1)


def export_task(progress, task_id, args, actual_files):
    """Exporting task

    Args:
        progress: which progress it is assigned to
        task_id: ID of the task
        args: parsed input arguments
        actual_files: files that have the necessary data
    """
    for file in actual_files:
        data = read_file(file, args.measure)
        save_matlab(filename=file, data=data)
        progress.update(task_id, advance=1)


def main():
    """Entry point for the CLI"""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("filename", nargs="+", help="HDF5 file to read")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--measure", action="store_true")
    args = parser.parse_args()

    run_cli(args=args)


def run_cli(args):
    """cli runner

    Args:
        args: arguments parsed from command line
    """
    with Progress() as progress:
        c, actual_files = count_files(
            filenames=args.filename, measure=args.measure
        )
        futures = []
        with ThreadPoolExecutor() as executor:
            if args.plot:
                plot_id = progress.add_task("[cyan]Plotting...", total=c)
                futures.append(
                    executor.submit(
                        plot_task, progress, plot_id, args, actual_files
                    )
                )
            if args.export:
                export_id = progress.add_task("[magenta]Exporting...", total=c)
                futures.append(
                    executor.submit(
                        export_task, progress, export_id, args, actual_files
                    )
                )
            for f in futures:
                f.result()


if __name__ == "__main__":
    main()
