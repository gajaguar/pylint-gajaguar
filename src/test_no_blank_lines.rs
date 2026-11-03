use ferrolint_plugin_sdk::prelude::*;

use crate::testing::{from_line, is_test_function, line_range, lines};

pub const CODE: &str = "GAJ003";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "test-no-blank-lines",
        "A test body contains a blank line.",
    )
    .pylint("W9003", "gajaguar-test-no-blank-lines")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !is_test_function(node, cx) {
        return;
    }
    let lines = lines(cx.source());
    let last = (node.range.end.line as usize).min(lines.len());
    // The first blank line after astroid's `fromlineno`, as the Python checker does.
    let blank =
        (from_line(node, cx) + 1..=last).find(|number| lines[number - 1].1.trim().is_empty());
    if let Some(number) = blank {
        let message = format!(
            "Test method '{}' contains a blank line at line {number}",
            node.name.unwrap_or_default()
        );
        cx.report(Diagnostic::new(CODE, message, line_range(number, &lines)));
    }
}
