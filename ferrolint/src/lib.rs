mod frozenset_constant;
mod no_docstrings;
mod no_relative_imports;
mod use_contextlib_suppress;

use ferrolint_plugin_sdk::prelude::*;

#[derive(Default)]
struct Gajaguar;

impl Checker for Gajaguar {
    fn info() -> Info {
        Info::new("pylint-gajaguar", env!("CARGO_PKG_VERSION"))
            .rule(frozenset_constant::rule())
            .rule(no_docstrings::rule())
            .rule(no_relative_imports::rule())
            .rule(use_contextlib_suppress::rule())
    }

    fn visit(&mut self, node: &Node<'_>, cx: &mut Context<'_>) {
        frozenset_constant::visit(node, cx);
        no_docstrings::visit(node, cx);
        no_relative_imports::visit(node, cx);
        use_contextlib_suppress::visit(node, cx);
    }
}

export_checker!(Gajaguar);
