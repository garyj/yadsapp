# Django Template Generator

Automatically converts this Django project into a reusable template via GitHub Actions.

## Quick Setup

### 1. Create Template Repository

```bash
gh repo create garyj/yads --public
```

### 2. Add GitHub Secrets

In **Settings → Secrets and variables → Actions**, add:

- `TEMPLATE_REPO_TOKEN`: Personal Access Token with `repo` permissions
- `OPENAI_API_KEY`: OpenAI API key (optional, for AI commit messages)

### 3. Update Workflow

Edit `.github/workflows/deploy-template.yml` line 34:

```yaml
repository: ${{ github.repository_owner }}/your-template-repo-name
```

### 4. Customize Template Files

Edit files in `template-files/`:

- `README.md` - Template documentation
- `.env.example` - Default environment variables
- `project_template.json` - Django template metadata

## How It Works

```
template-generator/
├── scripts/
│   └── convert_to_template.py    # Conversion script
├── template-files/               # Template-specific files
└── commit-template.txt           # LLM template for AI commit messages
```

**On push to main:**

1. Converts project (replaces `yads` → `{{ project_name }}`)
2. Syncs to template repository
3. Generates AI commit message using `llm` package
4. Commits and pushes

## Local Testing

```bash
python template-generator/scripts/convert_to_template.py
```

## Using the Template

```bash
django-admin startproject --template=https://github.com/garyj/yads/archive/main.zip myproject
```
