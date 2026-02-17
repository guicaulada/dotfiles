# Quality Gates

Quality gates catch problems at different stages, from quick sanity checks to thorough release validation. Each gate adds confidence before moving forward.

## Vibe Check (During Development)

Quick validation that the change is on the right track:

- Core flow works end-to-end
- No console errors or obvious regressions
- UI states (loading, empty, error) feel correct
- The change does what was intended

## Objective Check (Before PR)

Rigorous validation with measurable criteria:

- Review your own diff thoroughly
- All tests pass (unit, integration, e2e as applicable)
- No regressions introduced in related functionality
- Linters and type checks pass without new warnings
- Edge cases are handled

## Release Ready (Before Merge)

Final validation that the change is safe to ship:

- Documentation updated if the change affects public APIs or user-facing behavior
- Consider rollback plan for risky changes
- Verify the change works in conditions matching production
- All review feedback addressed
