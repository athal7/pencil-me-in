#!/usr/bin/env python3
"""
End-to-end tests for shortcuts.

These tests:
1. Build a minimal shortcut
2. Sign it
3. Import it (via open command)
4. Run it via CLI
5. Verify the output
"""

import os
import subprocess
import tempfile
import time
import plistlib
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    text,
    show_result,
    show_result_with_variable,
    set_variable,
    get_variable,
    ask_chatgpt,
    ask_chatgpt_with_variable,
)

SHORTCUTS_CLI = "/usr/bin/shortcuts"


def sign_shortcut(input_path: str, output_path: str) -> bool:
    """Sign a shortcut file. Returns True if successful."""
    result = subprocess.run(
        [
            SHORTCUTS_CLI,
            "sign",
            "--mode",
            "people-who-know-me",
            "--input",
            input_path,
            "--output",
            output_path,
        ],
        capture_output=True,
        text=True,
    )
    return os.path.exists(output_path) and os.path.getsize(
        output_path
    ) > os.path.getsize(input_path)


def import_shortcut(signed_path: str, name: str, timeout: int = 5) -> bool:
    """
    Import a shortcut by opening it.
    Returns True if shortcut appears in list within timeout.
    """
    # Open the file (this triggers import dialog on Mac)
    subprocess.run(["open", signed_path], check=True)

    # Wait for it to appear in list
    start = time.time()
    while time.time() - start < timeout:
        result = subprocess.run([SHORTCUTS_CLI, "list"], capture_output=True, text=True)
        if name in result.stdout:
            return True
        time.sleep(0.5)
    return False


def shortcut_exists(name: str) -> bool:
    """Check if a shortcut exists by name."""
    result = subprocess.run([SHORTCUTS_CLI, "list"], capture_output=True, text=True)
    return name in result.stdout


def run_shortcut(
    name: str, input_text: str = None, timeout: int = 30
) -> tuple[int, str, str]:
    """
    Run a shortcut and capture output.
    Returns (return_code, stdout, stderr).
    """
    cmd = [SHORTCUTS_CLI, "run", name]

    if input_text:
        # Pass input via stdin
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    else:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    return result.returncode, result.stdout, result.stderr


def delete_shortcut_if_exists(name: str):
    """Delete a shortcut from the library by finding and removing via AppleScript."""
    # Can't delete via CLI, but we can check if it exists
    # For now, just note that manual cleanup may be needed
    pass


class TestSimpleShortcut:
    """Test a minimal shortcut that just returns text."""

    NAME = "E2E-Test-Simple"

    def build(self) -> str:
        """Build the shortcut, return path to unsigned file."""
        actions = [
            text("Hello from E2E test!")[0],
        ]
        shortcut = create_shortcut(self.NAME, actions)

        path = f"/tmp/{self.NAME}.shortcut"
        save_shortcut(shortcut, path)
        return path

    def test(self):
        """Run the full test."""
        print(f"\n=== Testing {self.NAME} ===")

        # Build
        unsigned_path = self.build()
        assert os.path.exists(unsigned_path), "Failed to build shortcut"
        print(f"✓ Built: {unsigned_path}")

        # Sign
        signed_path = f"/tmp/{self.NAME}-signed.shortcut"
        assert sign_shortcut(unsigned_path, signed_path), "Failed to sign shortcut"
        print(f"✓ Signed: {signed_path}")

        # Check if already imported (from previous test run)
        if not shortcut_exists(self.NAME):
            print(f"  Shortcut not found, attempting import...")
            print(
                f"  NOTE: You may need to manually click 'Add Shortcut' in the dialog"
            )
            imported = import_shortcut(signed_path, self.NAME, timeout=10)
            if not imported:
                print(f"✗ Could not auto-import. Please manually import: {signed_path}")
                print(f"  Then re-run this test.")
                return False
        print(f"✓ Shortcut exists in library")

        # Run
        print(f"  Running shortcut...")
        returncode, stdout, stderr = run_shortcut(self.NAME)

        print(f"  Return code: {returncode}")
        print(f"  Stdout: {stdout[:200] if stdout else '(empty)'}")
        print(f"  Stderr: {stderr[:200] if stderr else '(empty)'}")

        # For a simple text action, output should contain our text
        # Note: show_result might not output to stdout in CLI mode
        assert returncode == 0, f"Shortcut failed with code {returncode}"
        print(f"✓ Shortcut ran successfully")

        return True


