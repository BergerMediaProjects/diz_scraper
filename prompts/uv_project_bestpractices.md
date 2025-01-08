
# Best Practices for Setting Up and Managing a Python Project

## Setting Up a Project

1. **Create and Initialize the Project:**
   ```bash
   uv init my-project
   cd my-project
   ```
   Alternatively, initialize in an existing directory:
   ```bash
   mkdir my-project
   cd my-project
   uv init
   ```

2. **Default Dependencies to Install:**
   Always include the following baseline dependencies for a robust development environment:
   - `pytest`: For testing.
   - `black`: For code formatting.
   - `flake8`: For linting.
   - `isort`: For organizing imports.
   - `mypy`: For type checking.
   - `ipython`: For an enhanced interactive shell.

   Install them as dev dependencies:
   ```bash
   uv add pytest black flake8 isort mypy ipython --group dev
   ```

3. **Set Python Version:**
   Specify the Python version in `.python-version` to ensure consistency:
   ```bash
   echo "3.x" > .python-version
   ```

---

## Running Commands

- **Run Scripts Consistently:**
  Always use `uv run` to execute scripts or commands in a consistent environment:
  ```bash
  uv run my_script.py
  ```

- **Run Shell Commands:**
  For interactive commands, prepend with `uv run --`:
  ```bash
  uv run -- flask run
  ```

- **Syncing the Environment:**
  `uv sync` is not required before `uv run`, as `uv run` automatically ensures the environment is up-to-date. 
  Use `uv sync` only when you want to explicitly update the environment without running a command, such as when preparing for manual activation:
  ```bash
  uv sync
  ```

---

## Development Best Practices

1. **Organize Code:**
   - Use a structured directory layout:
     ```
     .
     ├── my_project/
     │   ├── __init__.py
     │   ├── module1.py
     │   └── module2.py
     ├── tests/
     │   ├── test_module1.py
     │   └── test_module2.py
     ├── pyproject.toml
     └── README.md
     ```

2. **Maintain Clean Code:**
   - Format code using `black`:
     ```bash
     uv run -- black .
     ```
   - Lint code with `flake8`:
     ```bash
     uv run -- flake8 .
     ```
   - Organize imports using `isort`:
     ```bash
     uv run -- isort .
     ```
   - Check types with `mypy`:
     ```bash
     uv run -- mypy .
     ```

3. **Environment Variables:**
   Use `.env` files for environment-specific settings and load them in your application.

---

## Managing Packages

1. **Adding Dependencies:**
   - Add dependencies as needed:
     ```bash
     uv add requests
     ```
   - Specify version constraints:
     ```bash
     uv add 'flask>=2.0,<3.0'
     ```

2. **Removing Dependencies:**
   ```bash
   uv remove requests
   ```

3. **Updating Dependencies:**
   ```bash
   uv lock --upgrade-package flask
   ```

4. **Sync Environment:**
   After any change to dependencies or manually updating `pyproject.toml`:
   ```bash
   uv sync
   ```

5. **Locking Production Dependencies:**
   Exclude dev dependencies and lock production requirements:
   ```bash
   uv lock --prod
   ```

---

## Running Tests

1. **Write Tests:**
   Place all tests in a dedicated `tests/` directory, following the naming convention:
   ```
   test_<module_name>.py
   ```

2. **Run Tests:**
   Use `pytest` to execute tests:
   ```bash
   uv run -- pytest tests/
   ```

3. **Monitor Coverage:**
   Install and use `pytest-cov` for code coverage:
   ```bash
   uv add pytest-cov --group dev
   uv run -- pytest --cov=my_project tests/
   ```

---

## Summary

- Always use `uv` for dependency and environment management.
- Commit `pyproject.toml` and `uv.lock` to version control.
- Maintain a clear structure for code and tests.
- Regularly update and lock dependencies.
- Use automation tools like `black`, `flake8`, and `pytest` for clean and reliable code.
- Remember: `uv run` keeps your environment up-to-date, so manual `uv sync` is only necessary when explicitly preparing the environment.

By following these best practices, you ensure a consistent, maintainable, and scalable development workflow.
