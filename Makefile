##@ Run


WEBSITE_DIR ?= ~/website

GENAPI_KEY ?= 


.PHONY: all clean help mdpapers finetune


finetune:
	uv run --directory py blkfinetune ../dataset/posts.csv ../dataset/mdpapers

mdpapers:
	uv run --directory py blkpdfmd ../dataset/papers ../dataset/mdpapers

dataset/retrieval_result.csv: dataset/links.csv
	uv run --directory py retrieve ../dataset/links.csv ../dataset/papers ../dataset/retrieval_result.csv

dataset/links.csv: dataset/summary.csv
	uv run --directory py links ../dataset/summary.csv ../dataset/posts.csv $(GENAPI_KEY) ../dataset/links.csv

dataset/summary.csv: dataset/classification.csv
	uv run --directory py blksmry ../dataset/classification.csv ../dataset/summary.csv

dataset/classification.csv: dataset/posts.csv
	uv run --directory py blkcly ../dataset/posts.csv $(GENAPI_KEY) ../dataset/classification.csv 

dataset/posts.csv: py/.venv/bin/python
	uv run --directory py blkmkd $(WEBSITE_DIR) ../dataset/posts.csv

py/.venv/bin/python:
	cd py && uv sync

##@ Clean
clean: ## Clean the project.
	rm -rf py/.venv
	rm -rf dataset/posts.csv

##@ Help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL = help