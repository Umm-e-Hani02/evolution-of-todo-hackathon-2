# Implementation Plan: In-Memory Python Console Todo Application

**Branch**: `001-cli-todo` | **Date**: 2026-01-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo/spec.md`

## Summary

Build a console-based Todo application in Python that manages tasks entirely in memory for a single session. The application provides a menu-driven interface for five core CRUD operations: add, view, update, delete, and mark tasks complete. This is Phase I of the Evolution of Todo project, establishing the foundation for future phases that will add persistence, web interfaces, AI capabilities, and cloud deployment.

**Technical Approach**: Implement a layered architecture with clear separation between data models (Task entity), business logic (TodoService), and user interface (CLI handlers). Use Python 3.13+ with dataclasses for type-safe task representation and a simple list-based in-memory store. Follow PEP 8 standards and maintain clean code through iterative refactoring.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory list (no persistence - data lost on program exit)
**Testing**: Manual CLI acceptance testing per user story scenarios
**Target Platform**: Cross-platform console (Windows, macOS, Linux terminals)
**Project Type**: Single project (simple CLI application)
**Performance Goals**: Instant response for all operations, support 100+ tasks without degradation
**Constraints**: No external dependencies, no file I/O, no database, single-session only, PEP 8 compliant
**Scale/Scope**: Single-user, single-session, 5 core CRUD operations, educational/demonstration purpose

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase I: In-Memory Python Console Todo** - Constitution Requirements:

✅ **Scope Alignment**: Command-line Todo application with in-memory storage
- Add, list, complete, delete todos ✓
- Basic validation and error handling ✓
- Simple text-based interface ✓

✅ **Success Criteria Met**:
- All CRUD operations work correctly ✓
- Data persists during program execution (in-memory) ✓
- Clean, testable code structure ✓

✅ **Out of Scope Respected**:
- No persistence across sessions ✓
- No web interface ✓
- No AI features ✓

✅ **Progressive Complexity Principle**:
- Phase I focuses on: data structures, CLI interaction ✓
- No premature features from future phases ✓

✅ **Documentation-First**:
- spec.md complete ✓
- plan.md (this document) in progress ✓
- tasks.md will follow via `/sp.tasks` ✓

✅ **Code Quality Standards** (from constitution):
- PEP 8 compliant ✓
- Clear separation of concerns (models/services/cli) ✓
- No hardcoded secrets (N/A for Phase I) ✓
- Smallest viable change (no over-engineering) ✓

**Gate Status**: ✅ **PASS** - All constitution requirements met for Phase I

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo/
├── spec.md              # Feature requirements and user stories
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical research)
├── data-model.md        # Phase 1 output (Task entity definition)
├── quickstart.md        # Phase 1 output (how to run)
├── contracts/           # Phase 1 output (internal API contracts)
│   └── todo_service.md  # TodoService interface specification
└── checklists/
    └── requirements.md  # Specification quality validation
```

### Source Code (repository root)

```text
phase-1-cli/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Task dataclass definition
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py   # Business logic for CRUD operations
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── menu.py           # Menu display and input handling
│   │   └── handlers.py       # Command handlers for each operation
│   └── main.py               # Application entry point and main loop
├── tests/                    # Manual test scenarios (documented)
│   └── acceptance_tests.md   # Step-by-step testing procedures
├── .python-version           # Python version specification for UV
├── pyproject.toml            # UV project configuration
├── README.md                 # Phase I overview and setup
└── .gitignore                # Ignore __pycache__, *.pyc, etc.
```

**Structure Decision**: Selected **Option 1: Single project** because Phase I is a standalone console application without frontend/backend separation. The src/ directory uses a layered architecture (models, services, cli) to demonstrate clear separation of concerns as required by the Phase I constitution. This structure supports future evolution - Phase II can extend the services layer with persistence, Phase III can add AI handlers alongside CLI handlers, etc.

## Complexity Tracking

> No constitution violations - this section is not needed.

## Phase 0: Research & Design Decisions

### Research Questions Addressed

#### 1. Task Model: Dict vs Dataclass

**Decision**: Use Python `dataclass` for Task model

**Rationale**:
- **Type Safety**: Dataclasses provide type hints that help catch errors early
- **Immutability Options**: Can use `frozen=True` if needed for safety
- **Readability**: Clear attribute definitions vs dict key access
- **IDE Support**: Better autocomplete and refactoring support
- **Validation**: Can add `__post_init__` for custom validation
- **Standard Library**: Part of Python 3.7+ standard library (no external deps)

**Alternatives Considered**:
- **Dict**: Simpler but loses type safety and IDE support
- **NamedTuple**: Immutable but less flexible for future additions
- **Plain Class**: More verbose than dataclass with same benefits

**Example**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    description: str
    completed: bool = False
    id: int = 0  # Assigned by service layer
