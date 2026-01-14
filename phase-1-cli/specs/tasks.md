# Tasks: In-Memory Python Console Todo Application

**Feature**: 001-cli-todo
**Branch**: `001-cli-todo`
**Input**: Implementation plan from `/specs/plan.md`
**Prerequisites**: spec.md (complete), plan.md (complete), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which implementation phase this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Phase I project**: `phase-1-cli/` at repository root
- Paths shown below use `phase-1-cli/` as base

---

## Phase 1: Setup - Foundation & Project Structure

**Purpose**: Initialize project structure and development environment

- [ ] T001 Create `phase-1-cli/` directory at repository root
- [ ] T002 [P] Create `phase-1-cli/src/` directory
- [ ] T003 [P] Create `phase-1-cli/src/models/` directory
- [ ] T004 [P] Create `phase-1-cli/src/services/` directory
- [ ] T005 [P] Create `phase-1-cli/src/cli/` directory
- [ ] T006 [P] Create `phase-1-cli/tests/` directory
- [ ] T007 Create `phase-1-cli/pyproject.toml` with UV configuration (project name, Python 3.13+, no dependencies)
- [ ] T008 Create `phase-1-cli/.python-version` with content `3.13`
- [ ] T009 [P] Create `phase-1-cli/src/__init__.py` (empty module file)
- [ ] T010 [P] Create `phase-1-cli/src/models/__init__.py` (empty module file)
- [ ] T011 [P] Create `phase-1-cli/src/services/__init__.py` (empty module file)
- [ ] T012 [P] Create `phase-1-cli/src/cli/__init__.py` (empty module file)
- [ ] T013 Create `phase-1-cli/.gitignore` (Python artifacts: `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`)
- [ ] T014 Create `phase-1-cli/README.md` with project title, description, and "See quickstart.md for setup"

**Checkpoint**: Directory structure matches plan.md, UV can resolve environment (`uv run --version` works in phase-1-cli/)

---

## Phase 2: Core Data Model - Task Entity

**Purpose**: Implement Task dataclass with validation

- [ ] T015 Create `phase-1-cli/src/models/task.py` with module docstring
- [ ] T016 Import `dataclass` decorator from `dataclasses` module in task.py
- [ ] T017 Define `Task` dataclass with three fields: `description: str`, `completed: bool = False`, `id: int = 0`
- [ ] T018 Add `__post_init__` method to Task for description validation (strip whitespace, check non-empty, check ≤500 chars)
- [ ] T019 Add `__str__` method to Task returning formatted string: `"[✓] description"` if complete, `"[ ] description"` if incomplete
- [ ] T020 Add `mark_complete()` method to Task setting `self.completed = True`
- [ ] T021 Add module-level docstring explaining Task entity purpose
- [ ] T022 Add type hints to all Task methods
- [ ] T023 Manual REPL test: Create valid Task, verify fields
- [ ] T024 Manual REPL test: Try creating Task with empty description, verify ValueError raised
- [ ] T025 Manual REPL test: Try creating Task with 501-char description, verify ValueError raised

**Checkpoint**: Task instances can be created with validation, `__str__` displays correctly

---

## Phase 3: Service Layer - Basic Operations (Add & View)

**Purpose**: Implement TodoService with add and view operations

- [ ] T026 Create `phase-1-cli/src/services/todo_service.py` with module docstring
- [ ] T027 Import `Task` from `models.task` and `List` from `typing` in todo_service.py
- [ ] T028 Define `TodoService` class with class docstring
- [ ] T029 Implement `__init__(self)` initializing `self._tasks: list[Task] = []` and `self._next_id: int = 1`
- [ ] T030 Implement `add_task(self, description: str) -> Task` method
- [ ] T031 In `add_task`: Strip and validate description, raise ValueError if empty or too long
- [ ] T032 In `add_task`: Create Task with `id=self._next_id`, append to `_tasks`, increment `_next_id`, return task
- [ ] T033 Implement `get_all_tasks(self) -> list[Task]` returning `self._tasks.copy()`
- [ ] T034 Add docstrings to TodoService class and both methods
- [ ] T035 Add type hints to all TodoService methods
- [ ] T036 Manual REPL test: Create service, add task, verify ID is 1
- [ ] T037 Manual REPL test: Add 3 tasks, get_all_tasks, verify length is 3 and IDs are 1, 2, 3
- [ ] T038 Manual REPL test: Try add_task with empty string, verify ValueError

