# When Agents Duplicate Work

This repository contains the dataset and supporting scripts for our empirical study of duplicate pull requests in agentic software development.

## Dataset

`dataset.csv` contains **816 manually verified duplicate PR pairs**, involving **1,471 Agentic PRs** collected from AIDev-pop v5.

Each row represents one duplicate PR pair and includes:

- Basic information about the earlier and later PRs
- Submitter and coding-agent information
- The earliest evidence identifying the duplicate relationship
- The emergence context and classification rationale

## Code

The scripts in `code/` were used to identify candidate duplicate PR pairs from PR comments, reviews, and inline review comments. Candidate pairs were detected using three main rules:

1. A closure, supersession, or fix expression appears before a referenced PR number.
2. A PR number appears before an expression indicating duplication, supersession, or a fix.
3. The text explicitly contains “duplicate” followed by a PR number.

These rules were used only to identify candidate pairs. All duplicate relationships included in the final dataset were manually verified.

## Paper

**When Agents Duplicate Work: An Empirical Study of Duplicate Pull Requests in Agentic Software Development**

Citation information will be added after publication.

## License

See [LICENSE](LICENSE).
