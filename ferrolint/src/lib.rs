mod no_docstrings;
mod no_relative_imports;

use ferrolint_plugin_sdk::prelude::*;

#[derive(Default)]
struct Gajaguar;

impl Checker for Gajaguar {
    fn info() -> Info {
        Info::new("pylint-gajaguar", env!("CARGO_PKG_VERSION"))
            .rule(no_docstrings::rule())
            .rule(no_relative_imports::rule())
    }

    fn visit(&mut self, node: &Node<'_>, cx: &mut Context<'_>) {
        no_docstrings::visit(node, cx);
        no_relative_imports::visit(node, cx);
    }
}

export_checker!(Gajaguar);
