.PHONY: setup install-hooks check-readme-links

# Usage: make setup <problem-folder> [setup_num]
# Example: make setup 2142-the-number-of-passengers-in-each-bus-i      # uses ## Setup
#          make setup 2153-the-number-of-passengers-in-each-bus-ii 2   # uses ## Setup2
setup:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make setup <problem-folder>"; exit 1; \
	fi
	uv run python scripts/setup_sql.py $(filter-out $@,$(MAKECMDGOALS))

# Run once after cloning: enables the pre-commit hook that blocks commits
# adding a SQLs/ problem without a corresponding README.md link.
install-hooks:
	git config core.hooksPath githooks

# Same check the pre-commit hook runs; useful to run by hand.
check-readme-links:
	python3 scripts/check_readme_links.py

# Absorb extra targets so make doesn't error on the folder-name argument
%:
	@:
