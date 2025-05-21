from pathlib import Path
import tomllib
from importlib.resources import files
from typing import Any, List
import os


class PathNotFound(Exception):
    def __init__(self, message):
        self.message = message


class ParseInput:
    def __init__(self, inp, export):
        self.input = inp
        self.export = export
        self.cwd = Path.cwd()
        self.exportdir = "export"

    def get_path(self):
        absolute_path = Path(self.input)
        relative_path = self.cwd / self.input

        if relative_path.exists():
            path = relative_path
        elif absolute_path.exists():
            path = absolute_path
        else:
            PathNotFound(f"Can not locate path from input'{self.input}'")

        self.path = path

    def resolve_path(self):
        self.get_dirpath()

        if self.export is not None:
            Path.mkdir(self.path.parent / self.exportdir, exist_ok=True)

            if self.dirpath == self.path:
                basedir = self.dirpath.parts[-1]
                subd = get_dirtrees(basedir)
                export_paths = []

                for sub in subd:
                    export_path = self.path.parent / self.exportdir / sub 
                    export_paths.append(export_path)
                    Path.mkdir(export_path)
            else:
                export_paths = self.path.parent / self.exportdir

        self.files = self.find_input_files()
        self.export_paths = export_paths
            
    def get_dirpath(self):
        self.get_path()

        if self.path.is_file():
            dirpath = self.path.parent
        else:
            dirpath = self.path

        self.dirpath = dirpath

    def find_input_files(self):
        if self.path.is_file():
            self.files = self.path
        else:
            files = Path.rglob(".hdf5")
            self.files = files


def get_dirtrees(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(get_dirtrees(dirname))
    return subfolders


def load_config() -> dict[str, Any]:
    """Configuration file loader

    Returns:
        Dictionary containing configurations
    """
    path = files("hdfparse.conf").joinpath("conf.toml")
    with path.open("rb") as f:
        return tomllib.load(f)


def read_hdf5(file: Path) -> dict:
    """Function to read HDF5 files

    Args:
        file: Path to file

    Returns:
        Dictionary with data
    """
    data = {i: i for i in range(1, 2)}
    return data
