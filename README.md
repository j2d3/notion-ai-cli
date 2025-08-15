# 🚀 Notion Claude CLI

A command-line tool for uploading markdown files directly to your Notion workspace. Perfect for Claude Code users who want to create top-level pages and organize documentation efficiently.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🎯 **Create top-level pages** - Add pages at the same level as your existing workspace pages
- 🔒 **Secure OAuth authentication** - Uses Notion's official authentication flow
- 📝 **Rich markdown support** - Preserves headers, code blocks, lists, and formatting
- ⚡ **Simple CLI interface** - One command uploads any markdown file
- 🤖 **Claude Code integration** - Designed specifically for Claude Code workflows
- 🔐 **Privacy-focused** - All data stays local, no external servers

## 🏃‍♂️ Quick Start

### 1. Installation

```bash
# Clone or download this directory
cd notion-cli

# Run the install script
./install.sh
```

Or install manually:
```bash
pip install notion-client
# Add notion_cli.py to your PATH or create an alias
```

### 2. Setup Notion Integration

1. **Create Integration**: Go to https://www.notion.so/my-integrations
2. **Get Token**: Copy your "Internal Integration Token" 
3. **Configure CLI**: 
   ```bash
   notion-cli config set ntn_your_token_here
   ```
4. **Share Pages**: In Notion, share pages with your integration via "..." → "Add connections"

### 3. Start Using

```bash
# Upload a markdown file
notion-cli upload README.md --parent "Personal Website"

# List all pages in workspace
notion-cli list --type pages

# Search for content
notion-cli search "project documentation"

# Upload multiple files
notion-cli upload docs/*.md --parent "Documentation"
```

## 📖 Commands

### Upload Files
```bash
# Basic upload
notion-cli upload document.md

# Upload to specific parent page
notion-cli upload document.md --parent "Projects"
notion-cli upload document.md --parent "24f8f973-9991-80b2-944b-e5c1a0d419c8"

# Custom title
notion-cli upload README.md --title "My Project Documentation"

# Batch upload with wildcards
notion-cli upload docs/*.md --parent "Documentation"
```

### Workspace Management
```bash
# List all content
notion-cli list

# List only pages
notion-cli list --type pages

# List only databases
notion-cli list --type databases

# Search workspace
notion-cli search "meeting notes"
notion-cli search "project"
```

### Configuration
```bash
# Set token
notion-cli config set ntn_your_integration_token

# Show current config
notion-cli config show
```

## 🎨 Supported Markdown Features

✅ **Headers** (H1, H2, H3)
✅ **Code blocks** with syntax highlighting
✅ **Bullet points** and numbered lists
✅ **Inline formatting** (bold, italic, code)
✅ **Paragraphs** with proper spacing

### Code Block Language Mapping
- `jinja2` → `html`
- `yml` → `yaml` 
- `dockerfile` → `docker`
- Unknown languages → `plain text`

## 🔧 Configuration

Configuration is stored in `~/.notion-cli/config.json`:

```json
{
  "token": "ntn_your_integration_token"
}
```

## 📝 Examples

### Upload Project Documentation
```bash
# Upload main README
notion-cli upload README.md --parent "Projects" --title "MyApp Documentation"

# Upload all markdown files in docs/
notion-cli upload docs/*.md --parent "MyApp Documentation"
```

### Workspace Exploration
```bash
# Find all your pages
notion-cli list --type pages

# Search for specific content
notion-cli search "API documentation"

# Find databases
notion-cli list --type databases
```

### Batch Operations
```bash
# Upload multiple files
notion-cli upload *.md --parent "Documentation Hub"

# Upload files from subdirectories
notion-cli upload **/*.md --parent "All Docs"
```

## 🔒 Security

- Tokens are stored locally in `~/.notion-cli/config.json`
- Only you have access to your workspace content
- Uses official Notion API with standard authentication

## 🛠 Development

Built with:
- Python 3.8+
- [notion-client](https://github.com/ramnes/notion-sdk-py) - Official Notion Python SDK
- Standard library (argparse, pathlib, json)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your Notion workspace
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## 🆘 Troubleshooting

### "No Notion token configured"
Run `notion-cli config set YOUR_TOKEN` with your integration token.

### "Parent page not found"
Make sure you've shared the parent page with your integration in Notion.

### "Permission denied"
Ensure your integration has the necessary permissions (Read/Insert/Update content).

### "Language not supported"
Some code block languages are automatically mapped to supported ones. Unsupported languages default to "plain text".

## 🎯 Roadmap

- [ ] Template system for common document types
- [ ] Export existing Notion pages to markdown
- [ ] Database integration for structured content
- [ ] Bulk operations with progress bars
- [ ] Configuration profiles for multiple workspaces
- [ ] Rich text formatting enhancements