use std::collections::BTreeSet;

use ferrolint_plugin_sdk::prelude::*;

use crate::testing::{def_line, is_test_function, line_range, lines};

pub const CODE: &str = "GAJ016";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "test-partial-assertion",
        "A test asserts on a field without asserting the whole object.",
    )
    .pylint("W9016", "gajaguar-test-partial-assertion")
}

/// The name a subscript chain (`name[a][b]`) is rooted at; none for a plain
/// name or any other root.
fn subscript_root<'a>(node: &'a Node<'a>, cx: &Context<'a>) -> Option<&'a str> {
    let mut current = node;
    while current.kind == NodeKind::Subscript {
        current = cx.children(current).next()?;
    }
    (current.kind == NodeKind::Name && current.id != node.id)
        .then_some(current.name)
        .flatten()
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !is_test_function(node, cx) {
        return;
    }
    let mut subscripted = BTreeSet::new();
    let mut whole = BTreeSet::new();
    let asserts = (node.id + 1..=node.last)
        .filter_map(|id| cx.node(id))
        .filter(|other| other.kind == NodeKind::Assert);
    for assertion in asserts {
        let Some(test) = cx.children(assertion).next() else {
            continue;
        };
        if test.kind != NodeKind::Compare {
            continue;
        }
        // The operands are the compare's children: the left side, then the comparators.
        for operand in cx.children(test) {
            if let Some(root) = subscript_root(operand, cx) {
                subscripted.insert(root);
            } else if operand.kind == NodeKind::Name {
                whole.extend(operand.name);
            }
        }
    }
    let lines = lines(cx.source());
    let range = line_range(def_line(node, &lines), &lines);
    let name = node.name.unwrap_or_default();
    for partial in subscripted.difference(&whole) {
        let message = format!(
            "Test method '{name}' asserts on '{partial}[...]' without ever asserting the whole object"
        );
        cx.report(Diagnostic::new(CODE, message, range));
    }
}
