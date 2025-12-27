.PHONY: help install fetch analyze visualize all clean test

# Default target
help:
	@echo "O9NN Organization Graph Management"
	@echo ""
	@echo "Available targets:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make fetch       - Fetch latest organization data from GitHub"
	@echo "  make analyze     - Run organization analysis"
	@echo "  make visualize   - Generate visualizations"
	@echo "  make all         - Run fetch, analyze, and visualize"
	@echo "  make test        - Test all scripts"
	@echo "  make clean       - Remove generated files"
	@echo ""
	@echo "Environment variables:"
	@echo "  GITHUB_TOKEN or magoo - GitHub Personal Access Token (required)"
	@echo "  ORG_LOGIN            - Organization name (default: o9nn)"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Fetch organization data
fetch:
	@echo "Fetching organization data..."
	python fetch_org_graph.py

# Run analysis
analyze:
	@echo "Running organization analysis..."
	python analyze_org.py > analysis_output.txt
	@echo "Analysis saved to: analysis_output.txt"

# Generate visualizations
visualize:
	@echo "Generating visualizations..."
	python visualize_graph.py

# Run all steps
all: fetch analyze visualize
	@echo ""
	@echo "✅ All tasks completed successfully!"
	@echo ""
	@echo "Generated files:"
	@echo "  - org-graph-raw.json"
	@echo "  - org-graph.json"
	@echo "  - analysis_output.txt"
	@echo "  - org-graph-visualization.png"
	@echo "  - org-graph-network.png"

# Test all scripts
test:
	@echo "Testing scripts..."
	@python -m py_compile fetch_org_graph.py
	@python -m py_compile analyze_org.py
	@python -m py_compile visualize_graph.py
	@echo "✅ All scripts passed syntax check"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -f org-graph-raw.json org-graph.json analysis_output.txt
	rm -f org-graph-visualization.png org-graph-network.png
	rm -rf __pycache__ *.pyc
	@echo "✅ Cleanup complete"