```

#### 2. Command Handling: Numeric Menu vs Text-Based Commands

**Decision**: Use numeric menu system

**Rationale**:
- **Specification Alignment**: Spec (FR-001) explicitly requires "menu-driven CLI interface with numbered options"
- **User-Friendly**: Easier for beginners (target audience per spec)
- **Less Error-Prone**: Single digit input vs parsing text commands
- **Clear Options**: Menu displays all available operations
- **Validation**: Simple range check (1-6) vs complex string parsing

**Alternatives Considered**:
- **Text Commands** (e.g., "add", "list", "complete"): More flexible but requires parsing, more error cases, not specified in requirements
- **Single-Letter Shortcuts** (e.g., "a", "l", "c"): Less discoverable, not self-documenting

**Menu Structure**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit

Enter your choice (1-6):
```

#### 3. State Management: Global List vs Manager Class

**Decision**: Use `TodoService` manager class with internal list

**Rationale**:
- **Encapsulation**: Hides implementation details (could switch from list to dict later)
- **Testability**: Can instantiate service in tests with known state
- **Validation Logic**: Centralized place for index validation and error handling
- **Single Responsibility**: Service manages tasks, CLI handles I/O
- **Future-Proof**: Easy to add persistence layer in Phase II

**Alternatives Considered**:
- **Global List**: Simpler but violates separation of concerns, harder to test, couples CLI to data structure
- **Singleton Service**: Unnecessary complexity for single-user application

**Service Interface**:
```python
class TodoService:
    def __init__(self):
        self._tasks: List[Task] = []

    def add_task(self, description: str) -> Task
    def get_all_tasks(self) -> List[Task]
    def update_task(self, index: int, description: str) -> Task
    def delete_task(self, index: int) -> None
    def mark_complete(self, index: int) -> Task
    def _validate_index(self, index: int) -> None
```

#### 4. Index Management: 0-Based vs 1-Based

**Decision**: Use 1-based indexing for user-facing display, 0-based internally

**Rationale**:
- **User Expectation**: Spec (FR-001, User Story 1) shows "unique index number starting from 1"
- **Non-Technical Users**: Target audience (beginner developers) expects lists starting at 1
- **Conversion Layer**: CLI converts 1-based user input to 0-based list access
- **Clear Separation**: User sees 1-based, code uses 0-based (Python standard)

**Implementation**:
```python
# User enters: 1
# CLI converts: user_input - 1 = 0
# Service validates: 0 <= index < len(self._tasks)
# Display converts: index + 1 for output
```

#### 5. Error Handling Strategy

**Decision**: Use validation with descriptive error messages, no exceptions for user input errors

**Rationale**:
- **Spec Requirement**: FR-013 requires "specific error messages explaining what went wrong and how to correct it"
- **User Experience**: Exceptions crash the app; validation keeps the loop running
- **Graceful Degradation**: Invalid input shows error and re-prompts
- **Clear Guidance**: Error messages include valid range information

**Error Handling Patterns**:
- **Empty Description**: "Error: Task description cannot be empty. Please enter a valid description."
- **Invalid Index**: "Error: Invalid task number. Please enter a number between 1 and {count}."
- **Non-Numeric Input**: "Error: Please enter a valid number."
- **Empty List Operation**: "Error: No tasks available. Add a task first."

#### 6. Input Validation and Sanitization

**Decision**: Strip whitespace, enforce max length, validate non-empty

**Rationale**:
- **Spec Requirements**: FR-008 (reject empty/whitespace-only), FR-017 (max 500 chars), FR-018 (trim whitespace)
- **Data Integrity**: Consistent storage format
- **User Convenience**: Auto-trim is user-friendly (accepts " task " as "task")

**Validation Rules**:
```python
def validate_description(desc: str) -> str:
    desc = desc.strip()
    if not desc:
        raise ValueError("Description cannot be empty")
    if len(desc) > 500:
        raise ValueError("Description too long (max 500 characters)")
    return desc
```

#### 7. Completion Status Display

**Decision**: Use visual indicators [✓] for complete, [ ] for incomplete

**Rationale**:
- **Visual Clarity**: Symbols are instantly recognizable
- **Spec Alignment**: FR-003 requires "index number, description, and completion status"
- **Scanability**: Users can quickly identify completed tasks
- **Cross-Platform**: UTF-8 checkmark works on all modern terminals

**Display Format**:
```
1. [✓] Buy groceries
2. [ ] Call dentist
3. [✓] Finish report
```

### Architecture Decisions

**Layered Architecture**:
- **Models Layer** (`src/models/`): Data structures (Task dataclass)
- **Services Layer** (`src/services/`): Business logic, validation, state management
- **CLI Layer** (`src/cli/`): User interaction, input/output, menu display
- **Main** (`src/main.py`): Application bootstrap, main loop

