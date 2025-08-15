# Creating the Public Notion Template Page

## Instructions for Creating the OAuth Template Page

1. **Create the main template page in your Notion workspace:**
   - Title: "🚀 Notion AI CLI Workspace Template"
   - Use the content from `template-content.md`

2. **Create the sub-pages and database structure:**

### A. Documentation Hub (Page)
- Create a new page called "📝 Documentation Hub"
- Add sample sub-pages:
  - "API Reference"
  - "Installation Guide" 
  - "Deployment Guide"
  - "Troubleshooting"

### B. Development Tickets (Database)
Create a database called "🎫 Development Tickets" with these properties:
- **Title** (Title): Ticket name
- **Status** (Select): Not Started, In Progress, Review, Done
- **Priority** (Select): Low, Medium, High, Critical
- **Assignee** (Person): Team member
- **Project** (Select): Backend, Frontend, DevOps, Design
- **Due Date** (Date): Target completion
- **Description** (Text): Detailed description
- **Labels** (Multi-select): Bug, Feature, Enhancement, Documentation

### C. Knowledge Base (Page)
- Create a page called "🧠 Knowledge Base"
- Add sample sub-pages:
  - "Meeting Notes"
  - "Decision Logs"
  - "Research Findings"
  - "Best Practices"

### D. CI/CD Templates (Page)  
- Create a page called "⚙️ CI/CD Templates"
- Add sample sub-pages:
  - "Release Checklist"
  - "Deployment Guide"
  - "Rollback Procedure"

3. **Make the page public:**
   - Click "Share" on the main template page
   - Toggle "Share to web" 
   - Copy the public URL
   - This URL will be used in the Notion OAuth approval form

4. **Template page URL format:**
   The public URL should look like:
   `https://notion.so/your-workspace/Notion-CLI-Workspace-Template-[page-id]`

## Benefits of This Template

When users authorize the CLI during OAuth, they'll have the option to duplicate this template, giving them:

- **Immediate value**: Ready-to-use workspace structure
- **Clear examples**: Shows how CLI integrates with real workflows  
- **Best practices**: Demonstrates proper organization
- **Development focus**: Emphasizes the CLI's strength in dev workflows

This template directly addresses the CLI's core value proposition: enabling AI-powered development workflows to manage Notion content programmatically while maintaining the rich organizational structure that makes Notion powerful across any coding assistant - Claude Code, Cursor, Windsurf, and beyond.