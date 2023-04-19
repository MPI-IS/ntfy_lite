![unit tests](https://github.com/MPI-IS/ntfy_lite/actions/workflows/tests.yaml/badge.svg)
[![documentation](https://github.com/MPI-IS/ntfy_lite/actions/workflows/mkdocs.yaml/badge.svg)](https://mpi-is.github.io/ntfy_lite/)


# NTFY LITE

**ntfy_lite** is a minimalistic python API for sending [ntfy](https://ntfy.sh) notifications.

It comes with a **Handler** for the [logging package](https://docs.python.org/3/library/logging.html).

See the full documentation [here](https://mpi-is.github.io/ntfy_lite/).

See the source [here](https://github.com/MPI-IS/ntfy_lite).

## Installation

from source:

```bash
git clone https://github.com/MPI-IS/ntfy_lite.git
cd ntfy_lite
pip install .
```

from pypi:
```bash
pip install ntfy_lite
```

## Usage

The two following examples cover the full API.
You may also find the code in the demos folder of the sources.

### pushing notifications
https://github.com/MPI-IS/ntfy_lite/blob/da5750eed1ed58eacf4ff1bb1498586b41242f70/demos/ntfy_push.py#L1-L73

### logging handler

https://github.com/MPI-IS/ntfy_lite/blob/52fc7f008fdac3f735d39dd01064a0aa5b751e00/demos/ntfy_logging.py#L1-L146

## Limitation

No check regarding ntfy [limitations](https://ntfy.sh/docs/publish/#limitations) is performed before notifications are sent.

## Copyright

© 2020, Max Planck Society - Max Planck Institute for Intelligent Systems

