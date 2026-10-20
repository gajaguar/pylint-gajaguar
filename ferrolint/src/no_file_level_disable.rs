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

/// The offsets, in `text`, at which each string literal of an implicit
/// concatenation starts. shortcut: a quote nested in an f-string replacement
/// field ends the literal early, upgrade with the SDK's per-part ranges.
fn literal_starts(text: &str) -> Vec<usize> {
    let bytes = text.as_bytes();
    let mut starts = Vec::new();
    let mut at = 0;
    while at < bytes.len() {
        if bytes[at].is_ascii_whitespace() || bytes[at] == b'\\' {
            at += 1;
            continue;
        }
        starts.push(at);
        while at < bytes.len() && bytes[at].is_ascii_alphabetic() {
            at += 1;
        }
        let Some(&quote) = bytes.get(at) else { break };
        let triple = bytes[at..].starts_with(&[quote; 3]);
        at += if triple { 3 } else { 1 };
        while at < bytes.len() {
            match bytes[at] {
                b'\\' => at += 2,
                byte if byte == quote && (!triple || bytes[at..].starts_with(&[quote; 3])) => {
                    at += if triple { 3 } else { 1 };
                    break;
                }
                _ => at += 1,
            }
        }
    }
    starts
}

/// Whether a token starts on the comment's line before the comment. The
/// Python checker counts the line of a token's start, so the last line of a
/// multi-line string, with nothing but the string's tail before the comment,
/// still counts as standalone; a literal that follows it on that line is code.
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
            && literal_starts(&source[node.range.start.offset as usize..tail])
                .iter()
                .all(|&at| node.range.start.offset as usize + at < start)
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
