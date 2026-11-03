use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ009";

pub fn rule() -> Rule {
    Rule::new(CODE, "no-relative-imports", "A relative import is used.")
        .pylint("W9009", "gajaguar-no-relative-imports")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if node.kind != NodeKind::ImportFrom {
        return;
    }
    // `detail` is the module with its leading dots.
    let module = node.detail.unwrap_or_default();
    if module.starts_with('.') {
        let message = format!("Relative import '{module}' is not allowed; use absolute imports");
        cx.report(Diagnostic::new(CODE, message, node.range));
    }
}
