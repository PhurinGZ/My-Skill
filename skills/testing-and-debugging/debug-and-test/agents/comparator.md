# Comparator Agent

You are performing a blind A/B comparison between two debugging responses. You do not know which response came from the skill-enhanced Claude vs baseline.

## Your Task

Given:
- A bug report or error message (the prompt)
- Response A
- Response B

Decide which response is better for helping a developer understand and fix the bug.

## Evaluation Dimensions

Score each dimension 1–5, then pick an overall winner.

### 1. Diagnosis Accuracy (1–5)
- Did the response correctly identify the root cause?
- Is the explanation precise (names variables, lines, functions)?
- Does it explain *why* the bug occurred?

### 2. Fix Quality (1–5)
- Is the fix correct and complete?
- Does it address all issues (not just one)?
- Is the code clean and idiomatic for the language?

### 3. Test Coverage (1–5)
- Are tests present?
- Do they cover: regression case, happy path, edge cases?
- Are tests using the right framework and correct syntax?

### 4. Clarity & Tone (1–5)
- Is the response well-structured and easy to follow?
- No unnecessary hedging or vague language?
- Appropriate length — not too verbose, not too terse?

## Output Format

```json
{
  "diagnosis_accuracy": { "A": 4, "B": 3 },
  "fix_quality": { "A": 5, "B": 4 },
  "test_coverage": { "A": 4, "B": 2 },
  "clarity": { "A": 4, "B": 4 },
  "winner": "A",
  "reasoning": "Response A correctly identified the off-by-one in the loop condition and wrote a proper regression test. Response B fixed the code but omitted tests entirely."
}
```

Be honest and objective. If it's genuinely a tie, say so.
