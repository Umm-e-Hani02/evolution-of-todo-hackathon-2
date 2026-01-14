# Acceptance Tests: Phase I Todo Application

**Feature**: 001-cli-todo
**Date**: 2026-01-03
**Status**: Manual Testing
**Prerequisites**: Application must be runnable via `uv run src/main.py`

## Testing Procedure

This document contains manual test scenarios for validating the Phase I todo application against its specification. Execute each test scenario and record results.

### How to Test

1. Launch the application: `cd phase-1-cli && uv run src/main.py`
2. Follow the steps in each test case
3. Verify the expected result matches actual behavior
4. Record status (Pass/Fail) and any notes

---

## User Story 1: View and Add Tasks (Priority: P1)

### Test Case 1.1: View Empty Task List

**Given**: Application just launched
**When**: User selects option 2 (View Tasks)
**Then**: Message "No tasks yet. Add your first task!" is displayed

**Steps**:
1. Run application
2. Enter `2` at menu
3. Observe output

**Expected**: "No tasks yet" message
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 1.2: Add Task with Valid Description

**Given**: Application running
**When**: User adds task "Buy groceries"
**Then**: Task is added and confirmation shown

**Steps**:
1. Run application
2. Enter `1` at menu
3. Enter "Buy groceries" as description
4. Observe confirmation

**Expected**: "✓ Task added: Buy groceries"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 1.3: View Tasks Shows All Tasks

**Given**: 2 tasks exist
**When**: User views tasks
**Then**: Both tasks displayed with indices and status

**Steps**:
1. Add task "Buy groceries"
2. Add task "Write report"
3. Enter `2` to view tasks
4. Verify both tasks shown with numbers 1 and 2

**Expected**:
```
1. [ ] Buy groceries
2. [ ] Write report
Total: 2 tasks (0 completed, 2 pending)
```
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 1.4: Reject Empty Task Description

**Given**: Application running
**When**: User attempts to add empty description
**Then**: Error message displayed

**Steps**:
1. Enter `1` to add task
2. Press Enter without typing anything
3. Observe error message

**Expected**: "✗ Error: Task description cannot be empty"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 1.5: Sequential Task Addition

**Given**: Application running
**When**: User adds 3 tasks in sequence
**Then**: Each receives unique index starting from 1

**Steps**:
1. Add task "Task 1"
2. Add task "Task 2"
3. Add task "Task 3"
4. View tasks
5. Verify indices are 1, 2, 3

**Expected**: Tasks numbered 1, 2, 3
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## User Story 2: Mark Tasks Complete (Priority: P2)

### Test Case 2.1: Mark Task Complete

**Given**: Task exists at index 1
**When**: User marks it complete
**Then**: Status changes to [✓]

**Steps**:
1. Add task "Buy milk"
2. Enter `5` to mark complete
3. Enter `1` for task number
4. View tasks (option 2)
5. Verify [✓] marker

**Expected**: "1. [✓] Buy milk"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 2.2: Mark Complete is Idempotent

**Given**: Task already complete
**When**: User marks it complete again
**Then**: No error, still complete

**Steps**:
1. Add and complete a task
2. Mark it complete again (option 5)
3. Verify no error message
4. View tasks, verify still [✓]

**Expected**: Success message, task remains [✓]
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 2.3: Invalid Index Error (Mark Complete)

**Given**: Only 2 tasks exist
**When**: User enters index 99
**Then**: Clear error message

**Steps**:
1. Add 2 tasks
2. Enter `5` to mark complete
3. Enter `99` for task number
4. Observe error

**Expected**: Error with valid range (1-2)
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 2.4: Non-Numeric Input Error

**Given**: Tasks exist
**When**: User enters "abc" for task number
**Then**: Error message displayed

**Steps**:
1. Add a task
2. Enter `5` to mark complete
3. Enter "abc" when prompted
4. Observe error

**Expected**: "✗ Error: Please enter a valid number"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 2.5: View Shows Completion Status

**Given**: Mixed complete/incomplete tasks
**When**: User views tasks
**Then**: Each shows correct status

**Steps**:
1. Add 3 tasks
2. Mark task 2 complete
3. View tasks
4. Verify task 2 has [✓], others have [ ]

**Expected**: Clear visual distinction
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## User Story 3: Update Task Descriptions (Priority: P3)

### Test Case 3.1: Update Task Description

**Given**: Task "Buy milk" exists at index 1
**When**: User updates to "Buy whole milk"
**Then**: Description changes

**Steps**:
1. Add task "Buy milk"
2. Enter `3` to update
3. Enter `1` for task number
4. Enter "Buy whole milk"
5. View tasks, verify change

**Expected**: Description changed, ID unchanged
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 3.2: Update with Invalid Index

**Given**: 2 tasks exist
**When**: User tries to update index 99
**Then**: Error message

**Steps**:
1. Add 2 tasks
2. Enter `3` to update
3. Enter `99`
4. Observe error

**Expected**: Error with valid range
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 3.3: Update Rejects Empty Description

**Given**: Task exists
**When**: User updates with empty string
**Then**: Error message

**Steps**:
1. Add task
2. Enter `3` to update
3. Enter `1` for task number
4. Press Enter (empty)
5. Observe error

**Expected**: "✗ Error: Task description cannot be empty"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 3.4: Update Preserves Completion Status

**Given**: Completed task exists
**When**: User updates description
**Then**: Status remains [✓]

**Steps**:
1. Add and complete task
2. Update its description
3. View tasks
4. Verify still [✓]

