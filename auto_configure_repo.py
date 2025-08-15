#!/usr/bin/env python3
"""
Auto-configuration script for Notion CLI in new repositories

This script automatically adds Notion CLI instructions to CLAUDE.md files
when called from any repository directory.
"""

import os
import sys
from pathlib import Path

NOTION_CLI_INSTRUCTIONS = """
## Notion CLI Integration

The user has a custom Notion CLI tool available globally via the `notion` command.

### Quick Usage
```bash
# Get help and see available commands
notion --help

# Upload markdown files to user's Notion workspace
notion upload README.md --parent "Personal Website"
notion upload docs/*.md --parent "Projects"

# List workspace content
notion list --type pages
notion list --type databases

# Search workspace
notion search "documentation"

# Check configuration
notion config show
```

### Available Parent Pages
- "Personal Website" (main landing page)
- "Job Application Tracker"
- "Project Planner" (database)
- "Monthly Budget"
- "Weekly To-do List"

### When to Use Notion CLI
- User asks to upload documentation to Notion
- User wants to share project files with their Notion workspace
- User requests creating Notion pages from markdown content
- User asks to search or explore their Notion workspace

### Markdown Conversion Features
- Headers (H1, H2, H3) → Notion heading blocks
- Code blocks with syntax highlighting → Notion code blocks
- Bullet points and numbered lists → Notion list items
- Inline formatting (bold, italic, code) → Notion rich text
- Language mapping: jinja2→html, yml→yaml, dockerfile→docker

### Configuration
- Tool is pre-configured with user's Notion integration token
- Config stored in ~/.notion-cli/config.json
- No additional setup required

### Error Handling
- If parent page not found, tool will suggest alternatives
- Large files uploaded in chunks to respect API limits
- Unsupported languages automatically mapped to supported types
"""

def update_claude_md():
    """Add Notion CLI instructions to CLAUDE.md in current directory"""
    current_dir = Path.cwd()
    claude_md_path = current_dir / "CLAUDE.md"
    
    # Check if CLAUDE.md exists
    if not claude_md_path.exists():
        print("❌ No CLAUDE.md found in current directory")
        print("💡 Run /init first to create a CLAUDE.md file")
        return False
    
    # Read existing content
    with open(claude_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Notion CLI instructions already exist
    if "Notion CLI Integration" in content:
        print("✅ Notion CLI instructions already present in CLAUDE.md")
        return True
    
    # Add Notion CLI instructions
    updated_content = content + NOTION_CLI_INSTRUCTIONS
    
    # Write back
    with open(claude_md_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Added Notion CLI instructions to {claude_md_path}")
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Just check if notion command is available
        print("🔍 Checking Notion CLI availability...")
        try:
            import subprocess
            result = subprocess.run([
                "python", 
                "/Users/johndurkin/personal/zaumac/notion-cli/notion_cli.py", 
                "--help"
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Notion CLI available")
                print("🎯 Usage: notion upload README.md --parent 'Personal Website'")
                return True
            else:
                print("❌ Notion CLI not available")
                return False
        except Exception as e:
            print(f"❌ Error checking Notion CLI: {e}")
            return False
    
    print("🚀 Auto-configuring repository for Notion CLI...")
    success = update_claude_md()
    
    if success:
        print("\n🎉 Repository configured!")
        print("📝 Claude can now use: notion upload README.md --parent 'Personal Website'")
    
    return success

if __name__ == "__main__":
    main()