import pathlib
import h5py


def check_if_file_exists(filename: str) -> bool:
    file = pathlib.Path(filename)
    return file.exists()


def read_file(filename: str) -> dict:
    with h5py.File(filename, 'r') as fh:
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
