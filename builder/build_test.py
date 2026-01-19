#!/usr/bin/env python3
"""Minimal test - just capture Apple Intelligence output"""

import sys

sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    ask_apple_ai,
    set_variable,
    show_result_with_variable,
)


def build_test():
    actions = []

    # Simple AI query
    ai_action, _ = ask_apple_ai("Say hello world")
    actions.append(ai_action)
    actions.append(set_variable("response"))

    # Show it
    actions.append(show_result_with_variable("Response: ", "response", ""))

    return create_shortcut("AI Test", actions)


if __name__ == "__main__":
    shortcut = build_test()
    save_shortcut(shortcut, "/Users/athal/code/pencil-me-in/shortcuts/AI-Test.shortcut")
    print("Created AI-Test.shortcut")
