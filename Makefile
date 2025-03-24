.PHONY: setup-git-hooks

setup-git-hooks:
	@echo "Setting up git hooks..."
	@mkdir -p .git/hooks
	@cp .tools/githooks/commit-msg .git/hooks/
	@chmod +x .git/hooks/commit-msg
	@echo "Git hooks installed successfully"