.PHONY: show-help setup-git-hooks compile

default: setup-git-hooks show-help

show-help:
	@echo "make setup-git-hooks - Set up git hooks"
	@echo "make show-help - Display this help message"
	@echo "make compile - Compile the project"

setup-git-hooks:
	@echo "Setting up git hooks..."
	@mkdir -p .git/hooks
	@cp .tools/githooks/commit-msg .git/hooks/
	@chmod +x .git/hooks/commit-msg
	@echo "Git hooks installed successfully"

compile:
	@echo "Compiling the project..."
	@pyinstaller main.py -n dpt -F
	@echo "Compilation complete. The executable is located in the dist directory."