use ferrolint_plugin_sdk::prelude::*;

pub const CODE: &str = "GAJ006";

pub fn rule() -> Rule {
    Rule::new(
        CODE,
        "no-file-level-disable",
        "A comment holds a standalone `# pylint: disable=`.",
    )
    .pylint("W9006", "gajaguar-no-file-level-disable")
}

/// Whether the comment has `#`, spaces, `pylint:`, spaces and `keyword` at
/// any `#`, as the Python checker's regular expressions do.
fn pragma(text: &str, keyword: &str) -> bool {
    text.match_indices('#').any(|(at, _)| {
        text[at + 1..]
            .trim_start()
            .strip_prefix("pylint:")
            .is_some_and(|rest| rest.trim_start().starts_with(keyword))
    })
}

/// Whether a token starts on the comment's line before the comment. The
/// Python checker counts the line of a token's start, so the last line of a
/// multi-line string, with nothing but the string's tail before the comment,
/// still counts as standalone.
fn has_code(comment: &Comment<'_>, cx: &Context<'_>) -> bool {
    let offset = comment.range.start.offset as usize;
    let source = cx.source();
    let start = source[..offset].rfind('\n').map_or(0, |at| at + 1);
    let before = source[start..offset].trim_end();
    if before.trim_start().is_empty() {
        return false;
    }
    let tail = start + before.len();
    let line = comment.range.start.line;
    let string_tail = cx.nodes().iter().any(|node| {
        matches!(node.kind, NodeKind::StringLiteral | NodeKind::BytesLiteral)
            && node.range.start.line < line
            && node.range.end.offset as usize == tail
    });
    !string_tail
}

pub fn visit(node: &Node<'_>, cx: &mut Context<'_>) {
    if node.kind != NodeKind::Module {
        return;
    }
    let found: Vec<Diagnostic> = cx
        .comments()
        .iter()
        .filter(|comment| {
            pragma(comment.text, "disable=")
                && !pragma(comment.text, "disable-next=")
                && !has_code(comment, cx)
        })
        .map(|comment| {
            let message =
                "Standalone '# pylint: disable=' found; use inline or 'disable-next=' instead";
            Diagnostic::new(CODE, message, comment.range)
        })
        .collect();
    for diagnostic in found {
        cx.report(diagnostic);
    }
}
