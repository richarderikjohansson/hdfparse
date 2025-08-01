# hdfparse

Project develop with the Python project manager [Astral uv](https://docs.astral.sh/uv/) and the
CLI can be installed with this as well. The tool was developed to have a fast way to read and plot
retrieval data directly from the terminal. It can also export retrieval data to `.mat` format as 
well.

## Installing CLI

This tutorial is aimed to show how to install hdfparse with uv. If still have not installed uv on 
your machine see tutorial at [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/). To create 
a new environment for this tool, and also install all necessary dependencies uv have one single 
command for this and should be run from the project root:

```bash
uv sync
```

With this command is a virtual environment installed in `.venv`. To activate this you need to know 
which shell you are using. Most likely you are using `zsh` or `bash`. To activate the environment 
run:

```bash
source .venv/bin/activate
```

and if you are using `fish`

```fish
source .venv/bin/activate.fish
```

## Usage: Plotting

While in the environment that the tool is installed in and you have a `.hdf5` locally that contain
retrieval data you simply run:

```bash
hdfparse path/to/hdf5_file --plot
```

Where *path/to/hdf5_file* is the actual path to the file. Running this will plot:

* Volume Mixing Ratio together with the *apriori* used in the retrieval
* Measured and fitted spectra together with the residual
* Averaging Kernel as a line plot, with measurement response and Averaging Kernel as a contour
* Jacobian Matrix as a contour

These figures will be saved in a directory called `figs` and is located in the parent directory to 
the `.hdf5`.


## Usage: Exporting

As for the plotting functionality you have to be in the environment that the tool is installed in. To
export the retrieval data to `.mat` format you run the following:

```bash
hdfparse path/to/hdf5_file --export
```

That command export all current retrieval products from the file to a MATLAB file. As for the plotting 
a directory called `export` is created in the parent directory of the `.hdf5` file and the MATLAB file 
can be found there.

## Usage: Plotting and Exporting

Obviously you can plot and export at the same time and is done by running the following:

```bash
hdfparse path/to/hdf5_file --export --plot
```

And as for the single use of the two optional arguments will directories for the figures and the export 
be created in the parent directory to the `.hdf5` file.
