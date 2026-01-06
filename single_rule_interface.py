import gradio as gr
import json

choices = ["PASS", "WARN", "FAIL"]
NUMBER_OF_RULES_TO_ANNOTATE = 10

output_path = "output_annotations.jsonl"

def get_og_rule_by_id(index):
    return get_rule_by_id("rulesets/prompt1.jsonl", index)

def get_revised_rule_by_id(index):
    return get_rule_by_id("rulesets/prompt2.jsonl", index)

def get_rule_by_id(jsonl_path, index):
    with open(jsonl_path) as jsonl_fp:
        for line in jsonl_fp:
            rule = json.loads(line)
            if str(index) in rule["id"]:
                return rule["rule"]

    jsonl_fp.close()         
    return ""

def submit_annotation(prolific_id, og_rule, revised_rule, severity_score, extra_feedback, rule_id):
    data_to_save = {
        "prolific_id": prolific_id,
        "rule_id": rule_id,
        "og_rule": og_rule,
        "revised_rule": revised_rule,
        "severity_score": severity_score,
        "extra_feedback": extra_feedback
    }

    with open(output_path, "a") as output_fp:
        json.dump(data_to_save, output_fp)
        output_fp.write('\n')
    output_fp.close()

    if rule_id == NUMBER_OF_RULES_TO_ANNOTATE - 1:
        return gr.Column(visible=False), rule_id + 1, None, None, gr.Markdown("# Thank you for your annotations!\nPlease feel free to exit this screen.", visible=True)
    return gr.Column(), rule_id + 1, None, None, None

def update_rules(rule_id):
    return f"### Original Rule:\n{get_og_rule_by_id(rule_id)}", f"### Revised Rule:\n{get_revised_rule_by_id(rule_id)}"

def start_screen_submit(prolific_id):
    annotation_instructions = f"""## Welcome Participant {prolific_id}! \n If you exit or refresh the screen, you will be taken back to the start. If this happens, please press \"Submit\" without annotating anything until you get back to where you left off.
                        \n ### Scope Shift Criteria\nDetermine which, if any, of these apply to the revised rule when compared to the original:
                        \n - ADDED_OBLIGATION: Introduces a new duty or prohibition not present in the original
                        \n - LOST_OBLIGATION: Removes a duty or prohibition that was in the original
                        \n - OMITTED_CASE: Covers a new situation the original did not address
                        \n - NEGATIVE_IMPLICATION: Removes an explicit example, implying it no longer applies
                        \n ### Severity Score \n After identifying which criteria apply, assign ONE overall severity score to each revised rule:
                         - PASS: No substantive scope shift detected (no criteria apply)
                         - WARN: Minor scope shift that is debatable, some might consider it compatible with the original (at least one but no more than two criteria apply in a mild manner)
                         - FAIL: Clear and significant scope shift that is incompatible with the original intent (multiple criteria apply or one applies severely)"""
    # start screen, annotation interface, instruction markdown
    return gr.Column(visible=False), gr.Column(visible=True), annotation_instructions


with gr.Blocks(theme=gr.themes.Ocean(text_size='lg')) as demo:
    # Home screen where users enter their Prolific ID
    with gr.Column(visible=True) as start_screen:
        gr.Markdown("## Task Introduction \n Our work develops methods for automatically revising rulesets used to train AI to reduce ambiguity. We want our new rulesets to be consistent with the intent of the original rulesets and ask humans to validate our approach by scoring our rulesets using the same guidelines we provide our models.\n\n You will be given an \"original\" rule with a \"revised\" rule. For the revised rule, you must \n* Identify which scope shift criteria apply (if any)\n* Assign an overall severity score.")

        prolific_id = gr.Textbox(label="Please Enter Your Prolific ID")
        start_screen_enter = gr.Button()

    # Annotation interface
    rule_id = gr.State(0)
    with gr.Column(visible=False) as annotation_interface:
        annotation_instructions = gr.Markdown()
        with gr.Row() as instructions:
            og_rule = gr.Markdown()
            revised_rule = gr.Markdown()

        severity_score = gr.Radio(choices, label="Please select which best corresponds to the changes in the rules.")
        extra_feedback = gr.Textbox(interactive=True, label="Any Additional Feedback? (Optional)")
        submission_button = gr.Button("Submit")
    end_screen = gr.Markdown(visible=False)

    # Interactive logic after all components have been defined
    start_screen_enter.click(start_screen_submit, [prolific_id], [start_screen, annotation_interface, annotation_instructions]).then(
        update_rules, [rule_id], [og_rule, revised_rule]
    )
    submission_button.click(submit_annotation, 
                            [prolific_id, og_rule, revised_rule, severity_score, extra_feedback, rule_id], 
                            [annotation_interface, rule_id, severity_score, extra_feedback, end_screen])
    rule_id.change(update_rules, [rule_id], [og_rule, revised_rule])

demo.launch()
