# Quickstart Guide: In-Memory Python Console Todo Application

**Feature**: 001-cli-todo (Phase I)
**Date**: 2026-01-03
**Estimated Setup Time**: 5 minutes

## Prerequisites

- **Python 3.13+** installed on your system
- **Terminal/Command Prompt** access
- **Internet connection** (for UV installation only)

**Check Python Version**:
```bash
python --version
# Expected output: Python 3.13.0 or higher
```

If Python 3.13+ is not installed:
- Windows/macOS: Download from [python.org](https://www.python.org/downloads/)
- Linux: `sudo apt install python3.13` (Ubuntu) or equivalent

## Installation

### Step 1: Install UV (Package Manager)

UV is a fast, modern Python package manager. Install it globally:

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** (PowerShell):
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Alternative** (via pip):
```bash
pip install uv
```

**Verify Installation**:
```bash
uv --version
# Expected output: uv 0.x.x or higher
```

### Step 2: Navigate to Project Directory

```bash
cd path/to/evolution-of-todo/phase-1-cli
```

**Note**: If `phase-1-cli/` doesn't exist yet, it will be created during implementation (`/sp.implement` command).

### Step 3: Run the Application

UV automatically creates a virtual environment and runs the application:

```bash
uv run src/main.py
```

**First Run**: UV will:
1. Create a `.venv/` directory (virtual environment)
2. Install Python 3.13+ if needed
3. Launch the Todo application

## Using the Application

### Main Menu

When you run the application, you'll see:

```
╔═══════════════════════════════════════╗
║     Todo Application - Phase I        ║
║         (In-Memory Only)              ║
╚═══════════════════════════════════════╝

=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit

Enter your choice (1-6): _
```

### Operation Guide

#### 1. Add Task

**Action**: Create a new task

**Steps**:
1. Select option `1` from the menu
2. Enter task description when prompted
3. Task is added and confirmation message shown

**Example**:
```
Enter your choice (1-6): 1
Enter task description: Buy groceries
✓ Task added: Buy groceries
```

**Validation**:
- Description cannot be empty
- Maximum 500 characters
- Leading/trailing whitespace automatically trimmed

---

#### 2. View Tasks

**Action**: Display all tasks with their status

**Steps**:
1. Select option `2` from the menu
2. All tasks displayed with index numbers and completion status

**Example**:
```
Enter your choice (1-6): 2

Your Tasks:
1. [ ] Buy groceries
2. [✓] Write report
3. [ ] Call dentist

Total: 3 tasks (1 completed, 2 pending)
```

**Empty List**:
```
No tasks yet. Add your first task!
```

---

#### 3. Update Task

**Action**: Change a task's description

**Steps**:
1. Select option `3` from the menu
2. Enter task number (from View Tasks)
3. Enter new description
4. Task updated and confirmation shown

**Example**:
```
Enter your choice (1-6): 3
Enter task number to update: 1
Current description: Buy groceries
Enter new description: Buy groceries and milk
✓ Task updated: Buy groceries and milk
```

**Validation**:
- Task number must exist
- New description follows same rules as Add Task

---

#### 4. Delete Task

**Action**: Remove a task permanently

**Steps**:
1. Select option `4` from the menu
2. Enter task number to delete
3. Task removed and confirmation shown

**Example**:
```
Enter your choice (1-6): 4
Enter task number to delete: 2
✓ Task deleted: Write report

Remaining tasks renumbered.
```

**Note**: Task numbers are automatically renumbered after deletion, but internal IDs are preserved.

---

#### 5. Mark Task Complete

**Action**: Mark a task as done

**Steps**:
1. Select option `5` from the menu
2. Enter task number to mark complete
3. Task status changed and confirmation shown

**Example**:
```
Enter your choice (1-6): 5
Enter task number to mark complete: 1
✓ Task marked complete: Buy groceries and milk

View tasks to see updated status.
```

**Idempotent**: Can mark the same task complete multiple times without error.

---

#### 6. Exit

**Action**: Close the application

**Steps**:
1. Select option `6` from the menu
2. Application closes gracefully

**Example**:
```
Enter your choice (1-6): 6

Thank you for using Todo Application!
Your tasks are stored in memory only.
Data will be lost when the program exits.

Goodbye!
```

**Alternative**: Press `Ctrl+C` at any time to exit gracefully.

## Quick Example Session

Complete workflow demonstrating all features:

```bash
$ uv run src/main.py

=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit

Enter your choice (1-6): 1
Enter task description: Buy groceries
✓ Task added: Buy groceries

Enter your choice (1-6): 1
Enter task description: Write report
✓ Task added: Write report

Enter your choice (1-6): 1
Enter task description: Call dentist
✓ Task added: Call dentist

Enter your choice (1-6): 2

Your Tasks:
1. [ ] Buy groceries
2. [ ] Write report
3. [ ] Call dentist

Total: 3 tasks (0 completed, 3 pending)

Enter your choice (1-6): 5
Enter task number to mark complete: 1
✓ Task marked complete: Buy groceries

Enter your choice (1-6): 3
Enter task number to update: 2
Current description: Write report
Enter new description: Write quarterly report
✓ Task updated: Write quarterly report

Enter your choice (1-6): 4
Enter task number to delete: 3
✓ Task deleted: Call dentist

Enter your choice (1-6): 2

Your Tasks:
1. [✓] Buy groceries
2. [ ] Write quarterly report

Total: 2 tasks (1 completed, 1 pending)

Enter your choice (1-6): 6

Thank you for using Todo Application!
Goodbye!

$ # Re-running the app shows empty list (no persistence)
$ uv run src/main.py

Enter your choice (1-6): 2
No tasks yet. Add your first task!
```

## Error Handling Examples

### Empty Description

```
Enter task description:
✗ Error: Task description cannot be empty. Please enter a valid description.

Enter task description: _
```

### Description Too Long

```
Enter task description: [500+ characters]
✗ Error: Task description too long (501 characters, max 500).

Enter task description: _
```

### Invalid Task Number

```
Enter task number to update: 99
✗ Error: Invalid task number. Please enter a number between 1 and 3.

Enter task number to update: _
```

### Non-Numeric Input

```
Enter task number to mark complete: abc
✗ Error: Please enter a valid number.

Enter task number to mark complete: _
```

### Empty List Operations

```
Enter your choice (1-6): 4
✗ Error: No tasks available. Add a task first.

Enter your choice (1-6): _
```

## Common Issues

### Issue: "uv: command not found"

**Solution**: UV not installed or not in PATH. Run installation command again and restart terminal.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or ~/.zshrc for zsh

# Windows (PowerShell as Administrator)
irm https://astral.sh/uv/install.ps1 | iex
# Restart PowerShell
```

### Issue: "Python 3.13 not found"

**Solution**: UV will attempt to download Python 3.13 automatically. If this fails:

1. Manually install Python 3.13+ from [python.org](https://www.python.org/downloads/)
2. Or modify `.python-version` file to use available version (3.11+ minimum):
   ```bash
   echo "3.11" > phase-1-cli/.python-version
   ```

### Issue: "Module not found" errors

**Solution**: Ensure you're running from the correct directory and using `uv run`:

```bash
# From repository root
cd phase-1-cli
uv run src/main.py

# NOT: python src/main.py (misses UV environment setup)
```

### Issue: Unicode characters not displaying (✓ shows as ?)

**Solution**: Terminal encoding issue. Update terminal to use UTF-8 encoding:

- **Windows CMD**: `chcp 65001`
- **Windows PowerShell**: Already UTF-8 by default
- **macOS/Linux**: Already UTF-8 by default

**Fallback**: Application automatically uses ASCII `[X]` if UTF-8 unavailable.

## Tips and Best Practices

### Task Description Guidelines

**Good Descriptions** (concise, actionable):
- ✓ "Buy groceries for dinner"
- ✓ "Call dentist to schedule appointment"
- ✓ "Review Q4 budget report"

**Avoid** (vague, overly long):
- ✗ "Stuff"
- ✗ "Do the thing I was supposed to do yesterday that I forgot about..."
- ✗ [500-character essay]

### Workflow Tips

1. **Add Multiple Tasks First**: Use "Add Task" several times before organizing
2. **View Often**: Check status frequently with "View Tasks"
3. **Mark Complete as You Go**: Immediate satisfaction from [✓] marks
4. **Delete Completed Tasks**: Keep list manageable by removing finished items
5. **Update Instead of Delete+Add**: Use "Update Task" to refine descriptions

### Keyboard Shortcuts

- **Enter**: Submit input
- **Ctrl+C**: Exit application gracefully (same as option 6)
- **Ctrl+D** (Unix) / **Ctrl+Z** (Windows): EOF signal (also exits)

## Data Persistence Notice

⚠️ **IMPORTANT**: Phase I stores tasks **in-memory only**.

**This means**:
- ✅ Tasks persist during the program session
- ✅ You can add, view, update, delete freely
- ❌ Tasks are **lost when you exit** the application
- ❌ Closing terminal window loses all data
- ❌ No file saving or database storage

**Future Phases**:
- **Phase II**: Adds database persistence (tasks survive restart)
- **Phase III**: Adds AI-powered task management
- **Phase IV**: Adds Kubernetes deployment
- **Phase V**: Adds cloud storage and event-driven architecture

## Development and Testing

### Running Tests

Phase I uses **manual acceptance testing** (automated tests in Phase II).

**Test Procedure**:
1. Review acceptance scenarios in `specs/001-cli-todo/spec.md`
2. Execute test steps from `phase-1-cli/tests/acceptance_tests.md`
3. Verify expected outcomes match actual results

**Example Test**:
```
Test: Add task with empty description
Steps:
  1. Run application
  2. Select option 1 (Add Task)
  3. Press Enter without typing description
Expected: Error message "Task description cannot be empty"
Actual: [Record actual behavior]
Status: [Pass/Fail]
```

### Code Quality Checks

**PEP 8 Compliance** (optional, requires ruff):
```bash
# Install ruff
uv pip install ruff

# Check code style
ruff check phase-1-cli/src/

# Auto-fix issues
ruff check --fix phase-1-cli/src/
```

**Type Checking** (optional, requires mypy):
```bash
# Install mypy
uv pip install mypy

# Run type checker
mypy phase-1-cli/src/
```

## Project Structure

```
phase-1-cli/
├── src/
│   ├── models/
│   │   └── task.py           # Task entity
│   ├── services/
│   │   └── todo_service.py   # Business logic
│   ├── cli/
│   │   ├── menu.py           # Menu display
│   │   └── handlers.py       # Command handlers
│   └── main.py               # Entry point
├── tests/
│   └── acceptance_tests.md   # Manual test scenarios
├── .python-version           # Python 3.13
├── pyproject.toml            # UV configuration
├── README.md                 # Project overview
└── .gitignore                # Git exclusions
```

## Next Steps

After successfully running Phase I:

1. **Explore the Code**: Review `src/` directory to understand implementation
2. **Read Documentation**: See `specs/001-cli-todo/` for detailed design docs
3. **Run Acceptance Tests**: Execute test scenarios from `tests/acceptance_tests.md`
4. **Prepare for Phase II**: Review Phase II requirements (web application with database)

## Support and Resources

**Documentation**:
- Feature Specification: `specs/001-cli-todo/spec.md`
- Implementation Plan: `specs/001-cli-todo/plan.md`
- Data Model: `specs/001-cli-todo/data-model.md`
- Service Contract: `specs/001-cli-todo/contracts/todo_service.md`

**Project Links**:
- Repository: `evolution-of-todo/` (root)
- Branch: `001-cli-todo`
- Constitution: `.specify/memory/constitution.md`

**External Resources**:
- [UV Documentation](https://github.com/astral-sh/uv)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)

---

**Version**: 1.0.0
**Last Updated**: 2026-01-03
**Phase**: I - In-Memory Console Application
