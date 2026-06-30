.PHONY: setup

# Usage: make setup <filename.md> [setup_num]
# Example: make setup The_Number_of_Passengers_in_Each_Bus_1.md      # uses ## Setup
#          make setup The_Number_of_Passengers_in_Each_Bus_2.md 2    # uses ## Setup2
setup:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make setup <filename.md>"; exit 1; \
	fi
	uv run python scripts/setup_sql.py $(filter-out $@,$(MAKECMDGOALS))

# Absorb extra targets so make doesn't error on the filename argument
%:
	@:
