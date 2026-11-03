use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ014";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "require-final",
        "A module-level constant is not annotated Final.",
    )
    .pylint("C9014", "gajaguar-require-final")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !matches!(node.kind, NodeKind::Assign | NodeKind::AnnAssign)
        || cx.scope(node).kind != ScopeKind::Module
    {
        return;
    }
    let children: Vec<_> = cx.children(node).collect();
    let name = match (node.kind, children.as_slice()) {
        // One plain-name target and the value; chained or unpacking targets are skipped.
        (NodeKind::Assign, [target, _]) if target.kind == NodeKind::Name => target.name,
        (NodeKind::AnnAssign, [target, annotation, ..])
            if target.kind == NodeKind::Name && !is_final(annotation, cx) =>
        {
            target.name
        }
        _ => return,
    };
    let name = name.unwrap_or_default();
    if is_dunder(name) || name == "_" {
        return;
    }
    let message = format!("Module-level constant '{name}' must be annotated Final");
    cx.report(Diagnostic::new(CODE, message, node.range));
}

pub fn is_dunder(name: &str) -> bool {
    name.len() >= 5
        && name.starts_with("__")
        && name.ends_with("__")
        && name.chars().all(|c| c.is_alphanumeric() || c == '_')
}

fn is_final(annotation: &Node<'_>, cx: &Context<'_>) -> bool {
    match annotation.kind {
        NodeKind::Subscript => cx
            .children(annotation)
            .next()
            .is_some_and(|value| is_final(value, cx)),
        NodeKind::Name | NodeKind::Attribute => annotation.name == Some("Final"),
        _ => false,
    }
}
