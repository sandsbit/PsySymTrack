# Contributing to PsySymTrack

Thank you for your interest in contributing to **PsySymTrack**.

PsySymTrack is an open-source psychiatric symptom tracking and analysis application. Contributions are welcome, provided they follow
the project's development, testing, documentation, and licensing requirements.

## Project Leadership

**Project Leader:** Nikita Serba

The project leader is responsible for the overall direction and maintenance of PsySymTrack and has final authority over accepting contributions
into the main repository.

For questions about contributing, development decisions, or the project in general, contact:

<nikitaserba@icloud.com>

---

## How to Contribute

All code contributions must be associated with a **GitHub issue**. An issue is mandatory for every bugfix or feature contribution.

You may contribute in one of two ways:

1. **Create a new issue** describing the bug, improvement, or feature you want to work on, if an appropriate issue does not already exist.
2. **Choose an existing issue** that you would like to address.

Before beginning substantial work on an issue, it is recommended to indicate in the issue that you intend to work on it. This helps prevent
multiple contributors from independently implementing the same change.

### Standard Contribution Workflow

1. **Create or select an issue.**
2. **Fork the repository.**
3. **Create a new branch** specifically for the bugfix or feature.
4. **Implement the change.**
5. **Add or update unit tests** for the affected functionality.
6. **Update documentation** where necessary.
7. **Run the complete test suite.**
8. **Review your changes** for correctness, readability, and adherence to these guidelines.
9. **Push your branch** to your fork.
10. **Open a Pull Request** against the main PsySymTrack repository.
11. Clearly describe what the Pull Request changes and reference the relevant issue.

A Pull Request should contain one coherent change whenever reasonably possible. Avoid combining unrelated bugfixes, refactoring, and features into a single Pull Request.

---

## Branches

Create a **new branch for every bugfix or feature**.

Do not develop directly on the `master` branch.

Use descriptive branch names, for example:

```text
bugfix/date-range-calculation
bugfix/macos-scrolling
feature/lithium-warning
feature/quality-of-life-scale
```

Keep branches focused on the issue they address.

---

## Testing

Testing is a mandatory part of contributing code to PsySymTrack.

### Unit Tests

PsySymTrack uses Python's **built-in `unittest` framework**.

Any new functionality must have appropriate unit tests placed in the `tests` directory.

When modifying existing functionality, update or add tests whenever the behavior or expected results change.

Tests should cover, where applicable:

* normal/expected behavior;
* boundary conditions;
* invalid input;
* exceptional conditions;
* regression cases for fixed bugs.

A bugfix should ideally include a test that would have failed before the fix and passes after the fix.

### Before Opening a Pull Request

**Run the complete unit test suite before opening a Pull Request.**

Do not submit a Pull Request while knowingly having failing tests.

---

## Python Style

### Type Hints

Use Python type hints for functions, methods, parameters, attributes, and return values where appropriate.

Prefer explicit types:

```python
def calculate_average(values: list[float]) -> float:
    ...
```

rather than leaving the interface ambiguous.

### String Quotation

Use **double quotation marks** for strings:

```python
message = "Symptom recorded"
```

rather than:

```python
message = 'Symptom recorded'
```

Use the project's existing conventions where a Python construct specifically requires otherwise.

### Documentation

Write **docstrings (Pydocs)** where they provide useful information, particularly for:

* public classes;
* public functions and methods;
* non-obvious behavior;
* complex algorithms;
* APIs intended for use by other parts of the application.

Do not add meaningless documentation that merely restates the code.

For example, this is not useful:

```python
def get_name(self) -> str:
    """Gets the name."""
```

Prefer documentation that explains behavior, constraints, or non-obvious semantics when those details matter.

---

## Copyright and License Headers

Every source file must contain the project's **copyright and license header at the top of the file**.

Use an existing PsySymTrack source file as the authoritative example for the exact header format.

Do not remove or alter existing copyright or license notices.

New files must receive the same appropriate copyright and license notice.

---

# Clean Code

PsySymTrack follows the principles of **Clean Code** described by Robert C. Martin ("Uncle Bob"), adapted to Python
and to the needs of this project. The principles below are based primarily on *Clean Code: A Handbook of Agile Software Craftsmanship*,
including its guidance on names, functions, comments, formatting, error handling, classes, and testing.

Clean code is not code that merely works. It should also be understandable, maintainable, testable, and appropriately structured.

## 1. Use Meaningful Names

Names should reveal intent.

Prefer:

```python
maximum_sleep_duration
```

over:

```python
x
```

Prefer:

```python
calculate_episode_duration()
```

over:

```python
calculate()
```

Avoid unexplained abbreviations and ambiguous names.

A longer, descriptive name is generally preferable to a short name whose meaning must be inferred.

---

## 2. Functions Should Do One Thing

A function should have one clear responsibility.

Avoid functions that simultaneously:

* validate data;
* calculate results;
* modify application state;
* update the GUI;
* save data; and
* display error messages.

Instead, separate those responsibilities into appropriately named functions.

For example:

```python
validate_measurement()
calculate_measurement_score()
save_measurement()
```

---

## 3. Keep One Level of Abstraction per Function

Do not mix high-level operations with low-level implementation details unnecessarily.

For example, a function responsible for recording a symptom should not also contain detailed database/file-format parsing logic.

Separate high-level application logic from implementation details.

---

## 4. Avoid Excessive Nesting

Deeply nested `if`, `for`, and `while` blocks make code difficult to understand.

Prefer early validation, guard clauses, and extraction into smaller functions where appropriate.


---

## 5. Keep Classes Focused

Classes should have a clear responsibility and a limited number of reasons to change.

