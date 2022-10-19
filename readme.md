![unit tests](https://github.com/MPI-IS/ntfy_lite/actions/workflows/tests.yaml/badge.svg)

# NTFY LITE

**ntfy_lite** is a minimalistic python API for sending [ntfy](https://ntfy.sh) notifications.

It comes with a **Handler** for the [logging package](https://docs.python.org/3/library/logging.html).


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

https://github.com/MPI-IS/ntfy_lite/blob/079f110601e46261e81d7006cf8def0322fd0fb1/demos/ntfy_push.py#L1-L71


### logging handler

https://github.com/MPI-IS/ntfy_lite/blob/079f110601e46261e81d7006cf8def0322fd0fb1/demos/ntfy_logging.py#L1-L146

## Limitation

No check regarding ntfy [limitations](https://ntfy.sh/docs/publish/#limitations) is performed before notifications are sent.

## Copyright

© 2020, Max Planck Society - Max Planck Institute for Intelligent Systems

