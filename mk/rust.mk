# The ferrolint plugin in ferrolint/ is outside LANG_*_TARGETS: building it
# fetches the SDK from a private git repository and testing it needs a
# ferrolint binary, neither of which CI has.
CARGO := cd ferrolint && cargo
WASM := ferrolint/target/wasm32-wasip2/release/pylint_gajaguar_ferrolint.wasm
# The ferrolint binary the fixtures run under; build one in the ferrolint
# repository and point FERROLINT at it.
FERROLINT ?= ferrolint

##@ ferrolint plugin

ferrolint-build: ## Build the ferrolint plugin to ferrolint/target/wasm32-wasip2/release/
	$(CARGO) build --target wasm32-wasip2 --release

ferrolint-clippy: ## Lint the ferrolint plugin with clippy
	$(CARGO) clippy --target wasm32-wasip2 --release -- -D warnings

ferrolint-fmt: ## Format the ferrolint plugin with rustfmt
	$(CARGO) fmt

ferrolint-test: ferrolint-build ## Compare the plugin with pylint on ferrolint/fixtures — accepts FERROLINT=<binary> and CODES="GAJ009 ..."
	FERROLINT="$(FERROLINT)" python3 tools/ferrolint-fixtures.py $(WASM) $(CODES)

.PHONY: ferrolint-build ferrolint-clippy ferrolint-fmt ferrolint-test
