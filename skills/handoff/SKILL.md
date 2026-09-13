---
name: handoff
description: Write a handoff document when the user wants another agent or session to continue the work.
---

Save a concise handoff in the operating system's temporary directory unless
the user specifies a destination. A fresh agent should be able to resume the
requested work without reconstructing the conversation.

Capture the current objective, user constraints and authorizations, completed
work, relevant validation results, unresolved blockers, and concrete next steps.
Distinguish verified facts from assumptions and proposed actions. Include the
workspace, branch, and uncommitted work when relevant to resuming safely.

Link existing plans, issues, commits, diffs, and other artifacts by path or URL
instead of copying their contents. Include any essential context that exists
only in this conversation. Suggest skills only when they would help the next
task, and omit credentials and unnecessary personal information.

Tailor the document to the user's stated next-session focus. Finish by giving
the user the saved file's path.
