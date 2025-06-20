# How to Set Up and Use Taskmaster for Project Management

This guide provides detailed instructions for configuring Taskmaster, our AI-powered project management tool, for use within this repository. Following these steps will enable you to interact with the project's task list, contribute to our development workflow, and leverage AI for planning and execution.

## The Workflow Philosophy

All new features and significant changes must be planned using Taskmaster before implementation. This "plan-then-execute" model ensures every architectural decision is thought-out and documented.

1.  **Propose & Plan:** A Product Requirements Document (PRD) is created or updated in `.taskmaster/docs/prd.md` to outline the feature.
2.  **Generate Tasks:** The PRD is parsed by Taskmaster (`task-master parse-prd`) to create a structured list of tasks.
3.  **Implement:** Development work begins, following the generated tasks.
4.  **Document:** Upon completion, a detailed changelog is created, linking the work back to the original task.

## MCP (Model Control Protocol) Setup

The recommended way to interact with Taskmaster is via MCP, which integrates the tool directly into your code editor (e.g., Cursor, VS Code).

### 1. API Key Requirements

Taskmaster utilizes AI models from various providers. To use its AI-powered features, you must provide at least one API key. Add the relevant keys to your MCP configuration file.

-   **Required (at least one):**
    -   `ANTHROPIC_API_KEY` (for Claude models)
    -   `OPENAI_API_KEY`
    -   `GOOGLE_API_KEY` (for Gemini models)
    -   `MISTRAL_API_KEY`
    -   `XAI_API_KEY`
    -   `OPENROUTER_API_KEY`
-   **Recommended for Research:**
    -   `PERPLEXITY_API_KEY`

### 2. Manual MCP Configuration

Create or update the MCP configuration file in your editor's settings directory.

-   **Cursor:** `~/.cursor/mcp.json`
-   **VS Code (Project-level):** `.vscode/mcp.json`

Add the following server configuration, replacing the placeholder keys with your actual API keys. You can remove any providers you don't use.

```json
{
  "mcpServers": {
    "taskmaster-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",
        "OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"
      }
    }
  }
}
```

### 3. Enable in Cursor (Cursor-only)

If you are using Cursor, open **Settings (Ctrl+Shift+J)**, navigate to the **MCP** tab, and enable `task-master-ai` with the toggle.

### 4. Common Commands

Once configured, you can use natural language in your editor's chat pane to manage the project:

-   **`Initialize taskmaster-ai in my project`**
-   **`Can you parse my PRD at .taskmaster/docs/prd.md?`**
-   **`What's the next task I should work on?`**
-   **`Can you help me implement task 3?`**
-   **`Research the latest best practices for X`** 