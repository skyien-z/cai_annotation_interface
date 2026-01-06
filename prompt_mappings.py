prompt_mappings = {
    "least_restrictive_means": {
        "name": "Least Restrictive Means",
        "explanation": "We want rulesets that reduce ambiguity by being more specific, but we don't want rules to become overly restrictive by adding hard-coded numbers, exact response phrases, or fixed requirements.",
        "details": """
* Skip any rules where the `id` field contains **Meta-Rule**.
* If a rule exists in one ruleset but not the other, skip it.
* Compare each rule in the **Revised Ruleset** to its corresponding rule in the **Original Ruleset** (match them by the `id` field).
* For each revised rule, determine if it has become **Overly Restrictive**.
* Respond with a list of each revised rule that is **Overly Restrictive** along with feedback on *why* you marked it as overly restrictive.

### Definition of **Overly Restrictive**

A revised rule is **Overly Restrictive** if it adds hard-coded requirements not obviously required by the original rule, such as:

- **Exact phrases or wording that must be used**  
  *(e.g., "start your response with 'that sounds great!'")*
- **Specific numbers or limits**  
  *(e.g., "use no more than 20 words")*
- **Required counts or thresholds**  
  *(e.g., "refuse to answer 50% of the time")*
"""
    },
    "arbitrary_and_capricious": {
        "name": "Abitrary and Capricious",
        "explanation": "This prompt identifies arbitrary and capricious revisions including: \n 1. Adding entirely new rules not present in the original \n 2. Deleting existing rules from the original",
        "details": """
* Skip any rules where the `id` field contains **Meta-Rule**.
* Identify two types of problematic changes:

    1. **New Rule**: A rule appears in the **Revised Ruleset** but not in the **Original Ruleset** (based on the `id` field).
    2. **Deleted Rule**: A rule appears in the **Original Ruleset** but not in the **Revised Ruleset** (based on the `id` field).
"""
    },
    "absurdity_check": {
        "name": "Absurdity Check",
        "explanation": "This prompt applies an absurdity doctrine to catch rules that are:\n1. Self-contradictory within the revised rule itself\n2. Contradictory when read together with the corresponding original rule",
        "details": """
* Skip any rules where the `id` field contains **Meta-Rule**.
* If a rule exists in one ruleset but not the other, skip it.
* Compare each rule in the **Revised Ruleset** to its corresponding rule in the **Original Ruleset** (match them by the `id` field).

For each revised rule, determine whether or not it is **Absurd** according to the definition below.
Respond with a list of each revised rule that is **Absurd** along with your reasoning for why you marked it as absurd.

### Definition of **Absurd**

A revised rule is **Absurd** if either of the following conditions are true:
1. A literal reading of the revised rule would give a clearly absurd or self-contradictory result.
2. An attempt to fulfill the requirements of the revised rule together with the original rule would give a clearly absurd or self-contradictory result.
"""
    },
    "logical_outgrowth_doctrine": {
        "name": "Logical Outgrowth Doctrine",
        "explanation": "Overall ruleset structures should not shift between ruleset iterations based on logical outgrowth doctrine. While we allow rule linkages, or rules that refer to other rules in their text body, a rule linkage should not preclude the application of a separate rule. Similarly, while we allow meta-rules, we want to make sure meta-rules are consistent with the ruleset that they describe.",
        "details": """
A **Meta Rule** is a rule where the `id` field of the rule contains the string `"Meta-Rule"`.

* Skip any rules where the `id` field contains `"Meta-Rule"`.
* If a rule exists in one ruleset but not the other, skip it.
* Compare each rule in the **Revised Ruleset** to its corresponding rule in the **Original Ruleset** (match them by the `id` field).
* For each revised rule (that is not a Meta Rule), determine whether it creates a **Restrictive Linkage** to another rule.
* For each revised rule (that is not a Meta Rule), determine whether it is **Inconsistent With Meta** with any meta-rule.

Respond with a list of each revised rule that has either a **Restrictive Linkage** or is **Inconsistent With Meta**, along with feedback on *why* you marked it as being such and the rule that’s linked or the meta-rule that it’s being inconsistent with.

---

### Definition of **Restrictive Linkage**

A revised rule has a **Restrictive Linkage** if it precludes the application of a separate rule, or if it states that another rule precludes its application.

### Definition of **Inconsistent With Meta**

A revised rule is **Inconsistent With Meta** if a literal reading of the revised rule is inconsistent with any meta-rule. (A revised rule will often be orthogonal to a meta-rule, in which case you should not raise this flag.)
"""
    },
    "scope_shift_criteria": {
        "name": "Scope Shift Criteria",
        "explanation": "This prompt applies the scope shift criteria to the revised rule when compared to the original.",
        "details": """### Scope Shift Criteria

Determine which, if any, of these apply to the revised rule when compared to the original:

- **ADDED_OBLIGATION**: Introduces a new duty or prohibition not present in the original  
- **LOST_OBLIGATION**: Removes a duty or prohibition that was in the original  
- **OMITTED_CASE**: Covers a new situation the original did not address  
- **NEGATIVE_IMPLICATION**: Removes an explicit example, implying it no longer applies  

---

### Severity Score

After identifying which criteria apply, assign **ONE** overall severity score to each revised rule:

- **PASS**: No substantive scope shift detected (no criteria apply)
- **WARN**: Minor scope shift that is debatable, some might consider it compatible with the original (at least one but no more than two criteria apply in a mild manner)
- **FAIL**: Clear and significant scope shift that is incompatible with the original intent (multiple criteria apply or one applies severely)
"""
    }
}