**Checkpoint**: Can add tasks and retrieve them, IDs auto-increment from 1

---

## Phase 4: Service Layer - Modify Operations (Update, Delete, Complete)

**Purpose**: Complete CRUD operations in TodoService

- [ ] T039 Implement `_validate_index(self, index: int) -> None` private method in TodoService
- [ ] T040 In `_validate_index`: Raise IndexError with "No tasks available" message if `_tasks` is empty
- [ ] T041 In `_validate_index`: Raise IndexError with "Task index out of range" if index < 0 or index >= len(_tasks)
- [ ] T042 Implement `update_task(self, index: int, description: str) -> Task` method
- [ ] T043 In `update_task`: Call `_validate_index(index)`, validate new description, update task description, return task
- [ ] T044 Implement `delete_task(self, index: int) -> None` method
- [ ] T045 In `delete_task`: Call `_validate_index(index)`, remove task at index using `del self._tasks[index]`
- [ ] T046 Implement `mark_complete(self, index: int) -> Task` method
- [ ] T047 In `mark_complete`: Call `_validate_index(index)`, set `self._tasks[index].completed = True`, return task
- [ ] T048 Add docstrings to all new methods
- [ ] T049 Manual REPL test: Update task description, verify change persists
- [ ] T050 Manual REPL test: Delete middle task, verify list length decreases and remaining tasks shift
- [ ] T051 Manual REPL test: Mark task complete, verify `completed=True`
- [ ] T052 Manual REPL test: Call mark_complete twice on same task, verify idempotent (no error)
- [ ] T053 Manual REPL test: Try update_task with invalid index (99), verify IndexError
- [ ] T054 Manual REPL test: Try delete_task on empty list, verify IndexError with "No tasks available"

**Checkpoint**: All CRUD operations work, error handling robust for invalid indices

---

## Phase 5: CLI Layer - Menu System

**Purpose**: Implement menu display and input handling

- [ ] T055 Create `phase-1-cli/src/cli/menu.py` with module docstring
- [ ] T056 Define `display_menu() -> None` function printing menu header and options 1-6
- [ ] T057 In `display_menu`: Print "=== Todo Application ===" header
- [ ] T058 In `display_menu`: Print options: "1. Add Task", "2. View Tasks", "3. Update Task", "4. Delete Task", "5. Mark Task Complete", "6. Exit"
- [ ] T059 Define `get_menu_choice() -> int` function prompting "Enter your choice (1-6): "
- [ ] T060 In `get_menu_choice`: Use try/except to convert input to int
- [ ] T061 In `get_menu_choice`: If ValueError (non-numeric), print error and return -1
- [ ] T062 In `get_menu_choice`: If choice not in range 1-6, print error and return -1
- [ ] T063 In `get_menu_choice`: Return valid choice (1-6)
- [ ] T064 Add docstrings to both functions
- [ ] T065 Manual CLI test: Run `python -c "from src.cli.menu import display_menu; display_menu()"`, verify menu displays
- [ ] T066 Manual CLI test: Run menu choice function with valid input (3), verify returns 3
- [ ] T067 Manual CLI test: Run menu choice with invalid input ("abc"), verify error message and returns -1

**Checkpoint**: Menu displays correctly, input validation works, re-prompts on error

---

## Phase 6: CLI Layer - Command Handlers

**Purpose**: Implement handler functions for each menu operation

