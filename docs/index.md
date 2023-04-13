---
hide:
  - navigation
---

# NTFY LITE

**ntfy_lite** is a minimalistic python API for sending [ntfy](https://ntfy.sh) notifications.

It comes with a **Handler** for the [logging package](https://docs.python.org/3/library/logging.html).



Basic usage:

```python
import ntfy_lite as ntfy

ntfy.push(
  "my topic", priority=ntfy.Priority.DEFAULT, message="my message"
)
```