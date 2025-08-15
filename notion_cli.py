#!/usr/bin/env python3
"""
Notion CLI - A command-line tool for interacting with Notion workspaces

Usage:
    notion-cli upload FILE [--parent PARENT] [--title TITLE]
    notion-cli list [--type TYPE]
    notion-cli search QUERY
    notion-cli config set TOKEN
    notion-cli config show
    notion-cli --help

Commands:
    upload      Upload markdown file(s) to Notion
    list        List pages/databases in workspace  
    search      Search workspace content
    config      Manage configuration

Options:
    --parent PARENT     Parent page name or ID for uploads
    --title TITLE       Custom title for uploaded page
    --type TYPE         Filter by type: pages, databases, all [default: all]
    -h --help          Show this help message
"""

import argparse
import os
import sys
import json
import re
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from notion_client import Client
except ImportError:
    print("❌ notion-client not installed. Run: pip install notion-client")
    sys.exit(1)


class NotionCLI:
    def __init__(self):
        self.config_dir = Path.home() / ".notion-cli"
        self.config_file = self.config_dir / "config.json"
        self.config = self.load_config()
        self.client = None
        
        if self.config.get("token"):
            self.client = Client(auth=self.config["token"])
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def save_config(self):
        """Save configuration to file"""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def ensure_authenticated(self):
        """Ensure we have a valid Notion token"""
        if not self.client:
            print("❌ No Notion token configured.")
            print("💡 Run: notion-cli config set YOUR_TOKEN")
            sys.exit(1)
    
    def markdown_to_notion_blocks(self, markdown_content: str) -> List[Dict[str, Any]]:
        """Convert markdown content to Notion blocks"""
        blocks = []
        lines = markdown_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Headers
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('# ').strip()
                
                if level == 1:
                    heading_type = "heading_1"
                elif level == 2:
                    heading_type = "heading_2"
                else:
                    heading_type = "heading_3"
                
                blocks.append({
                    "object": "block",
                    "type": heading_type,
                    heading_type: {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                })
            
            # Code blocks
            elif line.startswith('```'):
                language = line[3:].strip()
                code_lines = []
                i += 1
                
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                code_content = '\n'.join(code_lines)
                
                # Map unsupported languages to supported ones
                language_mapping = {
                    "jinja2": "html",
                    "yml": "yaml",
                    "dockerfile": "docker",
                    "": "plain text"
                }
                
                mapped_language = language_mapping.get(language.lower(), language.lower())
                if not mapped_language:
                    mapped_language = "plain text"
                
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": code_content}
                        }],
                        "language": mapped_language
                    }
                })
            
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                })
            
            # Numbered lists
            elif re.match(r'^\d+\. ', line):
                text = re.sub(r'^\d+\. ', '', line).strip()
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                })
            
            # Regular paragraphs
            else:
                # Handle inline formatting (bold, italic, code)
                rich_text = self.parse_inline_formatting(line)
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": rich_text
                    }
                })
            
            i += 1
        
        return blocks
    
    def parse_inline_formatting(self, text: str) -> List[Dict[str, Any]]:
        """Parse inline markdown formatting like **bold**, *italic*, `code`"""
        rich_text = []
        
        # Simple approach - split by formatting markers
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
        
        for part in parts:
            if not part:
                continue
                
            if part.startswith('**') and part.endswith('**'):
                # Bold text
                content = part[2:-2]
                rich_text.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"bold": True}
                })
            elif part.startswith('*') and part.endswith('*'):
                # Italic text
                content = part[1:-1]
                rich_text.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"italic": True}
                })
            elif part.startswith('`') and part.endswith('`'):
                # Code text
                content = part[1:-1]
                rich_text.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"code": True}
                })
            else:
                # Regular text
                if part.strip():
                    rich_text.append({
                        "type": "text",
                        "text": {"content": part}
                    })
        
        return rich_text if rich_text else [{"type": "text", "text": {"content": text}}]
    
    def find_parent_by_name(self, parent_name: str) -> Optional[str]:
        """Find parent page ID by name"""
        try:
            results = self.client.search(query=parent_name)
            for item in results['results']:
                # Check page title
                if item['object'] == 'page':
                    title = self.get_page_title(item)
                    if title.lower() == parent_name.lower():
                        return item['id']
                # Check database title
                elif item['object'] == 'database':
                    title_list = item.get('title', [])
                    if title_list:
                        title = ''.join([t['plain_text'] for t in title_list])
                        if title.lower() == parent_name.lower():
                            return item['id']
            return None
        except Exception as e:
            print(f"❌ Error searching for parent: {e}")
            return None
    
    def get_page_title(self, page_item: Dict[str, Any]) -> str:
        """Extract title from page item"""
        title = "Untitled"
        
        # Try to get page title
        title_prop = page_item.get('properties', {}).get('title')
        if title_prop and title_prop.get('title'):
            title = ''.join([t['plain_text'] for t in title_prop['title']])
        else:
            # Try other title properties
            for prop_name, prop_value in page_item.get('properties', {}).items():
                if prop_value.get('type') == 'title' and prop_value.get('title'):
                    title = ''.join([t['plain_text'] for t in prop_value['title']])
                    break
        
        return title
    
    def get_parent_info(self, parent_id: str) -> Dict[str, Any]:
        """Get information about a parent (page or database)"""
        try:
            # Try to get as page first
            page = self.client.pages.retrieve(parent_id)
            return {"type": "page", "data": page}
        except Exception:
            try:
                # Try to get as database
                database = self.client.databases.retrieve(parent_id)
                return {"type": "database", "data": database}
            except Exception:
                # Fallback - assume it's a page
                return {"type": "page", "data": None}
    
    def get_database_title_property(self, database_id: str) -> str:
        """Get the title property name for a database"""
        try:
            database = self.client.databases.retrieve(database_id)
            for prop_name, prop_details in database['properties'].items():
                if prop_details['type'] == 'title':
                    return prop_name
            # Fallback
            return "Name"
        except Exception:
            return "Name"
    
    def get_or_create_documentation_parent(self, prefer_pages=True) -> str:
        """Get or create a Documentation parent page"""
        # First, try to find existing "Documentation" page
        doc_id = self.find_parent_by_name("Documentation")
        if doc_id:
            print("📁 Using existing 'Documentation' page as parent")
            return doc_id
        
        if prefer_pages:
            # Create a new "Documentation" page under Personal Website
            personal_website_id = self.find_parent_by_name("Personal Website")
            if personal_website_id:
                print("📝 Creating 'Documentation' page under 'Personal Website'")
                return self.create_documentation_page(personal_website_id)
            
            # Fallback to any available page
            try:
                results = self.client.search(query="")
                pages = [item for item in results['results'] if item['object'] == 'page']
                if pages:
                    parent_id = pages[0]['id']
                    print(f"📝 Creating 'Documentation' page under '{self.get_page_title(pages[0])}'")
                    return self.create_documentation_page(parent_id)
            except Exception:
                pass
        else:
            # Original behavior - use Project Planner database
            project_planner_id = self.find_parent_by_name("Project Planner")
            if project_planner_id:
                print("📁 Using 'Project Planner' database as parent")
                return project_planner_id
        
        # Final fallback to "Personal Website" 
        personal_website_id = self.find_parent_by_name("Personal Website")
        if personal_website_id:
            print("📁 Using 'Personal Website' as parent")
            return personal_website_id
        
        raise Exception("No suitable parent page found. Please specify a parent page.")
    
    def create_documentation_page(self, parent_id: str) -> str:
        """Create a Documentation page under the given parent"""
        try:
            page = self.client.pages.create(
                parent={"page_id": parent_id},
                properties={
                    "title": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "Documentation"}
                            }
                        ]
                    }
                }
            )
            print(f"✅ Created 'Documentation' page: {page['url']}")
            return page['id']
        except Exception as e:
            print(f"❌ Failed to create Documentation page: {e}")
            return parent_id  # Fallback to using the parent directly
    
    def cmd_upload(self, args):
        """Upload markdown file(s) to Notion"""
        self.ensure_authenticated()
        
        # Handle glob patterns
        files = []
        for pattern in args.files:
            if '*' in pattern:
                files.extend(glob.glob(pattern))
            else:
                files.append(pattern)
        
        if not files:
            print("❌ No files found to upload")
            return
        
        # Find parent page
        parent_id = None
        if args.parent:
            if args.parent.startswith('24f8f973-'):  # Looks like an ID
                parent_id = args.parent
            else:
                parent_id = self.find_parent_by_name(args.parent)
                if not parent_id:
                    print(f"❌ Parent page '{args.parent}' not found")
                    return
        else:
            # Auto-select smart default parent
            try:
                prefer_pages = not args.as_project  # Default to pages unless --as-project is specified
                parent_id = self.get_or_create_documentation_parent(prefer_pages)
                if args.as_project:
                    print("💡 No parent specified, creating as project")
                else:
                    print("💡 No parent specified, creating as standalone page")
            except Exception as e:
                print(f"❌ {e}")
                print("💡 Available pages:")
                self.cmd_list(type('obj', (object,), {'type': 'pages'})())
                return
        
        # Upload each file
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            print(f"🚀 Uploading {file_path}...")
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate title
            if args.title:
                title = args.title
            else:
                title = Path(file_path).stem.replace('_', ' ').replace('-', ' ').title()
            
            # Convert to blocks
            blocks = self.markdown_to_notion_blocks(content)
            
            try:
                # Determine parent type (page or database)
                parent_info = self.get_parent_info(parent_id)
                
                if parent_info['type'] == 'database':
                    # Find the title property name
                    title_prop_name = self.get_database_title_property(parent_id)
                    
                    # Create page in database
                    page = self.client.pages.create(
                        parent={"database_id": parent_id},
                        properties={
                            title_prop_name: {
                                "title": [
                                    {
                                        "type": "text",
                                        "text": {"content": title}
                                    }
                                ]
                            }
                        }
                    )
                else:
                    # Create page under another page
                    page = self.client.pages.create(
                        parent={"page_id": parent_id},
                        properties={
                            "title": {
                                "title": [
                                    {
                                        "type": "text",
                                        "text": {"content": title}
                                    }
                                ]
                            }
                        }
                    )
                
                # Add content blocks (in chunks)
                chunk_size = 100
                for i in range(0, len(blocks), chunk_size):
                    chunk = blocks[i:i + chunk_size]
                    self.client.blocks.children.append(
                        block_id=page['id'],
                        children=chunk
                    )
                
                print(f"✅ Uploaded: {title}")
                print(f"🔗 URL: {page['url']}")
                print()
                
            except Exception as e:
                print(f"❌ Error uploading {file_path}: {e}")
    
    def cmd_list(self, args):
        """List pages/databases in workspace"""
        self.ensure_authenticated()
        
        try:
            results = self.client.search(query="")
            items = results['results']
            
            if args.type != 'all':
                if args.type == 'pages':
                    items = [item for item in items if item['object'] == 'page']
                elif args.type == 'databases':
                    items = [item for item in items if item['object'] == 'database']
            
            print(f"📋 Found {len(items)} {args.type}:")
            print()
            
            for item in items:
                item_type = item['object']
                
                if item_type == 'page':
                    title = self.get_page_title(item)
                elif item_type == 'database':
                    title_list = item.get('title', [])
                    title = ''.join([t['plain_text'] for t in title_list]) if title_list else "Untitled"
                
                icon = "📄" if item_type == "page" else "🗃️"
                print(f"  {icon} {title}")
                print(f"     ID: {item['id']}")
                print(f"     URL: {item['url']}")
                print()
                
        except Exception as e:
            print(f"❌ Error listing items: {e}")
    
    def cmd_search(self, args):
        """Search workspace content"""
        self.ensure_authenticated()
        
        try:
            results = self.client.search(query=args.query)
            items = results['results']
            
            print(f"🔍 Search results for '{args.query}' ({len(items)} found):")
            print()
            
            for item in items:
                item_type = item['object']
                
                if item_type == 'page':
                    title = self.get_page_title(item)
                elif item_type == 'database':
                    title_list = item.get('title', [])
                    title = ''.join([t['plain_text'] for t in title_list]) if title_list else "Untitled"
                
                icon = "📄" if item_type == "page" else "🗃️"
                print(f"  {icon} {title}")
                print(f"     {item['url']}")
                print()
                
        except Exception as e:
            print(f"❌ Error searching: {e}")
    
    def cmd_config(self, args):
        """Manage configuration"""
        if args.action == 'set':
            if not args.token:
                print("❌ Token required")
                return
            
            self.config['token'] = args.token
            self.save_config()
            self.client = Client(auth=args.token)
            print("✅ Token saved successfully")
            
        elif args.action == 'show':
            if self.config.get('token'):
                masked_token = self.config['token'][:10] + "..." + self.config['token'][-4:]
                print(f"🔑 Token: {masked_token}")
                print(f"📁 Config: {self.config_file}")
            else:
                print("❌ No token configured")


def main():
    parser = argparse.ArgumentParser(
        description="Notion CLI - Upload and manage content in your Notion workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload markdown file(s) to Notion')
    upload_parser.add_argument('files', nargs='+', help='Markdown file(s) to upload (supports wildcards)')
    upload_parser.add_argument('--parent', help='Parent page name or ID')
    upload_parser.add_argument('--title', help='Custom title for the page')
    upload_parser.add_argument('--as-project', action='store_true', help='Create as project in database (default: create as standalone page)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List pages/databases in workspace')
    list_parser.add_argument('--type', choices=['pages', 'databases', 'all'], default='all', 
                           help='Type of items to list')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search workspace content')
    search_parser.add_argument('query', help='Search query')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='action', help='Config actions')
    
    set_parser = config_subparsers.add_parser('set', help='Set configuration')
    set_parser.add_argument('token', help='Notion integration token')
    
    config_subparsers.add_parser('show', help='Show current configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = NotionCLI()
    
    if args.command == 'upload':
        cli.cmd_upload(args)
    elif args.command == 'list':
        cli.cmd_list(args)
    elif args.command == 'search':
        cli.cmd_search(args)
    elif args.command == 'config':
        cli.cmd_config(args)


if __name__ == "__main__":
    main()