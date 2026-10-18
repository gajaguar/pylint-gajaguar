use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ013";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "frozenset-constant",
        "A module-level set constant is mutable.",
    )
    .pylint("W9013", "gajaguar-frozenset-constant")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !matches!(node.kind, NodeKind::Assign | NodeKind::AnnAssign)
        || cx.scope(node).kind != ScopeKind::Module
    {
        return;
    }
    // The value is the last child; an annotated assignment may have none.
    let children: Vec<_> = cx.children(node).collect();
    let value = match (node.kind, children.as_slice()) {
        (NodeKind::AnnAssign, [_, _]) => return,
        (_, [.., value]) => *value,
        _ => return,
    };
    if is_mutable_set(value, cx) {
        cx.report(Diagnostic::new(
            CODE,
            "Set constant should be a frozenset(...) for immutability",
            value.range,
        ));
    }
}

fn is_mutable_set(value: &Node<'_>, cx: &Context<'_>) -> bool {
    match value.kind {
        NodeKind::Set | NodeKind::SetComp => true,
        NodeKind::Call => cx.children(value).next().is_some_and(|func| {
            matches!(func.kind, NodeKind::Name | NodeKind::Attribute) && func.name == Some("set")
        }),
        _ => false,
    }
}
