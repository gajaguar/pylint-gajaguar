use ferrolint_plugin_sdk::prelude::*;

#[derive(Default)]
struct Gajaguar;

impl Checker for Gajaguar {
    fn info() -> Info {
        Info::new("pylint-gajaguar", env!("CARGO_PKG_VERSION"))
    }
}

export_checker!(Gajaguar);
