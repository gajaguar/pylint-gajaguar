use ferrolint_plugin_sdk::prelude::*;

use crate::testing::{from_line, is_test_function, section_markers};

pub const CODE: &str = "GAJ015";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "test-no-extra-comments",
        "A test body carries a comment that is not a section marker.",
    )
    .pylint("W9015", "gajaguar-test-no-extra-comments")
}

const PRAGMA_PREFIXES: [&str; 6] = [
    "# noqa",
    "# pylint:",
    "# type:",
    "# mypy:",
    "# fmt:",
    "# ruff:",
];

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !is_test_function(node, cx) {
        return;
    }
    let first = from_line(node, cx);
    let last = node.range.end.line as usize;
    let allowed = section_markers(cx);
    let found: Vec<Diagnostic> = cx
        .comments()
        .iter()
        .filter_map(|comment| {
            let line = comment.range.start.line as usize;
            let text = comment.text.trim();
            let extra = (first..=last).contains(&line)
                && !allowed.iter().any(|marker| marker == text)
                && !PRAGMA_PREFIXES
                    .iter()
                    .any(|prefix| text.starts_with(prefix));
            extra.then(|| {
                let name = node.name.unwrap_or_default();
                let message = format!(
                    "Test method '{name}' has an explanatory comment at line {line}: {text}"
                );
                Diagnostic::new(CODE, message, comment.range)
            })
        })
        .collect();
    for diagnostic in found {
        cx.report(diagnostic);
    }
}
