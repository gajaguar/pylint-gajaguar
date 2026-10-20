import functools

# pylint: disable=unused-import


@functools.cache
# pylint: disable=unused-import
async def decorated():
    # pylint: disable=unused-import
    value = 1  # pylint: disable=unused-import
    return value


def with_match(value):
    match value:
        # pylint: disable=unused-import
        case 1:  # pylint: disable=unused-import
            pass
        case _:
            pass


NAME = "x"
F_STRING = f"{NAME} # pylint: disable=unused-import"
F_MULTI = f"""{NAME}
# pylint: disable=unused-import
"""  # pylint: disable=unused-import
F_NESTED = f"{'#'} {NAME}"  # pylint: disable=unused-import
F_NESTED_DOUBLE = f"{"#"} {NAME}"  # pylint: disable=unused-import
F_FORMAT_SPEC = f"{NAME:>{10}}"  # pylint: disable=unused-import
F_FORMAT_SPEC_AFTER = f"{NAME:#>10}"  # pylint: disable=unused-import
RAW_F = rf"\{NAME}"  # pylint: disable=unused-import
