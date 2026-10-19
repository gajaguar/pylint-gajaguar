# pylint: disable=unused-import
import os  # pylint: disable=unused-import
# pylint: disable-next=unused-import
import sys

#pylint:disable=unused-import
#   pylint:   disable=unused-import
# pylint: disable = unused-import
# pylint : disable=unused-import
# pylint: enable=unused-import
# note # pylint: disable=unused-import
# pylint: disable=unused-import  # pylint: disable-next=unused-import
# pylint: disable-next=unused-import  # pylint: disable=unused-import
# pylint: disable=foo,bar
#PYLINT: disable=foo
# a comment about pylint: disable=foo
TEXT = "# pylint: disable=unused-import"
DOC = """text
# pylint: disable=unused-import
"""
TAIL = """text
"""  # pylint: disable=unused-import
TAIL_BYTES = b"""text
"""  # pylint: disable=unused-import
TAIL_NEXT = """text
"""
# pylint: disable=unused-import
CONTINUED = 1 + \
    2  # pylint: disable=unused-import
CALL = max(
    1,
    # pylint: disable=unused-import
    2,
)  # pylint: disable=unused-import
JOINED = """text
""" + "more"  # pylint: disable=unused-import
FORMATTED = f"""text {os}
"""  # pylint: disable=unused-import


def function():
    # pylint: disable=too-many-locals
    return [
        1,
        # pylint: disable=unused-import
    ]  # pylint: disable=unused-import


class Holder:
        # pylint: disable=too-few-public-methods
    pass
	# pylint: disable=unused-import