Avoid "God classes" that contain unrelated responsibilities.

For example, a class responsible for representing a symptom measurement should not also be responsible for:

* rendering an entire GUI;
* reading configuration files;
* calculating unrelated statistics; and
* managing application notifications.

This follows the **Single Responsibility Principle (SRP)** discussed by Martin.

---

## 6. Avoid Duplication

Follow **DRY — Don't Repeat Yourself**.

If the same logic appears in multiple places, consider whether it should be extracted into a shared function, class, or utility.

For example, if several parts of the application independently implement the same date-range calculation, centralize that calculation rather
than maintaining multiple copies.

Do not, however, eliminate duplication merely by creating an abstraction that is harder to understand than the duplicated code. The abstraction
must improve maintainability.

---

## 7. Keep Code Readable

Formatting is part of communication.

Use:

* consistent indentation;
* sensible whitespace;
* logical grouping;
* readable line lengths;
* clear ordering of related code;
* descriptive names.

Avoid unnecessarily large source files and functions. Related concepts should generally remain close together.
---

## 8. Comments Should Explain What Code Cannot

Prefer expressive code over comments.

Bad:

```python
# Check whether the score is greater than the maximum
if score > maximum:
    ...
```

The code already communicates this.

A comment can be appropriate when explaining:

* a non-obvious algorithm;
* an important design decision;
* an external constraint;
* a surprising implementation detail;
* a warning about behavior that is not apparent from the code.

Do not leave commented-out code in the repository. Version control already preserves previous implementations.

Martin specifically recommends avoiding comments that compensate for unclear code and using comments primarily when they provide information that the code itself cannot express clearly.

---

## 9. Handle Errors Clearly

Error handling should not obscure the normal application logic.

Use appropriate Python exceptions rather than returning arbitrary error codes where exceptions are the natural mechanism.

Exceptions should provide useful context.

Avoid silently swallowing errors:

```python
try:
    do_something()
except Exception:
    pass
```

If an exception is intentionally ignored, there should be a clear and justified reason.

---

## 10. Keep Abstractions Appropriate

Do not introduce an abstraction merely because it is technically possible.

A new class, interface, helper function, or inheritance layer should solve a real design problem.

Prefer simple code when simple code is sufficient.

At the same time, do not allow clearly duplicated or tightly coupled logic to accumulate merely to avoid creating an appropriate abstraction.

---

## 11. Keep Related Code Together

Code that changes together or serves the same responsibility should generally be located together.

For example, tests for a module should be easy to locate in the `tests` directory, and functionality should be organized according to the existing project
structure rather than creating arbitrary new locations.

---

## 12. Write Testable Code

Design code so that important behavior can be tested independently.

Avoid unnecessary global state and excessive coupling to GUI components, files, system time, or other external resources when those
dependencies can reasonably be isolated.

Unit tests should test behavior rather than implementation details wherever practical.

---

## 13. Leave the Code Better Than You Found It

When modifying an existing area of the project, avoid making the surrounding code unnecessarily worse.

If a small, safe cleanup is directly related to your change, it may be appropriate to perform it.

Do not use an unrelated issue as an excuse for a large refactoring. Large refactorings should normally have their own issue and Pull Request.

---

# Pull Requests

Every Pull Request must:

* reference an existing GitHub issue;
* describe the problem being solved;
* describe the implemented solution;
* include appropriate tests;
* pass the complete test suite;
* follow the project's Python and Clean Code conventions;
* preserve copyright and license headers;
* avoid unrelated changes.

A useful Pull Request description should make it possible for a reviewer to understand **what changed, why it changed, and how it was tested**.

Pull Requests may be reviewed for correctness, maintainability, test coverage, API consistency, compatibility, and adherence to project standards.

The project leader may request changes before a Pull Request can be merged.

---

# Reviewing Your Own Changes

Before submitting a Pull Request, review the complete diff yourself.

Check for:

* accidental changes;
* debugging output;
* commented-out code;
* unused imports;
* unnecessary dependencies;
* missing type hints;
* missing tests;
* missing documentation;
* incorrect exception handling;
* inconsistent naming;
* missing copyright/license headers;
* unrelated modifications.

Also verify that the complete test suite passes.

---

# Adding Dependencies

Do not add a third-party dependency for functionality that can reasonably be implemented using Python's standard library or existing project dependencies.

When a new dependency is genuinely necessary, explain the reason in the relevant issue or Pull Request.

Consider:

* maintenance status;
* license compatibility;
* security;
* platform compatibility;
* project size;
* whether the dependency is actively maintained.

---

# Backward Compatibility

Be careful when changing existing public interfaces, data formats, configuration formats, or persisted application data.

If a breaking change is necessary, document it clearly in the relevant issue and Pull Request.

---

# Contributors

Contributors should add their name to the **Contributors** list at the end of `README.md`.


GitHub also maintains contribution information based on repository history, but PsySymTrack additionally maintains a human-readable contributor list in the README.

---

# Legal Notice

By contributing to PsySymTrack, you agree to the following:

> **When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.**

Do not submit code, documentation, images, data, or other material copied from another project or source unless you have the legal right to contribute that material under the project's license.

If your contribution incorporates third-party material, disclose its origin and applicable license in the Pull Request before it is merged.

---

# Questions

If you are unsure whether a proposed change is appropriate, have questions about the architecture, or need clarification before beginning work, contact the project leader:

**Nikita Serba**
<nikitaserba@icloud.com@

When possible, technical questions that are useful to other contributors should be discussed in the relevant GitHub issue so that the answer becomes part of the project's public development history.

---

Thank you for helping keep PsySymTrack maintainable, reliable, and useful.
