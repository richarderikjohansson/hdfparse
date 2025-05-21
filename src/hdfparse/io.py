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

    def get_path(self) -> Path:
        absolute_path = Path(self.input)
        relative_path = self.cwd / self.input

        if relative_path.exists():
            return relative_path

        elif absolute_path.exists():
            return absolute_path

        else:
            PathNotFound(f"Can not locate path from input'{self.input}'")

    def resolve_path(self) -> Path | List[Path]:
        path = self.get_path()
        dirpath = self.get_basedir()

        if self.export is not None:
            Path.mkdir(path.parent / "export", exist_ok=True)

            if dirpath == path:
                basedir = dirpath.parts[-1]
                subd = fast_scandir(dirpath)
                export_tree = [p.split("")]

    def get_basedir(self) -> Path:
        path = self.get_path()

        if path.is_file():
            return path.parent
        else:
            return path


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def parse_input(input: str) -> Path | List[Path]:
    basedir = Path.cwd()
    absolute_path = Path(input)
    path = basedir / input

    if not path.exists() or not absolute_path.exists():
        PathNotFound(f"'{path}' can not be resolved, check your input")

    if path.is_dir():
        # get paths to all files
        #
        pass
    elif path.is_file() and path.suffix.lower() == ".hdf5":
        pass
    else:
        pass


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
