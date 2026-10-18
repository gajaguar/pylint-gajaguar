mod frozenset_constant;
mod module_const_naming;
mod no_docstrings;
mod no_inline_imports;
mod no_relative_imports;
mod require_final;
mod use_contextlib_suppress;

use ferrolint_plugin_sdk::prelude::*;

#[derive(Default)]
struct Gajaguar;

impl Checker for Gajaguar {
    fn info() -> Info {
        Info::new("pylint-gajaguar", env!("CARGO_PKG_VERSION"))
            .rule(frozenset_constant::rule())
            .rule(module_const_naming::rule())
            .rule(no_docstrings::rule())
            .rule(no_inline_imports::rule())
            .rule(no_relative_imports::rule())
            .rule(require_final::rule())
            .rule(use_contextlib_suppress::rule())
    }

    fn visit(&mut self, node: &Node<'_>, cx: &mut Context<'_>) {
        frozenset_constant::visit(node, cx);
        module_const_naming::visit(node, cx);
        no_docstrings::visit(node, cx);
        no_inline_imports::visit(node, cx);
        no_relative_imports::visit(node, cx);
        require_final::visit(node, cx);
        use_contextlib_suppress::visit(node, cx);
    }
}

export_checker!(Gajaguar);
