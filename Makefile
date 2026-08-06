.PHONY: setup

# Usage: make setup <problem-folder> [setup_num]
# Example: make setup 2142-the-number-of-passengers-in-each-bus-i      # uses ## Setup
#          make setup 2153-the-number-of-passengers-in-each-bus-ii 2   # uses ## Setup2
setup:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make setup <problem-folder>"; exit 1; \
	fi
	uv run python scripts/setup_sql.py $(filter-out $@,$(MAKECMDGOALS))

# Absorb extra targets so make doesn't error on the folder-name argument
%:
	@:
