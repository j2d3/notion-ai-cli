#!/bin/bash
"""
Quick install script for Notion CLI
"""

set -e

echo "🚀 Installing Notion CLI..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install notion-client if not already installed
echo "📦 Installing dependencies..."
pip3 install notion-client

# Create symlink to make it accessible globally
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/notion_cli.py"

# Create /usr/local/bin if it doesn't exist
sudo mkdir -p /usr/local/bin

# Create symlink
echo "🔗 Creating global command..."
sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/notion-cli

# Make executable
chmod +x "$SCRIPT_PATH"

echo "✅ Installation complete!"
echo ""
echo "🎯 Quick start:"
echo "  1. Get your Notion integration token from: https://www.notion.so/my-integrations"
echo "  2. Configure the CLI: notion-cli config set YOUR_TOKEN"
echo "  3. Share pages with your integration in Notion"
echo "  4. Upload files: notion-cli upload README.md --parent 'Personal Website'"
echo ""
echo "📚 For help: notion-cli --help"