- [ ] T068 Create `phase-1-cli/src/cli/handlers.py` with module docstring
- [ ] T069 Import `TodoService` from `services.todo_service` in handlers.py
- [ ] T070 Define `handle_add_task(service: TodoService) -> None` function
- [ ] T071 In `handle_add_task`: Prompt "Enter task description: ", get input
- [ ] T072 In `handle_add_task`: Use try/except to call `service.add_task(description)`
- [ ] T073 In `handle_add_task`: On success, print "✓ Task added: {description}"
- [ ] T074 In `handle_add_task`: On ValueError, print "✗ Error: {error message}"
- [ ] T075 Define `handle_view_tasks(service: TodoService) -> None` function
- [ ] T076 In `handle_view_tasks`: Call `service.get_all_tasks()`, get task list
- [ ] T077 In `handle_view_tasks`: If empty, print "No tasks yet. Add your first task!"
- [ ] T078 In `handle_view_tasks`: If not empty, print header "Your Tasks:", then enumerate tasks with 1-based index
- [ ] T079 In `handle_view_tasks`: For each task, print "{index}. {task}" (task.__str__ shows completion status)
- [ ] T080 In `handle_view_tasks`: Print summary "Total: {count} tasks ({completed} completed, {pending} pending)"
- [ ] T081 Define `handle_update_task(service: TodoService) -> None` function
- [ ] T082 In `handle_update_task`: Prompt "Enter task number to update: ", convert to 0-based index
- [ ] T083 In `handle_update_task`: Display current description, prompt "Enter new description: "
- [ ] T084 In `handle_update_task`: Use try/except to call `service.update_task(index, new_description)`
- [ ] T085 In `handle_update_task`: On success, print "✓ Task updated"
- [ ] T086 In `handle_update_task`: On ValueError/IndexError, print "✗ Error: {message}"
- [ ] T087 Define `handle_delete_task(service: TodoService) -> None` function
- [ ] T088 In `handle_delete_task`: Prompt "Enter task number to delete: ", convert to 0-based index
- [ ] T089 In `handle_delete_task`: Use try/except to call `service.delete_task(index)`
- [ ] T090 In `handle_delete_task`: On success, print "✓ Task deleted"
- [ ] T091 In `handle_delete_task`: On IndexError, print "✗ Error: {message}"
- [ ] T092 Define `handle_mark_complete(service: TodoService) -> None` function
- [ ] T093 In `handle_mark_complete`: Prompt "Enter task number to mark complete: ", convert to 0-based index
- [ ] T094 In `handle_mark_complete`: Use try/except to call `service.mark_complete(index)`
- [ ] T095 In `handle_mark_complete`: On success, print "✓ Task marked complete"
- [ ] T096 In `handle_mark_complete`: On IndexError, print "✗ Error: {message}"
- [ ] T097 Add docstrings to all handler functions
- [ ] T098 Add type hints to all handler function signatures

**Checkpoint**: Each handler prompts correctly, calls service methods, displays results/errors

---

## Phase 7: Main Application Loop

**Purpose**: Create application entry point and main loop

- [ ] T099 Create `phase-1-cli/src/main.py` with module docstring
- [ ] T100 Import `TodoService` from `services.todo_service` in main.py
- [ ] T101 Import all handler functions from `cli.handlers` in main.py
- [ ] T102 Import `display_menu`, `get_menu_choice` from `cli.menu` in main.py
- [ ] T103 Import `signal` and `sys` modules for Ctrl+C handling
- [ ] T104 Define `main() -> None` function with docstring
- [ ] T105 In `main`: Print welcome message "Welcome to Todo Application - Phase I"
- [ ] T106 In `main`: Print info message "(In-Memory Only - Data will be lost on exit)"
- [ ] T107 In `main`: Create `service = TodoService()` instance
- [ ] T108 In `main`: Create infinite loop `while True:`
- [ ] T109 In loop: Call `display_menu()` to show options
- [ ] T110 In loop: Call `choice = get_menu_choice()` to get user input
- [ ] T111 In loop: If choice == -1 (invalid), continue to next iteration
- [ ] T112 In loop: If choice == 1, call `handle_add_task(service)`
- [ ] T113 In loop: If choice == 2, call `handle_view_tasks(service)`
- [ ] T114 In loop: If choice == 3, call `handle_update_task(service)`
- [ ] T115 In loop: If choice == 4, call `handle_delete_task(service)`
- [ ] T116 In loop: If choice == 5, call `handle_mark_complete(service)`
- [ ] T117 In loop: If choice == 6, print goodbye message and break loop
- [ ] T118 Add signal handler for Ctrl+C: define `signal_handler(sig, frame)` printing goodbye and calling `sys.exit(0)`
- [ ] T119 Register signal handler: `signal.signal(signal.SIGINT, signal_handler)`
- [ ] T120 Add `if __name__ == "__main__": main()` guard at end of file
- [ ] T121 Add comprehensive docstring to main() explaining application flow

