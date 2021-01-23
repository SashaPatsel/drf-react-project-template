put this content in the PR Title above:

--> [{'merge into' branch}]{Description}

--> for example, if merging a new app release from an app branch into the STAGING-MASTER branch: "[STAGING-MASTER] Update version 1.0 to 1.1 for Habitat Planner"

## Summary

{User story: describes the scope of the code in this PR. Be as specific as possible.}

```
As a {role: developer, website admin, website visitor, API consumer, etc.},
In order to {describe desired action},
I would like {describe desired feature}.
```

For example:

```
As a developer,
In order to minimize bugs in the UI,
I would like to instantiate a testing framework on frontend.
```

### {Summary item}

- [ ] {change 1}
- [ ] {change 2}

{Additional summary item descriptions or narratives}

## Owners

- {Role}: {Name}, {github profile reference}

## Libraries / Dependencies / Frameworks Modified

- [ADD / REMOVE / UPDATE] {Lib name} : {Lib function} : {Reason for change}

## Challenges and Solutions

**{Category of development} (e.g. CSS, DB, etc.)**

- **Challenge**: ... **Solution**: ...

## User Interface

- {UI update description} {screenshot image}...

## References

- [{Reference link}]()

## Closing Comments

- {Comment}

## Checklist

**Before Merge**

- [ ] Verify merge-into branch in PR.
- [ ] Merge latest code from upstream remote branch to local branch, resolve conflicts.
- [ ] Confirm PR commit history is clean.
- [ ] Run app / pass checks in development environment.
- [ ] Run tests in development environment.
- [ ] Review code independently, then optionally ask for outside feedback, and refactor. Rerun and retest as necessary.
- [ ] Publish to upstream branch by merging this PR.

**After Merge**

- [ ] Pull merged-into upstream branch (e.g. STAGING and/or MASTER) to local matching branches.
- [ ] Delete temporary branches in Github and locally (e.g. for related feature or bug, not STAGING or MASTER branches).
- [ ] Run deployment flow (if releasing to platform STAGING or MASTER).
- [ ] Verify deployment and submit issues for unforeseen bugs.
- [ ] Update project board and leave comments.
