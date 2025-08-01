from pathlib import Path
import h5py
import os
from scipy.io import savemat


def check_if_file_exists(filename: str) -> bool:
    file = Path(filename)
    return file.exists()


def read_file(filename: str) -> dict:
    with h5py.File(filename, "r") as fh:
        datasets = list(fh.keys())
        measdata = ["kimra_data", "mira2_data"]
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


def save_matlab(filename: str, data: dict):
    basedir = Path(filename).parent
    export = basedir / "export"

    if not export.exists():
        os.mkdir(export)

    filename = Path(filename).name.split(".")[0] + ".mat"
    savemat(file_name=export / filename, mdict=data, oned_as="column")


def mk_figsdir(filename: str):
    basedir = Path(filename).parent
    figsdir = basedir / "figs"

    if not figsdir.exists():
        os.mkdir(figsdir)

    return figsdir