**Checkpoint**: Application runs continuously, handles all menu options, exits cleanly on option 6 or Ctrl+C

---

## Phase 8: Input Validation Refinement

**Purpose**: Strengthen error handling for all user inputs

- [ ] T122 Review `handle_add_task`: Ensure description trimming happens before service call
- [ ] T123 Review `handle_update_task`: Ensure new description trimming happens before service call
- [ ] T124 Add helper function `get_positive_int(prompt: str) -> int | None` in handlers.py for index input
- [ ] T125 In `get_positive_int`: Use try/except to convert input to int
- [ ] T126 In `get_positive_int`: Return None if ValueError or if number <= 0
- [ ] T127 Refactor `handle_update_task` to use `get_positive_int` helper
- [ ] T128 Refactor `handle_delete_task` to use `get_positive_int` helper
- [ ] T129 Refactor `handle_mark_complete` to use `get_positive_int` helper
- [ ] T130 Test empty list operations: Run app, try update/delete/complete without adding tasks, verify error messages
- [ ] T131 Test boundary cases: Add 2 tasks, try index 0, verify error message
- [ ] T132 Test boundary cases: Add 2 tasks, try index 99, verify error message
- [ ] T133 Test rapid sequential operations: Add 5 tasks, delete 3, add 2 more, view tasks, verify correct state
- [ ] T134 Test whitespace-only description: Try adding task with "   ", verify error
- [ ] T135 Test long description: Try adding 501-character description, verify error with character count
- [ ] T136 Test non-numeric input: Try update with "abc" as index, verify error message

**Checkpoint**: All edge cases from spec.md handled gracefully, no crashes

---

## Phase 9: Code Quality Review

**Purpose**: Ensure PEP 8 compliance and code cleanliness

- [ ] T137 Add module docstring to `task.py` explaining Task entity (if not already present)
- [ ] T138 Add module docstring to `todo_service.py` explaining service layer (if not already present)
- [ ] T139 Add module docstring to `menu.py` explaining menu functions (if not already present)
- [ ] T140 Add module docstring to `handlers.py` explaining CLI handlers (if not already present)
- [ ] T141 Add module docstring to `main.py` explaining application entry point (if not already present)
- [ ] T142 Review Task class: Ensure all public methods have docstrings with Args/Returns/Raises sections
- [ ] T143 Review TodoService class: Ensure all public methods have docstrings with Args/Returns/Raises sections
- [ ] T144 Review all handler functions: Ensure docstrings explain purpose and parameters
- [ ] T145 Review all files: Ensure type hints on all function signatures
- [ ] T146 Review all files: Check for unused imports, remove if found
- [ ] T147 Review all files: Check for dead code or commented-out code, remove if found
- [ ] T148 Review variable names: Ensure descriptive names (e.g., `task_count` not `tc`)
- [ ] T149 Ensure consistent error message formatting across all handlers (start with "✗ Error: ")
- [ ] T150 Ensure consistent success message formatting across all handlers (start with "✓ ")
- [ ] T151 Optional: Run `python -m py_compile` on all .py files to check syntax
- [ ] T152 Optional: If ruff available, run `ruff check phase-1-cli/src/` for PEP 8 compliance

**Checkpoint**: Code is clean, well-documented, and follows PEP 8 standards

---

## Phase 10: Documentation & Testing Preparation

**Purpose**: Create documentation and prepare for acceptance testing

- [ ] T153 Create `phase-1-cli/README.md` with sections: Title, Description, Features, Setup, Usage, Phase Evolution
- [ ] T154 In README: Add "Features" section listing 5 core operations (add, view, update, delete, complete)
- [ ] T155 In README: Add "Setup" section with UV installation and `uv run src/main.py` command
- [ ] T156 In README: Add "Usage" section with menu screenshot and brief operation guide
- [ ] T157 In README: Add "Phase Evolution" section noting this is Phase I (in-memory only), future phases add persistence/web/AI/K8s/cloud
- [ ] T158 In README: Add "Constraints" section noting Python 3.13+, no external deps, no persistence
- [ ] T159 Create `phase-1-cli/tests/acceptance_tests.md` with test case template
- [ ] T160 In acceptance_tests.md: Add header explaining manual testing procedure
- [ ] T161 In acceptance_tests.md: List all 23 acceptance scenarios from spec.md as test cases
- [ ] T162 For each test case: Include Given/When/Then, Steps, Expected Result, Actual Result (blank), Status (blank)
- [ ] T163 In acceptance_tests.md: Add "Edge Cases" section with 7 edge case tests from spec.md
- [ ] T164 In acceptance_tests.md: Add "No Persistence Verification" test: Add tasks → Exit → Restart → Verify empty

