# end2end tests must be run from the root directory.
.PHONY: test
test:
	pytest test/

.PHONY: lint
lint:
	@black -l 120 snipfile test
	@isort snipfile test
	@flake8 --max-line-length 120 --ignore E203 snipfile test

.PHONY: gen_goldenfiles
gen_goldenfiles:
	@python -m snipfile.cli --input-dir=test/data/golden_in --output-dir=test/data/golden_out
