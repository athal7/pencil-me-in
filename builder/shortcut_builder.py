"""
Shortcut Builder - Generate Apple Shortcuts programmatically
"""

import plistlib
import uuid
from typing import Any


def new_uuid() -> str:
    """Generate a new UUID for action references"""
    return str(uuid.uuid4()).upper()


def create_shortcut(
    name: str,
    actions: list[dict],
    icon_color: int = 4282601983,
    icon_glyph: int = 59771,
) -> dict:
    """Create a shortcut plist structure"""
    return {
        "WFWorkflowClientVersion": "2605.0.5",
        "WFWorkflowClientRelease": "7.0",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowIcon": {
            "WFWorkflowIconStartColor": icon_color,
            "WFWorkflowIconGlyphNumber": icon_glyph,
        },
        "WFWorkflowImportQuestions": [],
        "WFWorkflowInputContentItemClasses": [
            "WFStringContentItem",
            "WFGenericFileContentItem",
        ],
        "WFWorkflowActions": actions,
        "WFWorkflowTypes": ["NCWidget", "WatchKit"],
    }


def save_shortcut(shortcut: dict, path: str):
    """Save shortcut to file"""
    with open(path, "wb") as f:
        plistlib.dump(shortcut, f, fmt=plistlib.FMT_BINARY)


# =============================================================================
# Action Builders
# =============================================================================


def comment(text: str) -> dict:
    """Add a comment (for organization)"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.comment",
        "WFWorkflowActionParameters": {
            "WFCommentActionText": text,
        },
    }


def text(content: str, output_name: str = None) -> tuple[dict, str]:
    """Create a text action. Returns (action, uuid) for variable references."""
    action_uuid = new_uuid()
    action = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
        "WFWorkflowActionParameters": {
            "WFTextActionText": content,
            "UUID": action_uuid,
        },
    }
    if output_name:
        action["WFWorkflowActionParameters"]["CustomOutputName"] = output_name
    return action, action_uuid


def ask(
    question: str, default: str = None, input_type: str = "Text"
) -> tuple[dict, str]:
    """Ask for input. Returns (action, uuid)."""
    action_uuid = new_uuid()
    params = {
        "WFAskActionPrompt": question,
        "UUID": action_uuid,
        "WFInputType": input_type,
    }
    if default:
        params["WFAskActionDefaultAnswer"] = default
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.ask",
        "WFWorkflowActionParameters": params,
    }, action_uuid


def set_variable(name: str, input_ref: str = None) -> dict:
    """Set a variable from input or previous action output"""
    params = {"WFVariableName": name}
    if input_ref:
        params["WFInput"] = variable_ref(input_ref)
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.setvariable",
        "WFWorkflowActionParameters": params,
    }


def get_variable(name: str) -> tuple[dict, str]:
    """Get a variable. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getvariable",
        "WFWorkflowActionParameters": {
            "WFVariable": {
                "Value": {"VariableName": name, "Type": "Variable"},
                "WFSerializationType": "WFTextTokenAttachment",
            },
            "UUID": action_uuid,
        },
    }, action_uuid


def show_alert(title: str, message: str, show_cancel: bool = False) -> dict:
    """Show an alert dialog"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.alert",
        "WFWorkflowActionParameters": {
            "WFAlertActionTitle": title,
            "WFAlertActionMessage": message,
            "WFAlertActionCancelButtonShown": show_cancel,
        },
    }


def show_result(text: str) -> dict:
    """Show result (output)"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.showresult",
        "WFWorkflowActionParameters": {
            "Text": text,
        },
    }


def notification(title: str, body: str) -> dict:
    """Show a notification"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.notification",
        "WFWorkflowActionParameters": {
            "WFNotificationActionTitle": title,
            "WFNotificationActionBody": body,
        },
    }


# =============================================================================
# Menu Actions
# =============================================================================


def menu_start(items: list[str], prompt: str = None) -> tuple[dict, str]:
    """Start a menu. Returns (action, group_id)."""
    group_id = new_uuid()
    params = {
        "GroupingIdentifier": group_id,
        "WFControlFlowMode": 0,  # Start
        "WFMenuItems": items,
    }
    if prompt:
        params["WFMenuPrompt"] = prompt
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
        "WFWorkflowActionParameters": params,
    }, group_id


def menu_item(title: str, group_id: str) -> dict:
    """Menu item case"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 1,  # Item
            "WFMenuItemTitle": title,
        },
    }


