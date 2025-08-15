# 🚀 Notion Claude CLI

**The complete command-line interface for your Notion workspace.** Upload, create, search, and manage your entire Notion workspace from the terminal - just like using the web app, but faster and scriptable.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Why This Matters

**Stop being limited by nested hierarchies.** Most Notion tools force you to create pages inside existing pages. This CLI gives you the **same power as the Notion web app** - create pages anywhere, organize however you want.

## ✨ Full Workspace Control

- 🏠 **Top-level pages** - Create pages at your workspace root (like "Projects", "Notes", "Documents")
- 📊 **Database integration** - Add pages to databases, create new databases, query existing ones
- 🔍 **Complete workspace access** - Search, list, and navigate your entire Notion workspace
- 📝 **Rich content creation** - Full markdown support with proper formatting preservation
- ⚡ **Batch operations** - Upload entire documentation sites, process multiple files
- 🤖 **Automation ready** - Script your Notion workflows, integrate with CI/CD
- 🔐 **Full security model** - OAuth authentication with granular permissions control

## 🏗️ What Are "Top-Level Pages"?

In Notion's web app, you can create pages directly in your workspace sidebar - these become **top-level pages** like:
- 📝 "Meeting Notes" (not buried under another page)
- 🚀 "Project Alpha" (standalone project workspace)  
- 📚 "Documentation Hub" (main documentation entry point)
- 💡 "Ideas & Research" (your personal knowledge base)

**Most CLI tools can only create nested pages** (pages inside other pages). This CLI gives you **full workspace-level control** - the same power you have clicking "New Page" in Notion's sidebar.

## 🌟 Real-World Examples

### Enterprise Documentation
```bash
# Create a complete documentation site at workspace level
notion-cli upload README.md --title "API Documentation"
notion-cli upload docs/api/*.md --parent "API Documentation" 
notion-cli upload docs/guides/*.md --parent "API Documentation"
# Result: Professional docs site accessible from sidebar
```

### Project Management
```bash
# Create project workspace at top level
notion-cli upload project-overview.md --title "Project Phoenix"
notion-cli upload requirements.md --parent "Project Phoenix"
notion-cli upload architecture.md --parent "Project Phoenix"
# Result: Complete project hub in workspace sidebar
```

### Knowledge Base
```bash
# Build searchable knowledge base
notion-cli upload research/*.md --parent "Research Database"
notion-cli upload notes/*.md --parent "Research Database"
# Result: Centralized knowledge accessible to whole team
```

### CI/CD Integration
```bash
# Automated documentation deployment
# In your GitHub Actions:
notion-cli upload CHANGELOG.md --title "Release Notes v2.1"
notion-cli upload docs/*.md --parent "Product Documentation"
# Result: Auto-updated docs on every release
```

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

## 🎯 Roadmap: Complete Notion CLI Suite

### Phase 1: Content Management (Current)
- [x] **Top-level page creation** - Full workspace control
- [x] **Markdown upload** - Rich formatting preservation
- [x] **OAuth authentication** - Secure workspace access
- [ ] **Database creation** - Create new databases from CLI
- [ ] **Template system** - Predefined page templates

### Phase 2: Advanced Operations
- [ ] **Bidirectional sync** - Export Notion pages to markdown
- [ ] **Database querying** - SQL-like queries for Notion databases
- [ ] **Bulk operations** - Process hundreds of files with progress bars
- [ ] **Page relationships** - Create linked pages and references
- [ ] **Advanced formatting** - Tables, callouts, embeds

### Phase 3: Automation & Integration
- [ ] **Workflow automation** - Script complex Notion operations
- [ ] **Git integration** - Sync repos with Notion workspaces
- [ ] **CI/CD plugins** - GitHub Actions, Jenkins integrations
- [ ] **Multi-workspace** - Manage multiple Notion accounts
- [ ] **API webhooks** - Real-time Notion updates

### Phase 4: Enterprise Features
- [ ] **Team collaboration** - Shared CLI configurations
- [ ] **Permission management** - Fine-grained access control
- [ ] **Audit logging** - Track all CLI operations
- [ ] **Enterprise SSO** - SAML/OAuth enterprise auth
- [ ] **Backup & restore** - Complete workspace backups

**Vision**: Make Notion as scriptable and automatable as any modern dev tool.