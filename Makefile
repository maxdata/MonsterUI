# Declare phony targets that don't produce a file named after the target
.PHONY: tests tests-basic lint install mypy update docker docker-clean convert-and-delete


# Make target to convert Jupyter notebooks to Python scripts and delete original files
jupyter:
	@if find . -name "*.ipynb" -print | grep -q .; then \
		find . -name "*.ipynb" -exec sh -c 'jupyter nbconvert --to python "$$0" && rm "$$0"' {} \; ; \
	else \
		echo "No Jupyter notebook files found."; \
	fi
