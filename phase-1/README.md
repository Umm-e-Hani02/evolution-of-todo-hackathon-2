# Phase I: In-Memory Python Console Todo Application

A simple, console-based todo application that manages tasks in memory for the duration of a single session.

## Description

This is Phase I of the Evolution of Todo project, demonstrating the foundational implementation of a CLI-based task management system. The application provides five core CRUD operations through an intuitive numbered menu system.

## Features

- **Add Task**: Create new todo items with text descriptions
- **View Tasks**: Display all tasks with completion status and indices
- **Update Task**: Modify task descriptions
- **Delete Task**: Remove tasks from the list
- **Mark Complete**: Toggle task completion status

## Setup & Usage

See [quickstart.md](../specs/001-cli-todo/quickstart.md) in the specs directory for detailed setup instructions.

**Quick Start**:
```bash
cd phase-1-cli
uv run src/main.py
```

## Constraints

- **Python Version**: 3.13 or higher
- **Dependencies**: Python standard library only (no external packages)
- **Storage**: In-memory only - data is lost when application exits
- **Interface**: Console-based text interface
- **Users**: Single user, single session

## Phase Evolution

This is **Phase I** of a five-phase evolution demonstrating the progression from a simple CLI application to a distributed, cloud-native system:

- **Phase I** (Current): In-memory Python console Todo
- **Phase II** (Future): Full-stack web application with database persistence
- **Phase III** (Future): AI-powered conversational chatbot interface
- **Phase IV** (Future): Local Kubernetes deployment
- **Phase V** (Future): Cloud-native event-driven system on DigitalOcean

## Project Structure

```
phase-1-cli/
├── src/
│   ├── models/          # Task data model
│   ├── services/        # Business logic (TodoService)
│   ├── cli/             # Menu and command handlers
│   └── main.py          # Application entry point
├── tests/               # Manual acceptance test documentation
├── pyproject.toml       # UV project configuration
├── .python-version      # Python version specification
└── README.md            # This file
```

## Development

**Code Standards**: PEP 8 compliant, type-hinted, well-documented

**Architecture**: Layered design with clear separation of concerns
- Models layer: Task entity
- Services layer: TodoService (CRUD operations)
- CLI layer: Menu system and command handlers
- Main: Application loop and coordination

For detailed implementation documentation, see the `specs/001-cli-todo/` directory.
