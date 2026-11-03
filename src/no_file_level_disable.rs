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

/// The end of the string literal whose prefix starts at `at`, and whether it
/// is an f-string or t-string. Quotes nest in their replacement fields (PEP
/// 701), so a field is skipped whole, with the strings and comments in it.
fn string_end(bytes: &[u8], at: usize) -> (usize, bool) {
    let quote_at = at
        + bytes[at..]
            .iter()
            .take_while(|byte| byte.is_ascii_alphabetic())
            .count();
    let prefix = bytes[at..quote_at].to_ascii_lowercase();
    let formatted = prefix.iter().any(|byte| matches!(byte, b'f' | b't'));
    let Some(&quote) = bytes.get(quote_at) else {
        return (bytes.len(), formatted);
    };
    let triple = bytes[quote_at..].starts_with(&[quote; 3]);
    let width = if triple { 3 } else { 1 };
    let mut at = quote_at + width;
    while at < bytes.len() {
        match bytes[at] {
            // `\N{NAME}` is an escape, not a field.
            b'\\' if formatted && !prefix.contains(&b'r') && bytes[at + 1..].starts_with(b"N{") => {
                at += bytes[at..]
                    .iter()
                    .position(|&byte| byte == b'}')
                    .map_or(bytes.len() - at, |end| end + 1);
            }
            // A backslash before a brace escapes nothing: the brace still counts.
            b'\\' if formatted && matches!(bytes.get(at + 1), Some(b'{' | b'}')) => at += 1,
            b'\\' => at += 2,
            byte if byte == quote && (!triple || bytes[at..].starts_with(&[quote; 3])) => {
                return (at + width, formatted);
            }
            b'{' if formatted && bytes.get(at + 1) == Some(&b'{') => at += 2,
            b'{' if formatted => at = field_end(bytes, at + 1),
            _ => at += 1,
        }
    }
    (bytes.len(), formatted)
}

/// The offset after the `}` closing the replacement field whose expression
/// starts at `at`. The format spec after a top-level `:` is text with fields
/// of its own.
fn field_end(bytes: &[u8], mut at: usize) -> usize {
    let mut depth = 0_usize;
    while at < bytes.len() {
        match bytes[at] {
            b'\'' | b'"' => at = string_end(bytes, at).0,
            byte if byte.is_ascii_alphabetic() || byte == b'_' => {
                let name = bytes[at..]
                    .iter()
                    .take_while(|&&byte| byte.is_ascii_alphanumeric() || byte == b'_')
                    .count();
                let prefixed = name <= 2 && matches!(bytes.get(at + name), Some(b'\'' | b'"'));
                at = if prefixed {
                    string_end(bytes, at).0
                } else {
                    at + name
                };
            }
            b'#' => {
                at += bytes[at..]
                    .iter()
                    .position(|&byte| byte == b'\n')
                    .unwrap_or(bytes.len() - at);
            }
            b'(' | b'[' | b'{' => {
                depth += 1;
                at += 1;
            }
            b'}' if depth == 0 => return at + 1,
            b')' | b']' | b'}' => {
                depth = depth.saturating_sub(1);
                at += 1;
            }
            b':' if depth == 0 => return spec_end(bytes, at + 1),
            _ => at += 1,
        }
    }
    bytes.len()
}

/// The offset after the `}` closing a replacement field, from its format spec.
fn spec_end(bytes: &[u8], mut at: usize) -> usize {
    while at < bytes.len() {
        match bytes[at] {
            b'}' => return at + 1,
            b'{' => at = field_end(bytes, at + 1),
            _ => at += 1,
        }
    }
    bytes.len()
}

/// Where each string literal of an implicit concatenation starts in `text`,
/// and whether it is an f-string or t-string.
fn literals(text: &str) -> Vec<(usize, bool)> {
    let bytes = text.as_bytes();
    let mut found = Vec::new();
    let mut at = 0;
    while at < bytes.len() {
        if bytes[at].is_ascii_whitespace() || bytes[at] == b'\\' {
            at += 1;
            continue;
        }
        let (end, formatted) = string_end(bytes, at);
        found.push((at, formatted));
        at = end;
    }
    found
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
        let from = node.range.start.offset as usize;
        // An f-string's closing quote is a token of its own line, so only a
        // plain literal at the end of the concatenation leaves the line bare.
        matches!(
            node.kind,
            NodeKind::StringLiteral | NodeKind::BytesLiteral | NodeKind::FString
        ) && node.range.start.line < line
            && node.range.end.offset as usize == tail
            && {
                let parts = literals(&source[from..tail]);
                parts.last().is_some_and(|&(_, formatted)| !formatted)
                    && parts.iter().all(|&(at, _)| from + at < start)
            }
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