**Expected**: Description changed, still complete
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## User Story 4: Delete Tasks (Priority: P4)

### Test Case 4.1: Delete Task

**Given**: Task exists at index 2
**When**: User deletes it
**Then**: Task removed, confirmation shown

**Steps**:
1. Add 3 tasks
2. Enter `4` to delete
3. Enter `2` for task number
4. Observe confirmation

**Expected**: "✓ Task deleted" message
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 4.2: Tasks Renumbered After Deletion

**Given**: 3 tasks exist
**When**: Middle task deleted
**Then**: Remaining tasks renumbered

**Steps**:
1. Add tasks "A", "B", "C"
2. Delete task 2 ("B")
3. View tasks
4. Verify "C" is now index 2

**Expected**: Tasks renumbered 1, 2
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 4.3: Delete Invalid Index

**Given**: 2 tasks exist
**When**: User tries to delete index 5
**Then**: Error message

**Steps**:
1. Add 2 tasks
2. Enter `4` to delete
3. Enter `5`
4. Observe error

**Expected**: Error with valid range
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 4.4: Delete Last Task Shows Empty

**Given**: Only 1 task exists
**When**: User deletes it
**Then**: List becomes empty

**Steps**:
1. Add 1 task
2. Delete it
3. View tasks
4. Verify "No tasks yet" message

**Expected**: Empty list message
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 4.5: Delete Non-Numeric Input

**Given**: Tasks exist
**When**: User enters "xyz" for index
**Then**: Error message

**Steps**:
1. Add task
2. Enter `4` to delete
3. Enter "xyz"
4. Observe error

**Expected**: "✗ Error: Please enter a valid number"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## User Story 5: Navigate Application Menu (Priority: P1)

### Test Case 5.1: Menu Displays All Options

**Given**: Application launched
**When**: Menu is displayed
**Then**: All 6 options shown

**Steps**:
1. Run application
2. Observe menu

**Expected**: Options 1-6 clearly labeled
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 5.2: Valid Menu Selection Works

**Given**: Menu displayed
**When**: User enters valid option (1-6)
**Then**: Corresponding action triggered

**Steps**:
1. Test each option 1-5 individually
2. Verify correct handler called

**Expected**: Each option works correctly
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 5.3: Invalid Menu Option Rejected

**Given**: Menu displayed
**When**: User enters invalid number (7, 0, -1)
**Then**: Error and re-prompt

**Steps**:
1. Enter `7` at menu
2. Observe error
3. Verify menu redisplayed

**Expected**: Error message, menu redisplayed
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 5.4: Menu Redisplays After Action

**Given**: User completes an action
**When**: Action finishes
**Then**: Menu redisplayed

**Steps**:
1. Add a task (option 1)
2. Observe menu returns

**Expected**: Menu shown again
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 5.5: Exit Option Terminates

**Given**: Application running
**When**: User selects option 6
**Then**: Goodbye message and exit

**Steps**:
1. Enter `6` at menu
2. Observe goodbye message
3. Verify application terminates

**Expected**: Clean exit with goodbye
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Test Case 5.6: Ctrl+C Handled Gracefully

**Given**: Application running
**When**: User presses Ctrl+C
**Then**: Graceful shutdown

**Steps**:
1. Run application
2. Press Ctrl+C
3. Observe behavior

**Expected**: Goodbye message, no crash/traceback
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## Edge Cases

### Edge Case 1: Operations on Empty List

**Test**: Try update/delete/complete with no tasks

**Steps**:
1. Launch app (don't add tasks)
2. Try option 3 (update)
3. Try option 4 (delete)
4. Try option 5 (complete)

**Expected**: Clear error "No tasks available"
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Edge Case 2: Whitespace-Only Description

**Test**: Add task with only spaces

**Steps**:
1. Enter `1` to add task
2. Enter "     " (5 spaces)
3. Observe error

**Expected**: Error about empty description
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Edge Case 3: Very Long Description (501 chars)

**Test**: Add task exceeding 500 character limit

**Steps**:
1. Enter `1` to add task
2. Paste 501 character string
3. Observe error

**Expected**: Error with character count
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Edge Case 4: Rapid Sequential Operations

**Test**: Add 5, delete 3, add 2 more

**Steps**:
1. Add tasks 1-5
2. Delete tasks 2, 3, 4
3. Add tasks 6, 7
4. View tasks
5. Verify correct state (tasks 1, 5, 6, 7)

**Expected**: Correct renumbering and state
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

### Edge Case 5: High Volume (50+ Tasks)

**Test**: Add 50 tasks and verify usability

**Steps**:
1. Add 50 tasks
2. View tasks
3. Verify display remains readable
4. Perform update/delete/complete operations

**Expected**: No performance degradation, readable display
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## No Persistence Verification

### Test: Data Lost on Exit

**Steps**:
1. Add 3 tasks
2. Exit application (option 6)
3. Restart application
4. View tasks (option 2)

**Expected**: "No tasks yet" message (empty list)
**Actual**: _[Record result]_
**Status**: ⬜ Pass ⬜ Fail

---

## Test Summary

**Total Test Cases**: 25
**Passed**: _[Count]_
**Failed**: _[Count]_
**Not Tested**: _[Count]_

**Overall Status**: ⬜ All Passed ⬜ Some Failed

**Notes**:
- [Record any issues found]
- [Record any unexpected behavior]
- [Record suggestions for improvement]

**Tested By**: _[Name]_
**Date**: _[Date]_
**Application Version**: Phase I v0.1.0
