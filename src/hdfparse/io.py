from pathlib import Path
import h5py
import os
from scipy.io import savemat


def check_if_file_exists(filename: str) -> bool:
    """Check if file exists

    Args:
        filename: path to the filename

    Returns:
        boolean if file exist
    """
    file = Path(filename)
    return file.exists()


def read_file(filename: str, measure: bool) -> dict:
    """Function to read HDF5 files

    Args:
        filename: path to the file
        measure: boolean if measurement data should be read

    Returns:
        dictionary containing data from HDF5 file
    """
    with h5py.File(filename, "r", swmr=True) as fh:
        datasets = list(fh.keys())
        measdata = ["kimra_data", "mira2_data"]
        if not measure:
            # this will not work for several retrievals
            retdata = [dataset for dataset in datasets if dataset not in measdata]

            try:
                data = fh[retdata[0]]
            except IndexError:
                return {}

            dct = {}

            for key in data.keys():
                if key != "config":
                    dct[key] = data[key][:]
            return dct
        else:
            if "kimra_data" in datasets:
                data = fh["kimra_data"]
            else:
                data = fh["mira2_data"]

            dct = {}
            for key in data.keys():
                if key != "config":
                    try:
                        dct[key] = data[key][:]
                    except ValueError:
                        dct[key] = data[key][()]
            return dct


def save_matlab(filename: str, data: dict):
    """Function to export data to MATLAB format

    Args:
        filename: path to filename
        data: data to be exported
    """
    basedir = Path(filename).parent
    export = basedir / "export"

    if not export.exists():
        os.mkdir(export)

    filename = Path(filename).name.split(".")[0] + ".mat"
    savemat(file_name=export / filename, mdict=data, oned_as="column")


def mk_figsdir(filename: str):
    """Function to create a directory for figures

    Args:
        filename: path to filename
    """
    basedir = Path(filename).parent
    figsdir = basedir / "figs"

    if not figsdir.exists():
        os.mkdir(figsdir)

    return figsdir


def format_tqdm_desc(plot: bool, export: bool) -> str:
    """Function to format the tqdm description

    Args:
        plot: boolean if plotting
        export: boolean if exporting

    Returns:
        string with the tqdm description
    """
    if plot and export:
        desc = "Plotting and exporting data"
    elif plot and not export:
        desc = "Plotting data"
    elif export and not plot:
        desc = "Exporting data"
    else:
        desc = "Not doing anything"

    return desc