**Data Flow**:
```
User Input → CLI Handler → Service Method → Data Validation → In-Memory Store
         ← CLI Display ← Service Response ← Success/Error ←
```

**Why This Architecture**:
- **Testability**: Each layer can be tested independently
- **Clarity**: Each module has single responsibility
- **Evolvability**: Phase II can add persistence layer below services without changing CLI
- **Maintainability**: Changes to UI don't affect business logic and vice versa

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete Task entity definition with fields, validation rules, and state transitions.

**Summary**:
- **Task Entity**: `id` (int), `description` (str, 1-500 chars), `completed` (bool)
- **Validation**: Non-empty description, whitespace-trimmed, length-capped
- **State Transitions**: Incomplete → Complete (idempotent)

### API Contracts

See [contracts/todo_service.md](./contracts/todo_service.md) for complete TodoService interface specification.

**TodoService Public Interface**:
- `add_task(description: str) -> Task` - Creates new task
- `get_all_tasks() -> List[Task]` - Returns all tasks
- `update_task(index: int, description: str) -> Task` - Updates task description
- `delete_task(index: int) -> None` - Removes task and renumbers
- `mark_complete(index: int) -> Task` - Marks task as complete

**Error Responses**:
- `ValueError`: Invalid description (empty, too long)
- `IndexError`: Invalid task index (out of range)

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup and usage instructions.

**Quick Setup**:
1. Install UV: `pip install uv`
2. Navigate to `phase-1-cli/`
3. Run: `uv run src/main.py`

## Implementation Phases

### Phase 2: Foundation (Setup)

**Goal**: Project structure and development environment

**Tasks**:
1. Create `phase-1-cli/` directory structure
2. Initialize UV project with `pyproject.toml`
3. Set Python version to 3.13+ in `.python-version`
4. Create empty module files (`__init__.py` in each package)
5. Create `.gitignore` for Python artifacts
6. Create `README.md` with project overview

**Acceptance**: Directory structure matches plan, UV can resolve environment

### Phase 3: Core Data Model

**Goal**: Task entity and basic validation

**Tasks**:
1. Create `src/models/task.py` with Task dataclass
2. Add fields: `id`, `description`, `completed`
3. Add `__post_init__` validation for description
4. Create `__str__` method for display formatting
5. Test task creation with valid and invalid data (manual REPL testing)

**Acceptance**: Can create Task instances, validation rejects empty descriptions

### Phase 4: Service Layer - Basic Operations

**Goal**: TodoService with add and view operations

**Tasks**:
1. Create `src/services/todo_service.py` with TodoService class
2. Implement `__init__` with empty task list
3. Implement `add_task(description)` with validation and ID assignment
4. Implement `get_all_tasks()` returning list copy
5. Test adding tasks and retrieving them (manual Python REPL)

**Acceptance**: Can add tasks and view them, IDs auto-increment from 1

### Phase 5: Service Layer - Modify Operations

**Goal**: Complete CRUD operations in service layer

**Tasks**:
1. Implement `_validate_index(index)` private helper method
2. Implement `update_task(index, description)` with validation
3. Implement `delete_task(index)` with renumbering
4. Implement `mark_complete(index)` with idempotency
5. Test all operations with edge cases (invalid indices, empty list)

**Acceptance**: All CRUD operations work, error handling robust

### Phase 6: CLI Layer - Menu System

**Goal**: Main menu display and input handling

**Tasks**:
1. Create `src/cli/menu.py` with `display_menu()` function
2. Create `get_menu_choice()` function with validation
3. Handle non-numeric input gracefully
4. Handle out-of-range choices (1-6 only)
5. Test menu display and choice validation

**Acceptance**: Menu displays correctly, validates input, re-prompts on error

### Phase 7: CLI Layer - Command Handlers

**Goal**: Handlers for each menu operation

**Tasks**:
1. Create `src/cli/handlers.py` with handler functions
2. Implement `handle_add_task(service)` - prompts for description, calls service
3. Implement `handle_view_tasks(service)` - displays all tasks with formatting
4. Implement `handle_update_task(service)` - prompts for index and new description
5. Implement `handle_delete_task(service)` - prompts for index, confirms deletion
6. Implement `handle_mark_complete(service)` - prompts for index
7. Add error display helpers for user-friendly messages

**Acceptance**: Each handler prompts correctly, calls service, displays results/errors

### Phase 8: Main Application Loop

**Goal**: Application entry point and main loop

**Tasks**:
1. Create `src/main.py` with `main()` function
2. Initialize TodoService instance
3. Implement main loop: display menu → get choice → dispatch to handler
4. Handle exit option (choice 6) gracefully
5. Add Ctrl+C signal handling for graceful shutdown
6. Add welcome message and goodbye message

