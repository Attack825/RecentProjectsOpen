# Contributing

Thanks for taking the time to improve RecentProjectsOpen.

## Development Setup

1. Fork and clone the repository.

2. Create a virtual environment and install dependencies:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate

   # Runtime + development dependencies (ruff, mypy, pre-commit)
   pip install -r requirements-dev.txt
   pre-commit install
   ```

3. Verify the setup:

   ```powershell
   python -m unittest discover -s test -p "test_*.py"
   ruff check . ; ruff format --check .
   mypy
   ```

All three checks also run in CI (unit tests on Python 3.9 / 3.11 / 3.13).

## Adding a New Application

The registration name is the single source of truth. For `MYAPP` it determines:

| Thing | Value |
| --- | --- |
| Settings keys | `MYAPP_DOWNLOAD` / `MYAPP_STORAGE` (see `src/core/naming.py`) |
| Icon | `icons/MYAPP.png` |
| Trigger | the `acronyms` you set (e.g. `my` → `r my`) |

1. Create `src/application/myapp.py`:

   ```python
   from ..application.base_jetbrains import Jetbrains
   from ..core.registry import ApplicationRegistry


   @ApplicationRegistry.register("MYAPP")
   class MyApp(Jetbrains):
       def __init__(self, download_path: str, storage_file: str):
           super().__init__(download_path, storage_file)
           self.name = "MYAPP"    # config keys + icon are derived from this
           self.acronyms = "my"   # used as: r my <query>
   ```

   Files under `src/application/*.py` are imported automatically by
   `ApplicationRegistry.load_applications()`, so there is no list to update.

2. Implement `get_projects()`:

   - extend `BaseApplication` for a custom file format, or `BaseJetbrains` /
     `Vscode` when the data is the usual `recentProjects.xml` / `storage.json`;
   - call `self.validate_storage()` before parsing, so a missing file raises
     `StorageFileNotFound` and the user gets a warning item instead of a silent
     empty result;
   - return `list[Project]`.

3. Add `icons/MYAPP.png`, and document `MYAPP_DOWNLOAD` / `MYAPP_STORAGE` in the
   README's Program Path example plus the acronym table.

4. Add `test/test_myapp.py` with a sanitized sample under `test/mock_data/`.
   Cover the happy path and the missing-file path (`StorageFileNotFound`).

5. Run the checks from [Development Setup](#development-setup) and open a PR.

## Code Style and Checks

- `pre-commit` runs `ruff-format` and `ruff-check --fix` on every commit.
- `mypy` uses the baseline in [mypy.ini](mypy.ini): Python 3.9, Windows platform,
  `check_untyped_defs`. New code must pass it.
- Keep one responsibility per pull request. State the responsibility, dependencies,
  risks, and verification evidence in the PR / commit message.
