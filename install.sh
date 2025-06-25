#!/bin/bash

# Installation script for Claude-arXiv
# Sets up arxiv and arxiv_interactive aliases

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARXIV_SCRIPT="$SCRIPT_DIR/arxiv_simple.py"

echo "Claude-arXiv Installation"
echo "========================"

# Check if the main script exists
if [ ! -f "$ARXIV_SCRIPT" ]; then
    echo "Error: arxiv_simple.py not found in $SCRIPT_DIR"
    exit 1
fi

# Determine which shell config file to use
SHELL_CONFIG=""
if [ -f ~/.zshrc ]; then
    SHELL_CONFIG=~/.zshrc
    SHELL_NAME="zsh"
elif [ -f ~/.bashrc ]; then
    SHELL_CONFIG=~/.bashrc
    SHELL_NAME="bash"
elif [ -f ~/.bash_profile ]; then
    SHELL_CONFIG=~/.bash_profile
    SHELL_NAME="bash"
else
    echo "No shell configuration file found."
    echo "Please manually add these aliases to your shell config:"
    echo "alias arxiv='python $ARXIV_SCRIPT'"
    echo "alias arxiv_interactive='python $ARXIV_SCRIPT --interactive'"
    exit 1
fi

echo "Found shell: $SHELL_NAME"
echo "Config file: $SHELL_CONFIG"

# Function to check if an alias already exists
alias_exists() {
    local alias_name="$1"
    grep -q "^[[:space:]]*alias[[:space:]]\+${alias_name}=" "$SHELL_CONFIG" 2>/dev/null
}

# Function to remove existing aliases
remove_existing_aliases() {
    local alias_name="$1"
    # Create a temporary file
    local temp_file=$(mktemp)
    
    # Remove existing aliases (including commented ones from previous installations)
    grep -v "^[[:space:]]*alias[[:space:]]\+${alias_name}=" "$SHELL_CONFIG" > "$temp_file"
    grep -v "^[[:space:]]*#.*Claude arXiv integration" "$temp_file" > "${temp_file}.2"
    mv "${temp_file}.2" "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$SHELL_CONFIG"
}

# Check for existing aliases
ARXIV_EXISTS=false
ARXIV_INTERACTIVE_EXISTS=false

if alias_exists "arxiv"; then
    echo "Found existing 'arxiv' alias - will replace"
    ARXIV_EXISTS=true
fi

if alias_exists "arxiv_interactive"; then
    echo "Found existing 'arxiv_interactive' alias - will replace"
    ARXIV_INTERACTIVE_EXISTS=true
fi

# Always replace existing aliases if found
if [ "$ARXIV_EXISTS" = true ] || [ "$ARXIV_INTERACTIVE_EXISTS" = true ]; then
    echo "Replacing existing aliases..."
    remove_existing_aliases "arxiv"
    remove_existing_aliases "arxiv_interactive"
fi

# Add new aliases
echo ""
echo "Adding Claude-arXiv aliases to $SHELL_CONFIG..."

cat >> "$SHELL_CONFIG" << EOF

# Claude arXiv integration - added by install.sh
alias arxiv='python $ARXIV_SCRIPT'
alias arxiv_interactive='python $ARXIV_SCRIPT --interactive'
EOF

echo "✓ Aliases added successfully!"

# Test the aliases
echo ""
echo "Testing installation..."

# Source the config file and test
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "⚠️  Warning: Python not found in PATH"
    PYTHON_CMD="python"
fi

# Test if the script runs
if $PYTHON_CMD "$ARXIV_SCRIPT" --help >/dev/null 2>&1; then
    echo "✓ arxiv_simple.py is working correctly"
else
    echo "⚠️  Warning: There might be an issue with the Python script"
fi

echo ""
echo "Installation complete! 🎉"
echo ""
echo "Usage:"
echo "  arxiv 2404.11397 \"What is the main contribution?\""
echo "  arxiv_interactive 2404.11397"
echo ""
echo "To activate the aliases in your current session, run:"
echo "  source $SHELL_CONFIG"
echo ""
echo "Or restart your terminal."