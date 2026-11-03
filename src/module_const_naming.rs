use ferrolint_plugin_sdk::prelude::*;

use crate::require_final::is_dunder;

pub const CODE: &str = "GAJ005";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "module-const-naming",
        "A module-level name is not SCREAMING_SNAKE_CASE.",
    )
    .pylint("C9005", "gajaguar-module-const-naming")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    // A bound name is a store-context name, the `as` name of an except handler or
    // the capture of a `match` pattern (a pattern carries a name only when it binds one).
    let bound = match node.kind {
        NodeKind::Name => node.context == ExprContext::Store,
        NodeKind::ExceptHandler | NodeKind::Pattern => node.name.is_some(),
        _ => false,
    };
    if !bound || cx.scope(node).kind != ScopeKind::Module {
        return;
    }
    let name = node.name.unwrap_or_default();
    if is_dunder(name) || name == "_" || is_screaming(name) {
        return;
    }
    let message = format!("Module-level name '{name}' should be SCREAMING_SNAKE_CASE");
    cx.report(Diagnostic::new(CODE, message, node.range));
}

// `^_?[A-Z][A-Z0-9_]*$`
fn is_screaming(name: &str) -> bool {
    let rest = name.strip_prefix('_').unwrap_or(name);
    let mut chars = rest.chars();
    chars.next().is_some_and(|c| c.is_ascii_uppercase())
        && chars.all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || c == '_')
}
