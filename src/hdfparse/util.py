from rich.progress import track
import h5py


def count_files(filenames: list, measure: bool):
    """Sorting out the files with the data needed

    Args:
        filenames: list of file paths
        measure: boolean is measurement data should be used j
    Returns:
        c: number of files
        actual_files: filepaths with the data
    """
    c = 0
    actual_files = []
    lenfile = len(filenames)
    if not measure:
        for i in track(
            range(lenfile), description="Checking retrievals data..."
        ):
            with h5py.File(filenames[i], "r", swmr=True) as fh:
                datasets = list(fh.keys())
                measdata = ["kimra_data", "mira2_data"]
                retdata = [
                    dataset for dataset in datasets if dataset not in measdata
                ]
            if len(retdata) == 1:
                c += 1
                actual_files.append(filenames[i])
        return c, actual_files

    else:
        for i in track(
            range(lenfile), description="Checking measurement data..."
        ):
            with h5py.File(filenames[i], "r", swmr=True) as fh:
                datasets = list(fh.keys())
                if "kimra_data" in datasets or "mira2_data" in datasets:
                    c += 1
                    actual_files.append(filenames[i])
        return c, actual_files