**Checkpoint**: Documentation complete, acceptance test template ready for execution

---

## Phase 11: Final Testing & Validation

**Purpose**: Execute acceptance tests and verify all requirements met

- [ ] T165 Launch application: `uv run phase-1-cli/src/main.py`, verify starts without errors
- [ ] T166 Test User Story 1 (P1): Execute 5 acceptance scenarios for "View and Add Tasks"
- [ ] T167 Test User Story 2 (P2): Execute 5 acceptance scenarios for "Mark Tasks Complete"
- [ ] T168 Test User Story 3 (P3): Execute 4 acceptance scenarios for "Update Task Descriptions"
- [ ] T169 Test User Story 4 (P4): Execute 5 acceptance scenarios for "Delete Tasks"
- [ ] T170 Test User Story 5 (P1): Execute 6 acceptance scenarios for "Navigate Application Menu"
- [ ] T171 Test Edge Case 1: Try complete/update/delete from empty list, verify error messages
- [ ] T172 Test Edge Case 2: Try index out of range (10 when only 3 tasks), verify error
- [ ] T173 Test Edge Case 3: Try non-numeric input for index, verify error
- [ ] T174 Test Edge Case 4: Try whitespace-only task description, verify error
- [ ] T175 Test Edge Case 5: Try 501-character description, verify error with count
- [ ] T176 Test Edge Case 6: Rapid operations (add 5, delete 3, add 2), verify correct state
- [ ] T177 Test Edge Case 7: Add 50+ tasks, verify view remains usable and responsive
- [ ] T178 Test No Persistence: Add 3 tasks → Exit app → Restart → View tasks → Verify empty list
- [ ] T179 Document all test results in acceptance_tests.md (Actual Result, Status: Pass/Fail)
- [ ] T180 If any tests fail: Document issue, fix bug, re-run test, update status
- [ ] T181 Verify all 23 acceptance scenarios have Status: Pass
- [ ] T182 Final verification: Code is PEP 8 compliant, all functions documented, no dead code

**Checkpoint**: All 23 acceptance scenarios pass, application meets all Phase I success criteria

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start here
- **Phase 2 (Data Model)**: Depends on Phase 1 (directory structure must exist)
- **Phase 3 (Service - Basic)**: Depends on Phase 2 (Task class must exist)
- **Phase 4 (Service - Modify)**: Depends on Phase 3 (TodoService foundation must exist)
- **Phase 5 (CLI - Menu)**: Depends on Phase 1 (directory structure), independent of service layer
- **Phase 6 (CLI - Handlers)**: Depends on Phases 4 and 5 (service complete, menu functions exist)
- **Phase 7 (Main Loop)**: Depends on Phases 4, 5, and 6 (all components ready)
- **Phase 8 (Validation)**: Depends on Phase 7 (application must run first)
- **Phase 9 (Code Quality)**: Depends on Phases 2-7 (all code written)
- **Phase 10 (Documentation)**: Can start after Phase 7 (app runnable)
- **Phase 11 (Testing)**: Depends on all previous phases (complete application)

### Parallel Opportunities

**Phase 1 - Setup** (can run in parallel):
- T002-T006: Directory creation
- T009-T012: `__init__.py` file creation

**Phase 2 - Data Model** (sequential within phase):
- Must complete T015-T022 before testing (T023-T025)

**Phase 3 - Service Basic** (sequential):
- Must implement methods before testing

**Phase 5 & Phase 2-4** (parallel phases):
- Phase 5 (CLI Menu) can be developed in parallel with Phases 2-4 (Data & Service layers)
- CLI Menu has no dependency on Task or TodoService

**Phase 9 - Code Quality** (can parallelize by file):
- Docstring review can be done per module independently

