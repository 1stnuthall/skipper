from config import *
from slack_sdk.models.blocks import InputBlock, TextObject, PlainTextInputElement

# Hello World Test Request
req_hello_world = dict(
    group = "test",
    title_popup = "Hello World!",
    title_home = ":azdo: Hello World!",
    devops_pipeline_id = 5,
    command = "hello",
    approval_needed = "false",
    enabled = "false",
    blocks = [
        InputBlock(
            block_id = "hello_world",
            label = TextObject(type="plain_text", text="Enter Text"),
            element = PlainTextInputElement(action_id="hello_world")
        )
    ]
)