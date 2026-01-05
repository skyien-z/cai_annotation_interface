prompt_mappings = {
    "least_restrictive_means": {
        "explanation": "We want rulesets that reduce ambiguity by being more specific, but we don't want rules to become overly restrictive by adding hard-coded numbers, exact response phrases, or fixed requirements.",
        "details": """Skip any rules where the "id" field contains "Meta-Rule"
                    If a rule exists in one ruleset but not the other, skip it.
                    Compare each rule in the Revised Ruleset to its corresponding rule in the Original Ruleset (match them by the "id" field).
                    For each revised rule, determine if it has become OVERLY RESTRICTIVE.

                    Respond with a list of each revised rule that is OVERLY RESTRICTIVE along with feedback on *why* you marked it as overly restrictive.

                    # Definition of OVERLY RESTRICTIVE
                    A revised rule is OVERLY RESTRICTIVE if it adds hard-coded requirements not obviously required by the original rule like:
                    - Exact phrases or wording that must be used (e.g. "start your response with 'that sounds great!'")
                    - Specific numbers or limits (e.g. "use no more than 20 words")
                    - Required counts or thresholds (e.g. "refuse to answer 50% of the time")
                    """
    },
    "arbitrary_and_capricious": {
        "explanation": "This prompt identifies arbitrary and capricious revisions including: \n 1. Adding entirely new rules not present in the original \n 2. Deleting existing rules from the original",
        "details": """Skip any rules where the "id" field contains "Meta-Rule".
                    Identify two types of problematic changes:
                    1. NEW_RULE: A rule appears in the Revised Ruleset but not in the Original Ruleset (based on the "id" field)
                    2. DELETED_RULE: A rule appears in the Original Ruleset but not in the Revised Ruleset (based on the "id" field)
                    """
    },
    "absurdity_check": {
        "explanation": "This prompt applies an absurdity doctrine to catch rules that are:\n1. Self-contradictory within the revised rule itself\n2. Contradictory when read together with the corresponding original rule",
        "details": """Skip any rules where the "id" field contains "Meta-Rule".
                        If a rule exists in one ruleset but not the other, skip it.
                        Compare each rule in the Revised Ruleset to its corresponding rule in the Original Ruleset (match them by the "id" field).

                        For each revised rule, determine whether or not it is ABSURD according to the given definition.
                        Respond with a list of each revised rule that is ABSURD along with your reasoning for why you marked it as absurd.

                        # Definition of ABSURD
                        A revised rule is ABSURD if either of the following conditions are true:
                        1. A literal reading of the revised rule would give a clearly absurd or self-contradictory result
                        2. An attempt to fulfill the requirements of the revised rule together with the original rule would give a clearly absurd or self-contradictory result
                        """
    },
    "logical_outgrowth_doctrine": {
        "explanation": "Overall ruleset structures should not shift between ruleset iterations based on logical outgrowth doctrine. While we allow rule linkages, or rules that refer to other rules in their text body, a rule linkage should not preclude the application of a separate rule. Similarly, while we allow meta-rules, we want to make sure meta-rules are consistent with the ruleset that they describe.",
        "details": """A META_RULE is a rule where the "id" field of the rule contains the string "Meta-Rule"
                    Skip any rules where the "id" field contains "Meta-Rule".
                    If a rule exists in one ruleset but not the other, skip it.
                    Compare each rule in the Revised Ruleset to its corresponding rule in the Original Ruleset (match them by the "id" field).
                    For each revised rule, if it is not a META_RULE, determine whether it creates a RESTRICTIVE_LINKAGE to another rule.
                    For each revised rule, if it is not a META_RULE, determine whether it is INCONSISTENT_WITH_META with any meta-rule rule.

                    Respond with a list of each revised rule that has either a RESTRICTIVE_LINKAGE or is INCONSISTENT_WITH_META along with feedback on *why* you marked it as being such and the rule that’s linked or the meta-rule that it’s being inconsistent with.

                    # Definition of RESTRICTIVE_LINKAGE
                    A revised rule has a RESTRICTIVE_LINKAGE if it precludes the application of a separate rule, or if it states that another rule precludes its application.

                    # Definition of INCONSISTENT_WITH_META
                    A revised rule is INCONSISTENT_WITH_META if a literal reading of the revised rule is inconsistent with any meta-rule (a revised rule will often be orthogonal to a meta-rule, in which case you should not raise this flag)"""
    }
}