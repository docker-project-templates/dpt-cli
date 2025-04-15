.PHONY: show-help setup-git-hooks

default: setup-git-hooks show-help

show-help:
	@echo "make setup-git-hooks - Set up git hooks"
	@echo "make show-help - Display this help message"

setup-git-hooks:
	@echo "Setting up git hooks..."
	@mkdir -p .git/hooks
	@cp .tools/githooks/commit-msg .git/hooks/
	@chmod +x .git/hooks/commit-msg
	@echo "Git hooks installed successfully"