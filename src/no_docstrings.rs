use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ001";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "no-docstrings",
        "A function or class has a docstring.",
    )
    .pylint("W9001", "gajaguar-no-docstrings")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !matches!(node.kind, NodeKind::FunctionDef | NodeKind::ClassDef) {
        return;
    }
    // The body's first statement; decorators, parameters and bases are not statements.
    let Some(first) = cx.children(node).find(|child| Context::is_statement(child)) else {
        return;
    };
    if first.kind != NodeKind::Expr {
        return;
    }
    let Some(doc) = cx.children(first).next() else {
        return;
    };
    if doc.kind == NodeKind::StringLiteral {
        let name = node.name.unwrap_or_default();
        let message = format!("Docstring found in '{name}'; use comments instead");
        cx.report(Diagnostic::new(CODE, message, doc.range));
    }
}