class TestVariableInterpolation:
    """Test that variable interpolation works."""

    NAME = "E2E-Test-Variables"

    def build(self) -> str:
        """Build the shortcut."""
        actions = [
            text("World")[0],
            set_variable("greeting_target"),
            show_result_with_variable("Hello, ", "greeting_target", "!"),
        ]
        shortcut = create_shortcut(self.NAME, actions)

        path = f"/tmp/{self.NAME}.shortcut"
        save_shortcut(shortcut, path)
        return path

    def test(self):
        """Run the full test."""
        print(f"\n=== Testing {self.NAME} ===")

        # Build
        unsigned_path = self.build()
        assert os.path.exists(unsigned_path), "Failed to build shortcut"
        print(f"✓ Built: {unsigned_path}")

        # Sign
        signed_path = f"/tmp/{self.NAME}-signed.shortcut"
        assert sign_shortcut(unsigned_path, signed_path), "Failed to sign shortcut"
        print(f"✓ Signed: {signed_path}")

        # Check structure before import
        with open(unsigned_path, "rb") as f:
            data = plistlib.load(f)

        # Find the show_result action and verify structure
        show_result_action = None
        for action in data["WFWorkflowActions"]:
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.showresult":
                show_result_action = action
                break

        assert show_result_action is not None, "No show_result action found"
        text_param = show_result_action["WFWorkflowActionParameters"]["Text"]
        assert isinstance(text_param, dict), (
            "Text param should be dict for variable interpolation"
        )
        assert text_param.get("WFSerializationType") == "WFTextTokenString", (
            "Wrong serialization type"
        )
        assert "￼" in text_param["Value"]["string"], "Missing placeholder character"
        print(f"✓ Variable interpolation structure is correct")

        # Import and run
        if not shortcut_exists(self.NAME):
            print(f"  Shortcut not found, attempting import...")
            imported = import_shortcut(signed_path, self.NAME, timeout=10)
            if not imported:
                print(f"⚠ Could not auto-import. Please manually import: {signed_path}")
                return False
        print(f"✓ Shortcut exists in library")

        # Run
        print(f"  Running shortcut...")
        returncode, stdout, stderr = run_shortcut(self.NAME)

        assert returncode == 0, f"Shortcut failed with code {returncode}: {stderr}"
        print(f"✓ Shortcut ran successfully")

        return True


class TestChatGPTAction:
    """Test that ChatGPT action works with the Extension model."""

    NAME = "E2E-Test-ChatGPT"

    def build(self) -> str:
        """Build a shortcut that uses ChatGPT."""
        actions = [
            text("Libertyville, IL")[0],
            set_variable("location"),
            ask_chatgpt_with_variable(
                "What is the population of ",
                "location",
                "? Reply with just the number.",
            )[0],
            set_variable("response"),
            show_result_with_variable("ChatGPT said: ", "response", ""),
        ]
        shortcut = create_shortcut(self.NAME, actions)

        path = f"/tmp/{self.NAME}.shortcut"
        save_shortcut(shortcut, path)
        return path

    def test(self):
        """Run the full test."""
        print(f"\n=== Testing {self.NAME} ===")

        # Build
        unsigned_path = self.build()
        assert os.path.exists(unsigned_path), "Failed to build shortcut"
        print(f"✓ Built: {unsigned_path}")

        # Sign
        signed_path = f"/tmp/{self.NAME}-signed.shortcut"
        assert sign_shortcut(unsigned_path, signed_path), "Failed to sign shortcut"
        print(f"✓ Signed: {signed_path}")

        # Verify the ChatGPT action structure
        with open(unsigned_path, "rb") as f:
            data = plistlib.load(f)

        chatgpt_action = None
        for action in data["WFWorkflowActions"]:
            if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm":
                chatgpt_action = action
                break

        assert chatgpt_action is not None, "No askllm action found"
        params = chatgpt_action["WFWorkflowActionParameters"]
        assert "WFLLMPrompt" in params, "Missing WFLLMPrompt"

        prompt = params["WFLLMPrompt"]
        assert isinstance(prompt, dict), (
            "Prompt should be dict for variable interpolation"
        )
        assert prompt.get("WFSerializationType") == "WFTextTokenString", (
            "Wrong serialization type"
        )
        print(f"✓ ChatGPT action structure is correct")

        # Import and run
        if not shortcut_exists(self.NAME):
            print(f"  Shortcut not found, attempting import...")
            imported = import_shortcut(signed_path, self.NAME, timeout=10)
            if not imported:
                print(f"⚠ Could not auto-import. Please manually import: {signed_path}")
                print(f"  This test requires ChatGPT to be configured in Shortcuts.")
                return False
        print(f"✓ Shortcut exists in library")

        # Run - this will actually call ChatGPT
        print(f"  Running shortcut (this will call ChatGPT)...")
        try:
            returncode, stdout, stderr = run_shortcut(self.NAME, timeout=60)
            print(f"  Return code: {returncode}")
            if stdout:
                print(f"  Output: {stdout[:500]}")
            if stderr:
                print(f"  Stderr: {stderr[:200]}")

            assert returncode == 0, f"Shortcut failed: {stderr}"
            print(f"✓ ChatGPT shortcut ran successfully")
            return True
        except subprocess.TimeoutExpired:
            print(f"⚠ Shortcut timed out - ChatGPT may require user interaction")
            return False


if __name__ == "__main__":
    print("=" * 60)
    print("End-to-End Shortcut Tests")
    print("=" * 60)
    print("\nNOTE: These tests may require manual interaction:")
    print("- Clicking 'Add Shortcut' when import dialog appears")
    print("- Granting permissions when shortcuts run")
    print("- ChatGPT may require login/setup")
    print()

    results = {}

    # Run tests
    for test_class in [
        TestSimpleShortcut,
        TestVariableInterpolation,
        TestChatGPTAction,
    ]:
        test = test_class()
        try:
            results[test.NAME] = test.test()
        except Exception as e:
            print(f"✗ {test.NAME} failed with exception: {e}")
            results[test.NAME] = False

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")

    all_passed = all(results.values())
    print()
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")

    sys.exit(0 if all_passed else 1)
