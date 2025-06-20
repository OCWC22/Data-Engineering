# Changelog: 2025-06-19 - Update READMEs with New Documentation Structure

**Task:** [[Docs]] Update project READMEs to reflect the centralized documentation structure and introduce the "Changelog as Code" philosophy.
**Status:** Done

### Files Updated:
- **UPDATED:** `README.md` - Revised the project structure overview, added a section on navigating the new `docs/` directory, and introduced the "Changelog as Code" concept.
- **UPDATED:** `neuralake/README.md` - Updated the repository structure section to point to the centralized `docs/` directory and corrected the link to the main architectural document.

### Description:
This update aligns the project's primary README files with the recently completed documentation refactoring. The project structure sections have been rewritten to accurately describe the new layout, where all documentation resides in a root-level `docs` folder. This change introduces the concept of **Changelog as Catalog**, a practice inspired by the "Code as Catalog" principle, to maintain a rich, version-controlled history of the project's evolution.

### Reasoning:
The previous READMEs contained outdated information about the project structure, specifically the location of documentation. As the project adopts a more mature, AI-native development model where context is paramount, it is critical that the entry-point documents provide a clear and accurate map for both human and AI developers. This change ensures that anyone or anything interacting with the repository can easily find the information they need.

### Key Decisions & Trade-offs:
- **Centralized Documentation:** The decision to move all documentation to a single `docs` directory was reaffirmed in the READMEs. This improves organization at the cost of removing component-specific docs from the `neuralake` directory.
- **"Changelog as Code":** Formalized this term to describe our approach to maintaining changelogs. This provides a memorable name for the practice and links it philosophically to the project's other core tenets.

### Future Work:
- Continuously ensure all documentation and diagrams in the READMEs stay synchronized with the evolving codebase and structure. 