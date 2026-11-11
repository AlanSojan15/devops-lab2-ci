# DevOps Lab Exercise 2 — Basic CI Workflow with GitHub Actions

   ![CI](https://github.com/AlanSojan15/devops-lab2-ci/actions/workflows/ci.yml/badge.svg)

**Aim:** Design and implement a basic Continuous Integration (CI) workflow that is triggered automatically by commits, using GitHub Actions.

## Project structure

```
devops-lab2-ci/
├── .github/workflows/ci.yml   # the CI pipeline
├── app/
│   ├── calculator.py          # business logic
│   └── main.py                # Flask REST API
├── tests/
│   ├── test_calculator.py     # unit tests
│   └── test_api.py            # API tests
├── requirements.txt
└── .gitignore
```

## What the pipeline does

Every `git push` (any branch) or pull request to `main` triggers this pipeline:

| Stage | Step | Purpose |
|---|---|---|
| 1 | Checkout code | Pulls the commit onto a fresh Ubuntu runner |
| 2 | Set up Python | Installs Python 3.11 and 3.12 (matrix = 2 parallel jobs) |
| 3 | Install dependencies | `pip install -r requirements.txt` |
| 4 | Lint | `flake8` checks code style; fails the build on errors |
| 5 | Test | `pytest` runs 11 tests; any failure fails the build |
| 6 | Summary | Prints a success message with the commit SHA |

## Procedure

### Step 1 — Run it locally first
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
flake8 app tests --max-line-length=100
pytest -v                          # expect: 11 passed
python -m app.main                 # visit http://localhost:5000/add?a=2&b=3
```

### Step 2 — Create a GitHub repository
On GitHub → **New repository** → name it `devops-lab2-ci` → Public → **don't** add a README (we have one) → Create.

### Step 3 — Push the code (this first commit triggers CI)
```bash
git init
git add .
git commit -m "Initial commit: Flask app with CI workflow"
git branch -M main
git remote add origin https://github.com/<your-username>/devops-lab2-ci.git
git push -u origin main
```

### Step 4 — Watch the pipeline run
Open the repo → **Actions** tab → click the "Initial commit" run. You'll see two jobs (`3.11`, `3.12`) and each step's logs. Both should go green ✅.

### Step 5 — Demonstrate a FAILING build (important for the lab)
Break a test on purpose, e.g. in `app/calculator.py` change `return a + b` to `return a - b`:
```bash
git commit -am "Introduce bug in add()"
git push
```
The Actions tab shows a red ❌ — `test_add` and `test_add_endpoint` fail. GitHub also emails you. This proves CI catches bugs automatically on each commit.

### Step 6 — Fix it and see it go green again
Revert the change, then:
```bash
git commit -am "Fix add() bug"
git push
```
The run goes green ✅ again.

### Step 7 (optional) — Pull-request check
```bash
git checkout -b feature/power
# add a power() function + test
git commit -am "Add power operation"
git push -u origin feature/power
```
Open a Pull Request on GitHub — the CI result appears on the PR before merging.

### Step 8 — Add the status badge
Replace `<your-username>` in the badge line at the top of this README with your GitHub username and push. The badge shows the live pass/fail state.

## Screenshots to capture for the record
1. Repo with `.github/workflows/ci.yml` visible
2. Actions tab listing several runs (green and red)
3. A green run with both matrix jobs expanded
4. The red run showing the failing pytest output
5. README with the passing badge

## Workflow explained (`ci.yml`)
- `on: push / pull_request / workflow_dispatch` — the **triggers**. `push` on `"**"` means every commit on any branch.
- `jobs.build-and-test.runs-on: ubuntu-latest` — GitHub-hosted runner (a fresh VM each run).
- `strategy.matrix` — runs the same job on several Python versions in parallel.
- `uses:` — reusable actions from the marketplace (`checkout`, `setup-python`).
- `run:` — shell commands. If any command exits non-zero, the job fails and later steps are skipped.

## Result
A CI pipeline was implemented with GitHub Actions that automatically checks out, installs, lints and tests the application on every commit, reporting pass/fail status on GitHub.

## (Alternative) GitLab CI equivalent
If your lab uses GitLab, put this in `.gitlab-ci.yml` at the repo root instead:
```yaml
stages: [lint, test]

image: python:3.12

before_script:
  - pip install -r requirements.txt

lint:
  stage: lint
  script:
    - flake8 app tests --max-line-length=100

test:
  stage: test
  script:
    - pytest -v
```
View runs under **Build → Pipelines** in GitLab.
