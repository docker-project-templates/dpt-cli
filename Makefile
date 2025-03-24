.PHONY: show-help setup-git-hooks new-cmd

default: show-help

show-help:
	@echo "make setup-git-hooks - Set up git hooks"
	@echo "make new-cmd cmd_name=<command_name> - Create a new command"
	@echo "make show-help - Display this help message"

setup-git-hooks:
	@echo "Setting up git hooks..."
	@mkdir -p .git/hooks
	@cp .tools/githooks/commit-msg .git/hooks/
	@chmod +x .git/hooks/commit-msg
	@echo "Git hooks installed successfully"

new-cmd:
	@if [ -z $(cmd_name) ]; then \
		echo "Please provide a command name"; \
		echo "Usage: make new-cmd cmd_name=<command_name>"; \
		exit 1; \
	fi
	@chmod +x .tools/bin/create_cmd
	@echo "Creating new command..."
	@.tools/bin/create_cmd $(cmd_name)