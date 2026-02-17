# Testing

Tests protect against regressions, document expected behavior, and give confidence to refactor. They are a core part of the development workflow.

## When to Write Tests

- Write tests for every new feature or behavior
- Add tests when fixing bugs to prevent recurrence
- Update existing tests when changing behavior

## What to Test

- Test **behavior and outcomes**, not implementation details
- Focus on public interfaces and observable results
- Cover the happy path, edge cases, and error conditions
- Verify error messages and failure modes are correct

## How to Write Tests

- Keep tests readable — a test should clearly state what it verifies
- Use descriptive test names that explain the scenario and expectation
- Follow the Arrange-Act-Assert (or Given-When-Then) pattern
- Keep each test focused on one behavior
- Avoid test interdependence — each test runs independently

## Test Maintenance

- Treat test code with the same quality standards as production code
- Remove tests that no longer correspond to real behavior
- Prefer updating tests alongside code changes in the same commit

## Running Tests

- Run the full test suite before committing
- Fix failing tests before moving on to new work
- Investigate flaky tests rather than ignoring them