def menu_end(group_id: str) -> dict:
    """End menu"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 2,  # End
        },
    }


# =============================================================================
# Conditionals
# =============================================================================


def if_equals(value: str, compare_to: str) -> tuple[dict, str]:
    """If condition (equals). Returns (action, group_id)."""
    group_id = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 0,  # Start
            "WFCondition": 4,  # Equals
            "WFConditionalActionString": compare_to,
            "WFInput": {
                "Type": "Variable",
                "Variable": {
                    "Value": {"VariableName": value, "Type": "Variable"},
                    "WFSerializationType": "WFTextTokenAttachment",
                },
            },
        },
    }, group_id


def if_has_value(variable_name: str) -> tuple[dict, str]:
    """If has any value. Returns (action, group_id)."""
    group_id = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 0,
            "WFCondition": 100,  # Has any value
            "WFInput": {
                "Type": "Variable",
                "Variable": {
                    "Value": {"VariableName": variable_name, "Type": "Variable"},
                    "WFSerializationType": "WFTextTokenAttachment",
                },
            },
        },
    }, group_id


def otherwise(group_id: str) -> dict:
    """Else clause"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 1,  # Else
        },
    }


def end_if(group_id: str) -> dict:
    """End if"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 2,  # End
        },
    }


# =============================================================================
# Loops
# =============================================================================


def repeat_each_start(input_variable: str = None) -> tuple[dict, str]:
    """Start repeat with each loop. Returns (action, group_id)."""
    group_id = new_uuid()
    params = {
        "GroupingIdentifier": group_id,
        "WFControlFlowMode": 0,
    }
    if input_variable:
        params["WFInput"] = {
            "Value": {"VariableName": input_variable, "Type": "Variable"},
            "WFSerializationType": "WFTextTokenAttachment",
        }
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.each",
        "WFWorkflowActionParameters": params,
    }, group_id


def repeat_each_end(group_id: str) -> dict:
    """End repeat with each"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.repeat.each",
        "WFWorkflowActionParameters": {
            "GroupingIdentifier": group_id,
            "WFControlFlowMode": 2,
        },
    }


# =============================================================================
# Dictionary / JSON
# =============================================================================


def dictionary(items: dict[str, Any]) -> tuple[dict, str]:
    """Create a dictionary. Returns (action, uuid)."""
    action_uuid = new_uuid()
    # Convert items to WFDictionaryItems format
    wf_items = []
    for key, value in items.items():
        item = {
            "WFItemType": 0 if isinstance(value, str) else 1,  # 0=text, 1=number
            "WFKey": {"Value": key, "WFSerializationType": "WFTextTokenString"},
            "WFValue": {
                "Value": str(value),
                "WFSerializationType": "WFTextTokenString",
            },
        }
        wf_items.append(item)

    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.dictionary",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFItems": {
                "Value": wf_items,
                "WFSerializationType": "WFDictionaryFieldValue",
            },
        },
    }, action_uuid


def get_dictionary_value(key: str, input_uuid: str = None) -> tuple[dict, str]:
    """Get value from dictionary. Returns (action, uuid)."""
    action_uuid = new_uuid()
    params = {
        "UUID": action_uuid,
        "WFDictionaryKey": key,
    }
    if input_uuid:
        params["WFInput"] = action_output_ref(input_uuid, "Dictionary")
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getvalueforkey",
        "WFWorkflowActionParameters": params,
    }, action_uuid


def set_dictionary_value(key: str, value: str) -> dict:
    """Set value in dictionary"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.setvalueforkey",
        "WFWorkflowActionParameters": {
            "WFDictionaryKey": key,
            "WFDictionaryValue": value,
        },
    }


# =============================================================================
# Files
# =============================================================================


def get_file(path: str, error_if_not_found: bool = False) -> tuple[dict, str]:
    """Get file from iCloud/Shortcuts folder. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.documentpicker.open",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFGetFilePath": path,
            "WFFileErrorIfNotFound": error_if_not_found,
            "WFShowFilePicker": False,
        },
    }, action_uuid


def save_file(path: str, overwrite: bool = True) -> dict:
    """Save to file"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.documentpicker.save",
        "WFWorkflowActionParameters": {
            "WFFileDestinationPath": path,
            "WFSaveFileOverwrite": overwrite,
            "WFShowFilePicker": False,
        },
    }


# =============================================================================
# Web / Network
# =============================================================================


def get_url(url: str) -> tuple[dict, str]:
    """Download URL contents. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.downloadurl",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFURL": url,
        },
    }, action_uuid


