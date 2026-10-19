use ferrolint_plugin_sdk::prelude::*;

/// A file the `gajaguar-test-*` rules apply to: its stem starts with `test_`
/// or ends with `_test`, or a parent directory is named `test` or `tests`.
pub fn is_test_file(path: &str) -> bool {
    let path = std::path::Path::new(path);
    let stem = path
        .file_stem()
        .and_then(|stem| stem.to_str())
        .unwrap_or_default();
    stem.starts_with("test_")
        || stem.ends_with("_test")
        || path.parent().is_some_and(|parent| {
            parent
                .components()
                .any(|part| matches!(part.as_os_str().to_str(), Some("test" | "tests")))
        })
}

/// A `test_*` function of a test file.
pub fn is_test_function(node: &Node<'_>, cx: &Context<'_>) -> bool {
    node.kind == NodeKind::FunctionDef
        && node.name.is_some_and(|name| name.starts_with("test_"))
        && is_test_file(cx.path())
}

/// The source lines with the byte offset each starts at.
pub fn lines(source: &str) -> Vec<(usize, &str)> {
    source
        .split_inclusive('\n')
        .scan(0, |offset, line| {
            let start = *offset;
            *offset += line.len();
            Some((start, line))
        })
        .collect()
}

/// The 1-based line of the `def` keyword, after any decorators.
pub fn def_line(node: &Node<'_>, lines: &[(usize, &str)]) -> usize {
    let first = node.range.start.line as usize;
    (first..=node.range.end.line as usize)
        .find(|number| {
            let text = lines.get(number - 1).map_or("", |line| line.1).trim_start();
            text.starts_with("def ") || text.starts_with("async ")
        })
        .unwrap_or(first)
}

/// A range covering one line's text, from its indentation to its end.
pub fn line_range(number: usize, lines: &[(usize, &str)]) -> Range {
    let (start, text) = lines.get(number - 1).copied().unwrap_or((0, ""));
    let indent = text.len() - text.trim_start().len();
    let end = text.trim_end().len().max(indent);
    let position = |offset: usize| Position {
        offset: u32::try_from(start + offset).unwrap_or_default(),
        line: u32::try_from(number).unwrap_or_default(),
        column: u32::try_from(text[..offset].chars().count() + 1).unwrap_or_default(),
    };
    Range {
        start: position(indent),
        end: position(end),
    }
}