**Phase 11 - Testing** (can parallelize by user story):
- Different user stories can be tested in parallel if multiple testers available

### Critical Path

```
Phase 1 (Setup)
    ↓
Phase 2 (Data Model)
    ↓
Phase 3 (Service Basic)
    ↓
Phase 4 (Service Modify)
    ↓
Phase 6 (CLI Handlers) ← Phase 5 (CLI Menu) can run parallel with 2-4
    ↓
Phase 7 (Main Loop)
    ↓
Phase 8 (Validation Refinement)
    ↓
Phase 9 (Code Quality)
    ↓
Phase 10 (Documentation)
    ↓
Phase 11 (Final Testing)
```

---

## Implementation Strategy

### Recommended Approach

1. **Complete Setup First** (Phase 1): Establish foundation, verify UV works
2. **Build Bottom-Up** (Phases 2-4): Data model → Service layer → Test in REPL
3. **Add UI Layer** (Phases 5-6): Menu system → Handlers
4. **Integrate** (Phase 7): Connect all components in main loop
5. **Refine** (Phases 8-9): Strengthen validation, clean code
6. **Validate** (Phases 10-11): Document and test comprehensively

### Testing Milestones

- **After Phase 2**: Can create Task instances in Python REPL
- **After Phase 3**: Can add and view tasks in Python REPL
- **After Phase 4**: Can perform all CRUD operations in Python REPL
- **After Phase 7**: Can run full application and perform operations via CLI
- **After Phase 8**: Application handles all edge cases without crashing
- **After Phase 11**: Application passes all 23 acceptance scenarios

### Commit Strategy

Suggested commit points:
- After Phase 1: "Initialize Phase I project structure"
- After Phase 2: "Implement Task dataclass with validation"
- After Phase 4: "Complete TodoService CRUD operations"
- After Phase 7: "Implement main application loop and CLI"
- After Phase 9: "Code quality review and PEP 8 compliance"
- After Phase 11: "Phase I complete - all acceptance tests passing"

---

## Notes

- **Manual Testing**: Phase I uses manual testing only. Automated unit tests are Phase II scope.
- **REPL Testing**: Phases 2-4 suggest Python REPL testing for quick validation of service layer.
- **UV Environment**: All commands assume running from `phase-1-cli/` directory with UV managing environment.
- **No Persistence**: Reminder that data is lost on exit - this is by design for Phase I.
- **Error Messages**: Ensure all error messages are user-friendly and guide users to correct input.
- **Type Hints**: Use modern Python 3.13+ syntax (`list[Task]` not `List[Task]` where possible).
- **Idempotency**: `mark_complete` must be idempotent (can call multiple times without error).
- **Index Conversion**: Remember 1-based user indices must be converted to 0-based for list access.

---

## Total Tasks: 182

**By Phase**:
- Phase 1 (Setup): 14 tasks (T001-T014)
- Phase 2 (Data Model): 11 tasks (T015-T025)
- Phase 3 (Service Basic): 13 tasks (T026-T038)
- Phase 4 (Service Modify): 16 tasks (T039-T054)
- Phase 5 (CLI Menu): 13 tasks (T055-T067)
- Phase 6 (CLI Handlers): 31 tasks (T068-T098)
- Phase 7 (Main Loop): 23 tasks (T099-T121)
- Phase 8 (Validation): 15 tasks (T122-T136)
- Phase 9 (Code Quality): 16 tasks (T137-T152)
- Phase 10 (Documentation): 12 tasks (T153-T164)
- Phase 11 (Testing): 18 tasks (T165-T182)

**Estimated Effort**:
- Experienced developer: 4-6 hours (20-30 tasks/hour)
- Beginner developer: 8-12 hours (15-20 tasks/hour)

---

## Success Criteria

Phase I is complete when:
- [ ] All 182 tasks checked off
- [ ] All 23 acceptance scenarios pass (T181)
- [ ] Code is PEP 8 compliant (T152, T182)
- [ ] All functions have docstrings (T142-T144)
- [ ] Application runs without errors (T165)
- [ ] No persistence verification passes (T178)
- [ ] Documentation complete (README, acceptance_tests.md)
- [ ] Phase can be demonstrated independently per constitution

Ready to proceed with `/sp.implement` or manual implementation following this task list.
