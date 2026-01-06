import gradio as gr
import json

from prompt_mappings import prompt_mappings

output_path = "output_annotations.jsonl"
OG_RULESET_FILE = "rulesets/prompt1.jsonl"
REVISED_RULESET_FILES = [
    "rulesets/prompt2.jsonl",
    "rulesets/prompt3.jsonl",
    "rulesets/prompt4.jsonl",
]
NUMBER_OF_RULESETS_TO_ANNOTATE = len(REVISED_RULESET_FILES)

PROMPT_KEYS = list(prompt_mappings.keys())
NUMBER_OF_PROMPTS = len(PROMPT_KEYS)
TOTAL_TASKS = NUMBER_OF_RULESETS_TO_ANNOTATE * NUMBER_OF_PROMPTS


def get_og_ruleset():
    return get_ruleset(OG_RULESET_FILE)


def get_task_indices(task_id: int):
    """
    Map a linear task_id to (ruleset_index, prompt_index).

    Traversal order is:
      - fix a prompt (prompt_index),
      - iterate over all rulesets (ruleset_index),
      - then move to the next prompt.
    """
    prompt_index = task_id // NUMBER_OF_RULESETS_TO_ANNOTATE
    ruleset_index = task_id % NUMBER_OF_RULESETS_TO_ANNOTATE
    return ruleset_index, prompt_index


def get_revised_ruleset(task_id: int):
    ruleset_index, _ = get_task_indices(task_id)
    return get_ruleset(REVISED_RULESET_FILES[ruleset_index])

def get_ruleset(jsonl_path):
    rules = []
    with open(jsonl_path) as jsonl_fp:
        for line in jsonl_fp:
            rule = json.loads(line)
            rules.append(f"* {rule['id']}: {rule['rule']}")
    return "\n\n".join(rules)

def build_annotation_welcome(prolific_id):
    return f"""## Welcome Participant {prolific_id}!
If you exit or refresh the screen, you will be taken back to the start. If this happens, please press **"Submit"** without annotating anything until you get back to where you left off.
"""

def build_annotation_task(task_id):
    _, prompt_index = get_task_indices(task_id)
    prompt_key = PROMPT_KEYS[prompt_index]
    prompt_meta = prompt_mappings[prompt_key]
    name = prompt_meta["name"]
    explanation = prompt_meta["explanation"]
    return f"""
### Task: {name}

{explanation}
"""

def build_annotation_instructions(task_id: int) -> str:
    _, prompt_index = get_task_indices(task_id)
    prompt_key = PROMPT_KEYS[prompt_index]
    prompt_meta = prompt_mappings[prompt_key]

    details = prompt_meta["details"]

    instructions_md = f""" # Instructions

{details}
"""

    return instructions_md


def submit_annotation(prolific_id, rules_listing, extra_feedback, task_id):
    ruleset_index, prompt_index = get_task_indices(task_id)
    prompt_key = PROMPT_KEYS[prompt_index]
    prompt_meta = prompt_mappings[prompt_key]

    data_to_save = {
        "prolific_id": prolific_id,
        "task_id": task_id,
        "ruleset_index": ruleset_index,
        "og_ruleset_filename": OG_RULESET_FILE,
        "revised_ruleset_filename": REVISED_RULESET_FILES[ruleset_index],
        "prompt_key": prompt_key,
        "rules_listing": rules_listing,
        "human_reasoning": extra_feedback
    }

    with open(output_path, "a") as output_fp:
        json.dump(data_to_save, output_fp)
        output_fp.write("\n")
    output_fp.close()

    next_task_id = task_id + 1

    if next_task_id >= TOTAL_TASKS:
        # All ruleset/prompt combinations have been annotated
        end_screen = gr.Markdown(
            "# Thank you for your annotations!\nPlease feel free to exit this screen.",
            visible=True,
        )
        return gr.Column(visible=False), next_task_id, None, None, end_screen, gr.Markdown(visible=False)

    # Continue to next prompt (or next ruleset once prompts are exhausted)
    next_instructions = build_annotation_instructions(next_task_id)
    return gr.Column(), next_task_id, None, None, gr.Markdown(visible=False), next_instructions


def update_rules(task_id):
    return f"### Original Ruleset:\n\n{get_og_ruleset()}", f"### Revised Ruleset:\n\n{get_revised_ruleset(task_id)}"


def start_screen_submit(prolific_id, task_id):
    welcome_message = build_annotation_welcome(prolific_id)
    task_message = build_annotation_task(task_id)
    annotation_instructions = build_annotation_instructions(task_id)
    # start screen, annotation interface, instruction markdown
    return gr.Column(visible=False), gr.Column(visible=True), welcome_message, task_message, annotation_instructions


with gr.Blocks(theme=gr.themes.Ocean(text_size='lg')) as demo:
    # Home screen where users enter their Prolific ID
    with gr.Column(visible=True) as start_screen:
        gr.Markdown("## Task Introduction \n Our work develops methods for automatically revising rulesets used to train AI to reduce ambiguity. We want our new rulesets to be consistent with the intent of the original rulesets and ask humans to validate our approach by scoring our rulesets using the same guidelines we provide our models.\n\n You will be given an original ruleset, a revised ruleset, and instructions for how to evaluate the rulesets side-by-side.")

        prolific_id = gr.Textbox(label="Please Enter Your Prolific ID")
        start_screen_enter = gr.Button()

    # Annotation interface
    task_id = gr.State(0)
    with gr.Column(visible=False) as annotation_interface:
        welcome_message = gr.Markdown()
        gr.HTML("<hr>") 
        task_message = gr.Markdown()
        gr.HTML("<hr>") 
        with gr.Row() as instructions:
            annotation_instructions = gr.Markdown()
            og_rule = gr.Markdown()
            revised_rule = gr.Markdown()
        gr.HTML("<hr>") 

        rules_listing = gr.Textbox(interactive=True,label="Please list the rule numbers of any rules that fit the instruction criteria or type in keywords as the instructions see fit.")
        extra_feedback = gr.Textbox(interactive=True, label="Please, if possible, give a short explanation of your reasoning behind your annotation.")
        submission_button = gr.Button("Submit")
    end_screen = gr.Markdown(visible=False)

    # Interactive logic after all components have been defined
    start_screen_enter.click(
        start_screen_submit,
        [prolific_id, task_id],
        [start_screen, annotation_interface, welcome_message, task_message, annotation_instructions],
    ).then(
        update_rules,
        [task_id],
        [og_rule, revised_rule],
    )
    submission_button.click(
        submit_annotation,
        [prolific_id, rules_listing, extra_feedback, task_id],
        [annotation_interface, task_id, rules_listing, extra_feedback, end_screen, annotation_instructions],
    ).then(
        None,
        None,
        None,
        js="() => window.scrollTo({top: 0, behavior: 'smooth'})"
    )
    task_id.change(update_rules, [task_id], [og_rule, revised_rule])

demo.launch()