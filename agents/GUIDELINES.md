Follow these guidance while implementing steps:
1. write extremely simple code, it should be "skimmable" and you should still be able to understand it
2. minimize possible states by reducing number of arguments, remove or narrow any state
3. use discriminated unions to reduce number of states the code can be in
4. exhaustively handle any objects with multiple different types, fail on unknown type 
5. don't write defensive code, assume the values are always what types tell you they are
6. use asserts when loading data, and always be highly opinionated about the parameters you pass around. don't let things be optional if not strictly required
7. remove any changes that are not strictly required
8. bias for fewer lines of code
9. no complex or clever code
10. don't break out into too many function, that's hard to read
11. early returns are great
12. use asserts instead of try catches or default values when you do expect something to exist
13. never pass overrides except strictly necessary, keep argument count low
14. don't make arguments optional if they are actually required

Commit guidance:
## 1. The "Golden Seven" Rules
These rules were popularized by Chris Beams and are widely considered the standard for professional development.

1.  **Separate subject from body with a blank line.**
2.  **Limit the subject line to 50 characters.** (Keep it concise).
3.  **Capitalize the subject line.**
4.  **Do not end the subject line with a period.**
5.  **Use the imperative mood in the subject line.** (e.g., "Fix bug" instead of "Fixed bug").
6.  **Wrap the body at 72 characters.** (This ensures readability in terminal-based tools).
7.  **Use the body to explain *what* and *why* vs. *how*.**

---

## 2. Use the Imperative Mood
A Git commit should be viewed as an **instruction** for changing the state of the repository. A good trick is to complete this sentence:

> "If applied, this commit will **[your subject line]**"

* **Correct:** Refactor subsystem X for readability
* **Incorrect:** Refactored subsystem X or Refactoring subsystem X

---

## 3. Structure with Conventional Commits
Many modern teams use the **Conventional Commits** specification. This adds a machine-readable prefix to your messages, which is great for automated changelog generation.

**Format:** <type>(<scope>): <description>

### Common Types:
* feat: A new feature for the user.
* fix: A bug fix.
* docs: Documentation only changes.
* style: Changes that do not affect the meaning of the code (white-space, formatting, etc.).
* refactor: A code change that neither fixes a bug nor adds a feature.
* test: Adding missing tests or correcting existing tests.
* chore: Changes to the build process or auxiliary tools and libraries.

**Example:**
feat(auth): add OAuth2 provider support

---

## 4. Focus on the "Why"
The code shows you **how** the change was made, but it often fails to explain **why** it was necessary. Use the body of the commit message to:
* Explain the context of the problem.
* Explain why this specific solution was chosen over others.
* Mention any side effects or breaking changes.

---

## 5. Summary Table: Good vs. Bad Examples

| Feature | Bad Example | Good Example |
| :--- | :--- | :--- |
| **Clarity** | Fixed stuff | fix: resolve race condition in login handler |
| **Mood** | I added more logs | feat: add debug logging to API middleware |
| **Length** | This is a very long subject line that explains every single file I touched today... | refactor: simplify database connection logic |
| **Context** | Update README | docs: update setup instructions for Docker |

---

##  The "Atomic" Commit 
Try to keep your commits **atomic**. This means one commit should address exactly one logical change. If you find yourself using the word "and" in your subject line (e.g., "Fix typo and add login feature"), you should probably split it into two separate commits.

## Check for Broken Commits
Sometimes there is a commit with broken commit messages that does not follow previous commit guidelines + raw characters like \n being visible, or -s not being enforced.
After making commit check immediately if there is no broken commit message.

# Misc guidance
When managing python environments, use uv for package management.
Use ty for typechecking, ruff for linting.
Also when needing to execute things bias towards `uv run`.