# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Notion CLI Tool

This repository contains a custom-built Notion CLI tool that allows uploading markdown files and managing Notion workspace content.

### Setup Status
- ✅ Notion CLI is built and functional
- ✅ Token is already configured for user's workspace
- ✅ Tool is located at `/Users/johndurkin/personal/zaumac/notion-cli/notion_cli.py`
- ✅ Dependencies installed (notion-client)

### How to Use Notion CLI

**Important**: The tool is already configured with the user's Notion integration token. The user's workspace contains pages like "Personal Website", "Job Application Tracker", "Project Planner" database, etc.

#### Core Commands

```bash
# Navigate to the tool directory first
cd /Users/johndurkin/personal/zaumac/notion-cli

# Upload markdown files
python notion_cli.py upload README.md --parent "Personal Website"
python notion_cli.py upload *.md --parent "Personal Website"

# List workspace content
python notion_cli.py list --type pages
python notion_cli.py list --type databases

# Search workspace
python notion_cli.py search "documentation"

# Check configuration
python notion_cli.py config show
```

#### When to Use Notion CLI

Use this tool when:
- User asks to upload documentation to Notion
- User wants to share project files with their Notion workspace
- User requests creating Notion pages from markdown content
- User asks to search or explore their Notion workspace

#### Available Parent Pages (from user's workspace)
- "Personal Website" (ID: 24f8f973-9991-80b2-944b-e5c1a0d419c8)
- "Job Application Tracker"
- "Weekly To-do List" 
- "Project Planner" (database)
- "Monthly Budget"
- "Welcome to Notion!"

#### Markdown Conversion Features
- Headers (H1, H2, H3) → Notion heading blocks
- Code blocks with syntax highlighting → Notion code blocks
- Bullet points and numbered lists → Notion list items
- Inline formatting (bold, italic, code) → Notion rich text
- Language mapping: jinja2→html, yml→yaml, dockerfile→docker

#### Example Usage Patterns

```bash
# Upload project documentation
python notion_cli.py upload README.md --parent "Personal Website" --title "Project Name - Documentation"

# Upload all markdown files from a directory
python notion_cli.py upload docs/*.md --parent "Personal Website"

# Search for existing content before uploading
python notion_cli.py search "project name"

# List all pages to find appropriate parent
python notion_cli.py list --type pages
```

#### Error Handling
- If parent page not found, tool will list available options
- Tool handles unsupported languages by mapping to closest supported type
- Large files are uploaded in chunks to respect API limits
- Token is securely stored in ~/.notion-cli/config.json

### Development Notes
- Tool built with Python 3.12+ and notion-client library
- Uses official Notion API with proper authentication
- Supports batch operations and wildcard file patterns
- Configuration persists between sessions

### Integration with Other Projects
To use this tool in other repositories, either:
1. Copy these instructions to other CLAUDE.md files
2. Install globally using `./install.sh` 
3. Reference the full path to the tool from anywhere