#!/usr/bin/env python3
"""Test shortcut to find the correct ChatGPT output name"""

import sys
sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    comment,
    ask_chatgpt,
    set_variable_from_action,
    show_result_with_variable,
    show_alert,
)

def build_test():
    actions = []
    
    actions.append(comment("Test ChatGPT output capture"))
    
    # Simple ChatGPT call
    chatgpt, chatgpt_uuid = ask_chatgpt("Say exactly: Hello World")
    actions.append(chatgpt)
    
    # Try capturing with different output names
    output_names = ["response", "Response", "result", "Result", "text", "Text", "answer", "Answer", "output", "Output", "message", "Message"]
    
    for name in output_names:
        actions.append(set_variable_from_action(f"test_{name}", chatgpt_uuid, name))
    
    # Show what we captured
    for name in output_names:
        actions.append(show_result_with_variable(f"{name}: [", f"test_{name}", "]"))
    
    return create_shortcut("Test ChatGPT Capture", actions)

if __name__ == "__main__":
    shortcut = build_test()
    output_path = "/Users/athal/code/pencil-me-in/shortcuts/Test-ChatGPT-Capture.shortcut"
    save_shortcut(shortcut, output_path)
    print(f"Created: {output_path}")