**Acceptance**: App runs continuously, handles all menu options, exits cleanly

### Phase 9: Input Validation Refinement

**Goal**: Robust error handling for all user inputs

**Tasks**:
1. Review all input points (task description, index numbers, menu choices)
2. Add whitespace trimming to description inputs
3. Add length validation (500 char max) with clear error messages
4. Test empty list operations (update/delete/complete with no tasks)
5. Test boundary cases (index 0, index > count, negative numbers)
6. Test rapid sequential operations (add 5, delete 3, add 2)

**Acceptance**: All edge cases from spec handled gracefully, no crashes

### Phase 10: Code Quality Review

**Goal**: PEP 8 compliance and code cleanup

**Tasks**:
1. Run `ruff check` or `black` for formatting
2. Add docstrings to all public functions and classes
3. Add type hints to all function signatures
4. Remove any dead code or unused imports
5. Review variable names for clarity
6. Ensure consistent error message formatting
7. Add module-level docstrings

**Acceptance**: Code passes PEP 8 checks, all functions documented

### Phase 11: Documentation and Testing

**Goal**: Complete documentation and test procedures

**Tasks**:
1. Create `README.md` in `phase-1-cli/` with overview and setup
2. Create `tests/acceptance_tests.md` with step-by-step test scenarios
3. Execute all 23 acceptance scenarios from spec.md manually
4. Document test results and any issues found
5. Create quickstart.md with running instructions
6. Update this plan.md with final status

**Acceptance**: All 23 acceptance scenarios pass, documentation complete

## Development Workflow

**Iterative Approach**:
1. Implement one phase at a time in order (don't skip ahead)
2. Test each phase before moving to next (manual REPL or CLI testing)
3. Refactor as needed to maintain clean code
4. Document decisions and issues in PHRs

**Main Loop First Strategy**:
- Phase 8 establishes the application skeleton
- Phases 3-7 can be developed incrementally
- Each operation added and tested one at a time
- Menu and handlers glue everything together

**Continuous Refactoring**:
- After each phase, review for code smells
- Extract common patterns into helper functions
- Maintain separation of concerns
- Keep functions small and focused

## Testing Strategy

**Manual CLI Acceptance Testing**:
- Execute each user story's acceptance scenarios from spec.md
- Test happy paths first (normal operations)
- Then test error cases (invalid inputs)
- Then test edge cases (empty list, boundary indices)

**Test Flow**:
1. Launch application
2. Add 3 tasks with different descriptions
3. View tasks - verify all displayed with correct indices
4. Mark task #2 complete - verify status changes
5. Update task #1 description - verify change persists
6. Delete task #2 - verify renumbering (old #3 becomes new #2)
7. View tasks - verify state is correct
8. Test edge cases:
   - Try to update task #99 (invalid index)
   - Try to add empty description
   - Try to add 501-character description
   - Mark task complete twice (idempotency)
9. Exit application
10. Re-launch - verify no tasks persist (in-memory only)

**Edge Case Coverage** (from spec):
- ✅ Complete/update/delete from empty list
- ✅ Out-of-range index
- ✅ Non-numeric input for index
- ✅ Whitespace-only description
- ✅ Very long description (100+ chars)
- ✅ Rapid sequential operations
- ✅ High volume (50+ tasks)

**No Persistence Verification**:
- Add tasks → Exit → Restart → Verify list is empty
- Confirms in-memory-only requirement

## Risk Analysis

### Technical Risks

**Risk 1: Python Version Availability**
- **Mitigation**: UV handles Python version management, document fallback to 3.11+ if 3.13 unavailable

**Risk 2: Terminal Encoding Issues**
- **Mitigation**: Use UTF-8 encoding explicitly, fallback to ASCII checkmarks if needed

**Risk 3: Cross-Platform Differences**
- **Mitigation**: Test on Windows, macOS, Linux; use os-agnostic code

### Scope Risks

**Risk 4: Feature Creep**
- **Mitigation**: Strictly enforce Phase I constitution constraints, defer persistence/web/AI to future phases

**Risk 5: Over-Engineering**
- **Mitigation**: Use simplest solution that meets requirements, avoid premature optimization

## Next Steps

After Phase 1 (this plan) completes:

1. Run `/sp.tasks` to generate detailed task breakdown from this plan
2. Run `/sp.implement` to execute tasks with AI assistance
3. Create ADR if significant architectural decisions need documentation (e.g., "Why Dataclass over Dict for Task Model")
4. Create PHR for this planning session

**Estimated Effort**: 4-6 hours for experienced Python developer, 8-12 hours for beginner (target audience)

**Success Criteria**: All 23 acceptance scenarios from spec.md pass, code is PEP 8 compliant, application is demonstrable and independently runnable per Phase I constitution requirements.
