# Testing Documentation

## Overview
This project uses Python's built-in `unittest` framework to ensure correctness and reliability at multiple levels: unit tests, integration tests, system tests, and persistence tests.

## Test Files

### 1. test_unit_library.py
**Purpose:** Unit tests for individual library functions  
**Coverage:** Tests simple and medium complexity functions in `meal_finder_library.py`  
**Tests include:**
- Text normalization
- Budget checking
- Meal formatting
- Price calculations
- Diet filtering
- Rating operations

### 2. test_unit_classes.py
**Purpose:** Unit tests for class methods  
**Coverage:** Tests `Meal`, `Menu`, and `UserPreferences` classes  
**Tests include:**
- Object creation
- Property access
- Individual method functionality
- Data conversion (to_dict)

### 3. test_integration.py
**Purpose:** Integration tests verifying components work together  
**Coverage:** Tests interactions between Menu, Meal, UserPreferences, and library functions  
**Tests include:**
- Menu with multiple meals
- CSV import to Menu workflow
- Preference learning from menu history
- Filtering combined with ratings
- Recommendation generation with preferences
- Complete filtering pipelines

### 4. test_system.py
**Purpose:** System tests for complete end-to-end workflows  
**Coverage:** Tests realistic user scenarios from start to finish  
**Tests include:**
- New user finding and selecting meals
- Returning user getting personalized recommendations
- CSV import and analytics generation
- Budget-constrained searches
- Rating affecting recommendations
- Edge cases and empty states

### 5. test_persistence.py
**Purpose:** Data persistence tests (CRITICAL FOR PROJECT 4)  
**Coverage:** Tests save/load and import/export functionality  
**Tests include:**
- Menu save and load
- UserPreferences save and load
- Save/load round-trip verification
- Error handling (missing files, invalid JSON)
- CSV import
- Analytics export to JSON
- Complete session persistence

## Running Tests

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Test File
```bash
python -m unittest tests.test_unit_library
python -m unittest tests.test_integration
python -m unittest tests.test_system
python -m unittest tests.test_persistence
```

### Run Individual Test Class
```bash
python -m unittest tests.test_unit_library.TestSimpleFunctions
```

### Run with Verbose Output
```bash
python -m unittest discover tests -v
```

## Testing Strategy

### Unit Tests
Unit tests validate individual functions and methods work correctly in isolation. These tests ensure core logic is correct before testing component interactions.

**Example:** Testing that `normalize_text()` correctly strips whitespace and converts to lowercase.

### Integration Tests
Integration tests verify that multiple components work together correctly. These tests ensure data flows properly between functions and classes.

**Example:** Testing that filtering by diet and then by price produces the expected subset of meals.

### System Tests
System tests validate complete end-to-end workflows that simulate realistic user interactions. These tests ensure the entire system functions correctly for actual use cases.

**Example:** Testing a complete user journey from viewing meals, filtering by preferences, to making a selection.

### Persistence Tests
Persistence tests verify that data can be saved to files and loaded back correctly. These tests are critical for Project 4 requirements.

**Example:** Testing that a Menu saved to JSON can be loaded back with all meals and ratings intact.

## Test Coverage Summary

**Total Tests:** 40+ tests across 5 files

**Coverage by Component:**
- Library functions: 15+ tests
- Meal class: 5+ tests
- Menu class: 8+ tests
- UserPreferences class: 6+ tests
- Integration workflows: 10+ tests
- System workflows: 8+ tests
- Persistence operations: 10+ tests

**Coverage by Feature:**
- Meal creation and management
- Menu operations (add, filter, search)
- User preference learning
- Recommendation generation
- Budget constraints
- Rating systems
- CSV import
- Save/load to JSON
- Analytics export
- Error handling

## Expected Results

All tests should pass when run. If any tests fail, review the error messages to identify the issue.

**Sample output when all tests pass:**
```
...................................
----------------------------------------------------------------------
Ran 40 tests in 0.234s

OK
```

## Notes

- Test files are located in the `tests/` directory
- Test data files (if created) are cleaned up automatically
- All persistence tests use temporary directories that are deleted after tests
- Tests use Python's standard library only (no external dependencies)

## Project 4 Requirements Met

**Unit Tests:** Individual class and method verification  
**Integration Tests:** 5-8 tests verifying component interaction  
**System Tests:** 3-5 tests validating complete workflows  
**Persistence Testing:** Save/load and import/export verification  
**Error Handling Tests:** File I/O error handling coverage  
**Documentation:** Clear testing strategy explanation
