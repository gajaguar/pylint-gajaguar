use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ004";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "unused-arg-use-del",
        "An unused argument is hidden with a leading underscore.",
    )
    .pylint("W9004", "gajaguar-unused-arg-use-del")
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if node.kind != NodeKind::FunctionDef {
        return;
    }
    let Some(parameters) = cx
        .children(node)
        .find(|child| child.kind == NodeKind::Parameters)
    else {
        return;
    };
    let source = cx.source();
    let mut diagnostics = Vec::new();
    for parameter in cx
        .children(parameters)
        .filter(|child| child.kind == NodeKind::Parameter)
    {
        let name = parameter.name.unwrap_or_default();
        if matches!(name, "self" | "cls" | "_") || !name.starts_with('_') || name.starts_with("__")
        {
            continue;
        }
        // `*args` and `**kwargs` are not in the Python checker's argument lists.
        let before = source[..parameter.range.start.offset as usize].trim_end();
        if before.ends_with('*') || cx.text(parameter).starts_with('*') {
            continue;
        }
        // Only name loads count as a use, as astroid's `Name` nodes do.
        let used = (node.id + 1..=node.last)
            .filter_map(|id| cx.node(id))
            .any(|other| {
                other.kind == NodeKind::Name
                    && other.context == ExprContext::Load
                    && other.name == Some(name)
            });
        if used {
            continue;
        }
        let mut range = parameter.range;
        range.end = Position {
            offset: range.start.offset + u32::try_from(name.len()).unwrap_or_default(),
            line: range.start.line,
            column: range.start.column + u32::try_from(name.chars().count()).unwrap_or_default(),
        };
        let message = format!(
            "Argument '{name}' uses leading underscore; use 'del {name}' at the top of the body instead"
        );
        diagnostics.push(Diagnostic::new(CODE, message, range));
    }
    for diagnostic in diagnostics {
        cx.report(diagnostic);
    }
}
