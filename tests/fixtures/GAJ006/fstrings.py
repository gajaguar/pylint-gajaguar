CFG = {"a": 1, "k": 2}
NAME = "x"
PRAGMA = "# pylint: disable=unused-import"
INLINE_F = f"{CFG["a"]}"  # pylint: disable=unused-import
INLINE_SINGLE = f'{CFG['k']}'  # pylint: disable=unused-import
INLINE_DEEP = f"{f"{f"{NAME}"}"}"  # pylint: disable=unused-import
INLINE_HASH = f"{'#'}{{#}}"  # pylint: disable=unused-import
INLINE_SPEC = f"{NAME!r:{"#"}>4}"  # pylint: disable=unused-import
INLINE_TEXT = f"{NAME} # pylint: disable=unused-import"
INLINE_BRACES = f"{{# pylint: disable=unused-import}}"
F_TAIL = f"""{CFG["a"]}
"""  # pylint: disable=unused-import
F_THEN_PLAIN = f"{CFG["a"]}" """text
"""  # pylint: disable=unused-import
SINGLE_THEN_PLAIN = f'{CFG['k']}' '''text
'''  # pylint: disable=unused-import
HASH_THEN_PLAIN = f"{'#'}{{#}}" """text
"""  # pylint: disable=unused-import
SPEC_THEN_PLAIN = f"{NAME!r:{"#"}>4}" """text
"""  # pylint: disable=unused-import
QUOTE_THEN_PLAIN = f"{'"'}{"'"}" """text
"""  # pylint: disable=unused-import
NAMED_THEN_PLAIN = f"\N{LEFT CURLY BRACKET}{CFG["a"]}" """text
"""  # pylint: disable=unused-import
RAW_THEN_PLAIN = rf"\{CFG["a"]}" """text
"""  # pylint: disable=unused-import
NESTED_THEN_PLAIN = f"{f"{f"{NAME}"}"}" """text
"""  # pylint: disable=unused-import
PLAIN_THEN_F = """text
""" f"{CFG["a"]}"  # pylint: disable=unused-import
F_THEN_MULTI = f"""{CFG["a"]}
""" """text
"""  # pylint: disable=unused-import
PLAIN_THEN_F_TAIL = "a" f"""{CFG["a"]}
"""  # pylint: disable=unused-import
MULTI_FIELD = f"{CFG[
    "a"
]}"  # pylint: disable=unused-import
MULTI_FIELD_TAIL = f"{CFG[
    "a"
]}" """text
"""  # pylint: disable=unused-import
