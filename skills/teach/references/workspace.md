# Teaching workspace

Use the user's chosen learning directory. Continue its existing conventions;
read only the mission, preferences, and records relevant to the current topic.

## Learning state

- `MISSION.md`: the learning goal, success criteria, and constraints. Use
  [MISSION-FORMAT.md](../MISSION-FORMAT.md) when creating or revising it. Ground
  it in the user's stated goal; ask only for missing details that matter.
- `learning-records/0001-slug.md`: demonstrated understanding, prior knowledge,
  corrected misconceptions, or changes in direction. Use
  [LEARNING-RECORD-FORMAT.md](../LEARNING-RECORD-FORMAT.md) when adding a record.
- `RESOURCES.md`: annotated sources worth reusing. Use
  [RESOURCES-FORMAT.md](../RESOURCES-FORMAT.md) when updating it. Include
  communities only when real-world feedback would help and the user wants it.
- `NOTES.md`: teaching preferences and useful working notes.
- `GLOSSARY.md`: shared terminology when needed, using
  [GLOSSARY-FORMAT.md](../GLOSSARY-FORMAT.md).

Update the mission when the user changes their goal. Ask before substituting a
new goal of your own. Record learning based on the user's answers or work, not
merely because a lesson was delivered.

## Lesson artifacts

For workspace lessons, the default output is `lessons/0001-slug.html`, using the
next available number. Keep each lesson focused, readable, and tied to the
mission. Include practice with feedback and useful source links. Link related
lessons or reference material when it helps navigation.

Reuse existing styles and components in `assets/`. Extract new shared components
when there is a concrete reuse need. Add compact, printable `reference/*.html`
cheat sheets when the content will be useful beyond the lesson.

Check that the produced lesson works, including its interactions and local
links, and provide the user with the file path. Learning can continue after the
artifact is complete; wait for evidence before recording mastery.
