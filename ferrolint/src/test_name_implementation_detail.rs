use ferrolint_plugin_sdk::prelude::*;

use crate::testing::{def_line, is_test_function, line_range, lines};

pub const CODE: &str = "GAJ017";

const TERMS: [&str; 10] = [
    "called",
    "calls",
    "impl",
    "internal",
    "mock",
    "patch",
    "private",
    "return_value",
    "spy",
    "stub",
];

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "test-name-implementation-detail",
        "A test name names an implementation detail.",
    )
    .pylint("W9017", "gajaguar-test-name-implementation-detail")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !is_test_function(node, cx) {
        return;
    }
    let name = node.name.unwrap_or_default();
    let lowered = name.to_lowercase();
    let words: Vec<&str> = lowered
        .split(|c: char| !(c.is_ascii_lowercase() || c.is_ascii_digit()))
        .filter(|word| !word.is_empty())
        .collect();
    // A term with an underscore matches anywhere; a single word must be a whole word.
    let found: Vec<&str> = TERMS
        .iter()
        .copied()
        .filter(|term| {
            if term.contains('_') {
                lowered.contains(term)
            } else {
                words.contains(term)
            }
        })
        .collect();
    if found.is_empty() {
        return;
    }
    let lines = lines(cx.source());
    let range = line_range(def_line(node, &lines), &lines);
    let message = format!(
        "Test name '{name}' names an implementation detail: {}",
        found.join(", ")
    );
    cx.report(Diagnostic::new(CODE, message, range));
}
