
import gradio as gr


task_instructions="""### Task Introduction
Our work develops methods for automatically revising rulesets used to train AI to reduce ambiguity. We want our new rulesets to be consistent with the intent of the original rulesets and ask humans to validate our approach by scoring our rulesets using the same guidelines we provide our models.
### Task Steps
For each task, you will be given a prompt and asked to list out the rule numbers that satisfy each prompt. Please provide any open-ended reasoning you have in the text box provided.
"""

prompt_and_ruleset="""### Prompt 1: "Least Restrictive Means" Check
Explanation: 
We want rulesets that reduce ambiguity by being more specific, but we don't want rules to become overly restrictive by adding hard-coded numbers, exact response phrases, or fixed requirements.

"""

choices = ["PASS", "WARN", "FAIL"]

with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    with gr.Row(visible=True) as instructions:
        markdown = gr.Markdown(task_instructions)
        # user_input = gr.Textbox(interactive=True)
        gr.Radio(choices, label="hi")
    
demo.launch()