def get_url_variable(variable_name: str) -> tuple[dict, str]:
    """Download URL from variable. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.downloadurl",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFURL": {
                "Value": {
                    "attachmentsByRange": {
                        "{0, 1}": {"Type": "Variable", "VariableName": variable_name}
                    },
                    "string": "￼",
                },
                "WFSerializationType": "WFTextTokenString",
            },
        },
    }, action_uuid


# =============================================================================
# AI / ChatGPT
# =============================================================================


def ask_chatgpt(prompt: str) -> tuple[dict, str]:
    """
    Ask ChatGPT (via Apple's built-in "Use Model" action).
    Uses the system default model.
    Returns (action, uuid).
    """
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.askllm",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFLLMPrompt": prompt,
        },
    }, action_uuid


def ask_chatgpt_with_input(
    prompt_template: str, input_variable: str
) -> tuple[dict, str]:
    """Ask ChatGPT with variable interpolation. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.askllm",
        "WFWorkflowActionParameters": {
            "UUID": action_uuid,
            "WFLLMPrompt": {
                "Value": {
                    "attachmentsByRange": {
                        "{0, 1}": {"Type": "Variable", "VariableName": input_variable}
                    },
                    "string": f"￼\n\n{prompt_template}",
                },
                "WFSerializationType": "WFTextTokenString",
            },
        },
    }, action_uuid


# =============================================================================
# Calendar
# =============================================================================


def get_upcoming_events(calendar: str = None, count: int = 50) -> tuple[dict, str]:
    """Get upcoming calendar events. Returns (action, uuid)."""
    action_uuid = new_uuid()
    params = {
        "UUID": action_uuid,
        "WFGetUpcomingItemCount": count,
    }
    if calendar:
        params["WFGetUpcomingItemCalendar"] = calendar
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getupcomingevents",
        "WFWorkflowActionParameters": params,
    }, action_uuid


def add_calendar_event(
    title: str,
    start_date: str = None,
    end_date: str = None,
    calendar: str = None,
    all_day: bool = False,
    notes: str = None,
) -> dict:
    """Add a new calendar event"""
    params = {"WFCalendarItemTitle": title}
    if calendar:
        params["WFCalendarDescriptor"] = calendar
    if start_date:
        params["WFCalendarItemStartDate"] = start_date
    if end_date:
        params["WFCalendarItemEndDate"] = end_date
    if all_day:
        params["WFCalendarItemAllDay"] = True
    if notes:
        params["WFCalendarItemNotes"] = notes
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.addnewevent",
        "WFWorkflowActionParameters": params,
    }


# =============================================================================
# Reminders
# =============================================================================


def add_reminder(
    title: str, remind_date: str = None, list_name: str = None, notes: str = None
) -> dict:
    """Add a new reminder"""
    params: dict[str, Any] = {"WFCalendarItemTitle": title}
    if list_name:
        params["WFCalendarDescriptor"] = list_name
    if remind_date:
        params["WFAlertEnabled"] = True
        params["WFAlertCustomTime"] = remind_date
    if notes:
        params["WFCalendarItemNotes"] = notes
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.addnewreminder",
        "WFWorkflowActionParameters": params,
    }


# =============================================================================
# Utility / References
# =============================================================================


def variable_ref(name: str) -> dict:
    """Create a variable reference for use in parameters"""
    return {
        "Value": {"VariableName": name, "Type": "Variable"},
        "WFSerializationType": "WFTextTokenAttachment",
    }


def action_output_ref(output_uuid: str, output_name: str) -> dict:
    """Create a reference to a previous action's output"""
    return {
        "Value": {
            "OutputName": output_name,
            "OutputUUID": output_uuid,
            "Type": "ActionOutput",
        },
        "WFSerializationType": "WFTextTokenAttachment",
    }


def run_shortcut(name: str, show_while_running: bool = False) -> dict:
    """Run another shortcut"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.runworkflow",
        "WFWorkflowActionParameters": {
            "WFWorkflowName": name,
            "WFShowWorkflow": show_while_running,
        },
    }


def exit_shortcut() -> dict:
    """Exit/stop the shortcut"""
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.exit",
        "WFWorkflowActionParameters": {},
    }


def choose_from_list(
    prompt: str = None, select_multiple: bool = False
) -> tuple[dict, str]:
    """Choose from a list. Returns (action, uuid)."""
    action_uuid = new_uuid()
    params = {"UUID": action_uuid}
    if prompt:
        params["WFChooseFromListActionPrompt"] = prompt
    if select_multiple:
        params["WFChooseFromListActionSelectMultiple"] = True
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefromlist",
        "WFWorkflowActionParameters": params,
    }, action_uuid


def get_text_from_input() -> tuple[dict, str]:
    """Get text from previous action. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.detect.text",
        "WFWorkflowActionParameters": {"UUID": action_uuid},
    }, action_uuid


def get_dictionary_from_input() -> tuple[dict, str]:
    """Parse JSON/dictionary from input. Returns (action, uuid)."""
    action_uuid = new_uuid()
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.detect.dictionary",
        "WFWorkflowActionParameters": {"UUID": action_uuid},
    }, action_uuid
