use ferrolint_plugin_sdk::prelude::*;

use crate::testing::{def_line, is_test_function, line_range, lines};

pub const CODE: &str = "GAJ002";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "test-aaa-markers",
        "A test lacks an Arrange, Act or Assert marker.",
    )
    .pylint("W9002", "gajaguar-test-aaa-markers")
}

// The `test-section-markers` option is a comma-separated list; the
// TEST_SECTION_MARKERS environment override is not available to a plugin.
fn markers(cx: &Context<'_>) -> Vec<String> {
    let names: Vec<&str> = cx
        .option("test-section-markers")
        .map(|value| {
            value
                .split(',')
                .map(str::trim)
                .filter(|name| !name.is_empty())
                .collect()
        })
        .unwrap_or_default();
    if names.is_empty() {
        return ["Arrange", "Act", "Assert"]
            .map(|name| format!("# {name}"))
            .to_vec();
    }
    names.iter().map(|name| format!("# {name}")).collect()
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !is_test_function(node, cx) {
        return;
    }
    let lines = lines(cx.source());
    let first = def_line(node, &lines);
    let last = node.range.end.line as usize;
    let raw: String = lines[first - 1..last.min(lines.len())]
        .iter()
        .map(|line| line.1)
        .collect();
    let missing: Vec<String> = markers(cx)
        .into_iter()
        .filter(|marker| !raw.contains(marker.as_str()))
        .collect();
    if missing.is_empty() {
        return;
    }
    let message = format!(
        "Test method '{}' missing AAA marker(s): {}",
        node.name.unwrap_or_default(),
        missing.join(", ")
    );
    cx.report(Diagnostic::new(CODE, message, line_range(first, &lines)));
}
