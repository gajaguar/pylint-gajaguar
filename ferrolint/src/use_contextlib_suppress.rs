use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ012";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "use-contextlib-suppress",
        "A try/except/pass should be contextlib.suppress.",
    )
    .pylint("W9012", "gajaguar-use-contextlib-suppress")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if node.kind != NodeKind::Try {
        return;
    }
    // A try block's statements, then its handlers, then the else and finally
    // statements: any statement after the first handler is one of the latter.
    let mut handlers = 0;
    for child in cx.children(node) {
        if child.kind == NodeKind::ExceptHandler {
            if !is_silent(child, cx) {
                return;
            }
            handlers += 1;
        } else if handlers > 0 && Context::is_statement(child) {
            return;
        }
    }
    if handlers > 0 {
        cx.report(Diagnostic::new(
            CODE,
            "Use 'contextlib.suppress(...)' instead of 'try/except/pass'",
            node.range,
        ));
    }
}

// A typed handler whose whole body is one `pass`.
fn is_silent(handler: &Node<'_>, cx: &Context<'_>) -> bool {
    // The Python checker never visits `try/except*`.
    if cx
        .text(handler)
        .trim_start_matches("except")
        .trim_start()
        .starts_with('*')
    {
        return false;
    }
    let mut statements = cx
        .children(handler)
        .filter(|child| Context::is_statement(child));
    let typed = cx
        .children(handler)
        .next()
        .is_some_and(|first| !Context::is_statement(first));
    typed
        && statements
            .next()
            .is_some_and(|only| only.kind == NodeKind::Pass)
        && statements.next().is_none()
}
