#!/usr/bin/env python3
"""
Tests for shortcut generation

These tests validate:
1. Plist structure is valid
2. Required fields are present
3. Control flow (menus, ifs) is properly nested
4. Action parameters match expected schema
"""

import plistlib
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from shortcut_builder import (
    create_shortcut,
    comment,
    text,
    ask,
    set_variable,
    menu_start,
    menu_item,
    menu_end,
    if_has_value,
    otherwise,
    end_if,
    show_alert,
    show_result,
)


def validate_shortcut_structure(data: dict) -> list[str]:
    """Validate a shortcut dict has correct structure. Returns list of errors."""
    errors = []

    # Check required top-level keys
    required_keys = ["WFWorkflowActions", "WFWorkflowIcon"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")

    actions = data.get("WFWorkflowActions", [])
    if not actions:
        errors.append("No actions in shortcut")
        return errors

    menu_groups = {}
    if_groups = {}

    for i, action in enumerate(actions):
        action_id = action.get("WFWorkflowActionIdentifier", "MISSING")
        params = action.get("WFWorkflowActionParameters", {})

        if action_id == "MISSING":
            errors.append(f"Action {i}: Missing WFWorkflowActionIdentifier")
            continue

        # Validate conditional actions
        if action_id == "is.workflow.actions.conditional":
            group_id = params.get("GroupingIdentifier")
            mode = params.get("WFControlFlowMode")

            if group_id is None:
                errors.append(f"Action {i}: Conditional missing GroupingIdentifier")
            if mode is None:
                errors.append(f"Action {i}: Conditional missing WFControlFlowMode")

            if mode == 0:  # start
                if "WFInput" not in params:
                    errors.append(f"Action {i}: If-start missing WFInput")
                else:
                    wf_input = params["WFInput"]
                    # Must have Type field
                    if "Type" not in wf_input:
                        errors.append(f"Action {i}: WFInput missing Type field")
                    # If Type=Variable, must have Variable field
                    if (
                        wf_input.get("Type") == "Variable"
                        and "Variable" not in wf_input
                    ):
                        errors.append(
                            f"Action {i}: WFInput Type=Variable but missing Variable field"
                        )

                if "WFCondition" not in params:
                    errors.append(f"Action {i}: If-start missing WFCondition")

                if group_id:
                    if_groups[group_id] = {"start": i, "end": None}
            elif mode == 2:  # end
                if group_id and group_id in if_groups:
                    if_groups[group_id]["end"] = i

        # Validate menu actions
        if action_id == "is.workflow.actions.choosefrommenu":
            group_id = params.get("GroupingIdentifier")
            mode = params.get("WFControlFlowMode")

            if group_id is None:
                errors.append(f"Action {i}: Menu missing GroupingIdentifier")

            if mode == 0:  # start
                if "WFMenuItems" not in params:
                    errors.append(f"Action {i}: Menu start missing WFMenuItems")
                if group_id:
                    menu_groups[group_id] = {"start": i, "items": [], "end": None}
            elif mode == 1:  # item
                if "WFMenuItemTitle" not in params:
                    errors.append(f"Action {i}: Menu item missing WFMenuItemTitle")
                if group_id and group_id in menu_groups:
                    menu_groups[group_id]["items"].append(i)
            elif mode == 2:  # end
                if group_id and group_id in menu_groups:
                    menu_groups[group_id]["end"] = i

    # Check all control flow is closed
    for group_id, menu in menu_groups.items():
        if menu["end"] is None:
            errors.append(f"Menu not closed (started at action {menu['start']})")

    for group_id, if_block in if_groups.items():
        if if_block["end"] is None:
            errors.append(f"If not closed (started at action {if_block['start']})")

    return errors


def test_if_has_value_structure():
    """Test that if_has_value generates correct WFInput structure"""
    action, group_id = if_has_value("test_var")
    params = action["WFWorkflowActionParameters"]

    assert "WFInput" in params, "Missing WFInput"
    wf_input = params["WFInput"]

    assert wf_input.get("Type") == "Variable", (
        f"WFInput.Type should be 'Variable', got {wf_input.get('Type')}"
    )
    assert "Variable" in wf_input, "WFInput missing Variable field"

    var_ref = wf_input["Variable"]
    assert "Value" in var_ref, "Variable reference missing Value"
    assert var_ref["Value"].get("VariableName") == "test_var", "Wrong variable name"

    print("✓ if_has_value structure is correct")


def test_menu_structure():
    """Test that menu generates correct structure"""
    actions = []

    menu, group_id = menu_start(["Option 1", "Option 2"], prompt="Choose")
    actions.append(menu)
    actions.append(menu_item("Option 1", group_id))
    actions.append(show_result("Selected 1"))
    actions.append(menu_item("Option 2", group_id))
    actions.append(show_result("Selected 2"))
    actions.append(menu_end(group_id))

    shortcut = create_shortcut("Test Menu", actions)
    errors = validate_shortcut_structure(shortcut)

    assert not errors, f"Menu structure errors: {errors}"
    print("✓ Menu structure is correct")


def test_nested_control_flow():
    """Test nested menus and ifs"""
    actions = []

    # Outer menu
    outer_menu, outer_id = menu_start(["A", "B"])
    actions.append(outer_menu)

    actions.append(menu_item("A", outer_id))
    # Nested if inside menu
    if_action, if_id = if_has_value("some_var")
    actions.append(if_action)
    actions.append(show_alert("Has value", "Variable has a value"))
    actions.append(otherwise(if_id))
    actions.append(show_alert("No value", "Variable is empty"))
    actions.append(end_if(if_id))

    actions.append(menu_item("B", outer_id))
    actions.append(show_result("Selected B"))

    actions.append(menu_end(outer_id))

    shortcut = create_shortcut("Test Nested", actions)
    errors = validate_shortcut_structure(shortcut)

    assert not errors, f"Nested structure errors: {errors}"
    print("✓ Nested control flow is correct")


def test_generated_shortcuts():
    """Test the actual generated shortcut files"""
    shortcuts_dir = "/Users/athal/code/pencil-me-in/shortcuts"

    for name in ["Pencil-Me-In-Setup.shortcut", "Pencil-Me-In.shortcut"]:
        path = os.path.join(shortcuts_dir, name)
        if not os.path.exists(path):
            print(f"⚠ {name} not found, skipping")
            continue

        with open(path, "rb") as f:
            data = plistlib.load(f)

        errors = validate_shortcut_structure(data)
        if errors:
            print(f"✗ {name} has errors:")
            for e in errors:
                print(f"  - {e}")
            raise AssertionError(f"{name} validation failed")
        else:
            action_count = len(data.get("WFWorkflowActions", []))
            print(f"✓ {name} is valid ({action_count} actions)")


def test_shortcut_can_be_signed():
    """Test that shortcuts can be signed (validates Apple's parser accepts them)"""
    import tempfile

    shortcuts_dir = "/Users/athal/code/pencil-me-in/shortcuts"
    # Use full path to Apple's shortcuts CLI to avoid conflict with python shortcuts package
    shortcuts_cli = "/usr/bin/shortcuts"

    for name in ["Pencil-Me-In-Setup.shortcut", "Pencil-Me-In.shortcut"]:
        path = os.path.join(shortcuts_dir, name)
        if not os.path.exists(path):
            continue

        with tempfile.NamedTemporaryFile(suffix=".shortcut", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [
                    shortcuts_cli,
                    "sign",
                    "--mode",
                    "people-who-know-me",
                    "--input",
                    path,
                    "--output",
                    tmp_path,
                ],
                capture_output=True,
                text=True,
            )
            # The ERROR messages about attribute strings are warnings, not failures
            # Check if output file was created and is larger than input (has signature)
            if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > os.path.getsize(
                path
            ):
                print(f"✓ {name} can be signed")
            else:
                print(f"✗ {name} signing failed")
                print(f"  stdout: {result.stdout}")
                print(f"  stderr: {result.stderr}")
                raise AssertionError(f"{name} signing failed")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == "__main__":
    print("Running shortcut tests...\n")

    test_if_has_value_structure()
    test_menu_structure()
    test_nested_control_flow()
    test_generated_shortcuts()
    test_shortcut_can_be_signed()

    print("\n✅ All tests passed!")
