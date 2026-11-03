CARGO := cargo
CARGO_DENY_VERSION := 0.20.2
WASM_TARGET := wasm32-wasip2
PLUGIN := target/$(WASM_TARGET)/release/pylint_gajaguar.wasm
PACKAGE_DIR := python/pylint_gajaguar
# The ferrolint binary the fixtures run under (uv tool install ferrolint==1.1.0).
FERROLINT ?= ferrolint

##@ Rust

install-rust: ## Fetch the crate's dependencies and install the pinned cargo-deny
	$(CARGO) fetch --locked
	$(CARGO) install --locked cargo-deny@$(CARGO_DENY_VERSION)

clippy: ## Lint with Clippy for the plugin target, treating warnings as errors
	$(CARGO) clippy --locked --target $(WASM_TARGET) -- -D warnings

fmt: ## Format code with rustfmt in place — accepts FILES="..."
	$(CARGO) fmt -- $(FILES)

fmt-check: ## Check formatting with rustfmt, without writing — accepts FILES="..."
	$(CARGO) fmt --check -- $(FILES)

deny: ## Check dependencies for advisories, licenses and sources with cargo-deny
	$(CARGO) deny --locked check

ferrolint-test: plugin-build ## Run the plugin over tests/fixtures and compare with their expected findings — accepts FERROLINT=<binary> and CODES="GAJ009 ..."
	FERROLINT="$(FERROLINT)" python3 tools/ferrolint-fixtures.py $(PLUGIN) $(CODES)

plugin-build: ## Build the plugin as a WASM component into target/
	$(CARGO) build --locked --release --target $(WASM_TARGET)

plugin: plugin-build ## Build the plugin into python/pylint_gajaguar/plugin.wasm
	cp $(PLUGIN) $(PACKAGE_DIR)/plugin.wasm

wheel: plugin ## Build the py3-none-any wheel that carries plugin.wasm into dist/
	uv build --wheel

ferrolint-sha256: plugin-build ## Print the sha256 of the built plugin, for a [[plugins]] entry in ferrolint.toml
	@shasum -a 256 $(PLUGIN) | cut -d' ' -f1

.PHONY: install-rust clippy fmt fmt-check deny ferrolint-test plugin-build plugin wheel ferrolint-sha256
