from __future__ import annotations

from typing import TYPE_CHECKING

import astroid
from astroid.builder import AstroidBuilder

if TYPE_CHECKING:
    import pathlib

    from astroid.nodes import Module
    from astroid.nodes import NodeNG


def build_module_from_source(tmp_path: pathlib.Path, source: str) -> Module:
    path = tmp_path / "sample_module.py"
    path.write_text(source, encoding="utf-8")
    return AstroidBuilder(astroid.MANAGER).file_build(str(path))


def node_position(node: NodeNG) -> dict[str, int]:
    # pylint reports FunctionDef/ClassDef messages using node.position (the
    # header span), not the full node span (which includes the body).
    position = getattr(node, "position", None) or node
    return {
        "line": position.lineno if hasattr(position, "lineno") else node.fromlineno,
        "col_offset": position.col_offset,
        "end_line": position.end_lineno,
        "end_col_offset": position.end_col_offset,
    }
