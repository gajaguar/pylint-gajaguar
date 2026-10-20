use crate::testing::{def_line, lines};
use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ008";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "no-inline-imports",
        "An import sits inside a function or class.",
    )
    .pylint("W9008", "gajaguar-no-inline-imports")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if !matches!(node.kind, NodeKind::Import | NodeKind::ImportFrom) {
        return;
    }
    let scope = cx.scope(node);
    if scope.kind == ScopeKind::Module {
        return;
    }
    if node.kind == NodeKind::ImportFrom && under_type_checking(node, cx) {
        return;
    }
    let frame = match scope.kind {
        ScopeKind::Class => "ClassDef",
        ScopeKind::Lambda => "Lambda",
        _ if cx.node(scope.node).is_some_and(|def| {
            let lines = lines(cx.source());
            lines[def_line(def, &lines) - 1]
                .1
                .trim_start()
                .starts_with("async")
        }) =>
        {
            "AsyncFunctionDef"
        }
        _ => "FunctionDef",
    };
    let names = cx
        .children(node)
        .filter(|alias| alias.kind == NodeKind::Alias)
        .map(|alias| alias.detail.or(alias.name).unwrap_or_default())
        .collect::<Vec<_>>()
        .join(", ");
    let message = format!("Import of '{names}' inside {frame}; move to top of module");
    cx.report(Diagnostic::new(CODE, message, node.range));
}

// The Python checker looks at the direct parent `if` only, whichever branch
// the import is in.
fn under_type_checking(node: &Node<'_>, cx: &Context<'_>) -> bool {
    let Some(parent) = cx.parent(node) else {
        return false;
    };
    let test = match parent.kind {
        NodeKind::If => cx.children(parent).next(),
        NodeKind::ElifElseClause => {
            let own = cx
                .children(parent)
                .next()
                .filter(|first| !Context::is_statement(first));
            own.or_else(|| cx.parent(parent).and_then(|top| cx.children(top).next()))
        }
        _ => None,
    };
    test.is_some_and(|test| {
        matches!(test.kind, NodeKind::Name | NodeKind::Attribute)
            && test.name == Some("TYPE_CHECKING")
    })
}
