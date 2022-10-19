""" ntfy lite: notification push examples """

import tempfile
from pathlib import Path
import ntfy_lite as ntfy

topic = "ntfy_lite_demo"  # or something else
email = None  # write your email here if you wish


def run():

    # note: icon does not seem to work, but that does not seem to be an issue with ntfy_lite
    #       as the icon example from the ntfy documentation also do not work

    # basic usage, most arguments are optional
    ntfy.push(
        topic,
        "ntfy_lite demo 1 - basic usage",
        message="this is a demo from ntfy_lite",
        tags=["butterfly", "cat"],
        icon="https://styles.redditmedia.com/t5_32uhe/styles/communityIcon_xnt6chtnr2j21.png",
        actions=[
            ntfy.ViewAction(
                label="open ntfy.sh website", url="https://ntfy.sh", clear=False
            ),
            ntfy.ViewAction(
                label="open ntfy_lite github",
                url="https://github.com/MPI-IS/ntfy_lite",
                clear=False,
            ),
        ],
        email=email,
    )

    # sending an attachment instead of a message
    with tempfile.TemporaryDirectory() as tmp:

        filepath = Path(tmp) / "ntfy_lite_demo.txt"
        with open(filepath, "w") as f:
            f.write("content of ntfy_lite_demo.txt")

        # note: you can not specify both a message and a
        #       filepath
        ntfy.push(
            topic,
            "ntfy_lite demo 2 - file attachment",
            filepath=filepath,
            tags="file_folder",
            email=email,
        )

    # delayed notificiation / scheduled delivery
    ntfy.push(
        topic,
        "ntfy_lite demo 2 - delayed notification",
        message="one minute delayed notification",
        at="1m",  # see: https://ntfy.sh/docs/publish/#scheduled-delivery
        tags="hourglass",
        email=email,
    )


if __name__ == "__main__":

    try:
        run()
    except Exception as e:
        print(f"failed to send the notification: {e}")
    else:
        print(f"notifications sent, visit https://ntfy.sh/{topic}")