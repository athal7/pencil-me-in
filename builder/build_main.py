#!/usr/bin/env python3
"""
Build "Pencil Me In" main shortcut

Simple flow:
1. Load config JSON from iCloud
2. Get busy times from calendar
3. Pass config + busy times to ChatGPT, let it fetch sources and generate ICS
4. Save ICS file
"""

import sys

sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    comment,
    set_variable,
    get_variable,
    show_alert,
    show_result_with_variable,
    get_file,
    save_file,
    get_dictionary_from_input,
    get_upcoming_events,
    ask_apple_ai_with_variables,
)

CONFIG_PATH = "Shortcuts/pencil-me-in-config.json"

PROMPT = """You are a family event assistant. Find upcoming events and create an ICS calendar file.

## CONFIG
{config}

## BUSY TIMES (from user's calendar - avoid scheduling conflicts)
{busy_events}

## INSTRUCTIONS
1. Read the config to understand:
   - Location and kids' ages (for age-appropriate filtering)
   - Event sources (fetch each enabled source URL)
   - Streaming services (for sports/TV recommendations if enabled in preferences)
   - Preferences (family_friendly_only, include_sports, include_tv_premieres)

2. For each enabled source in the config:
   - If type is "ics": fetch the URL and parse VEVENT entries
   - If type is "webpage": fetch the page and extract event information

3. Filter events:
   - Only events in the next 14 days
   - No conflicts with busy times
   - Age-appropriate for the kids listed

4. If preferences allow, also find:
   - Sports games on the user's streaming services
   - Family-friendly TV/movie premieres

## OUTPUT
Return ONLY valid ICS content (no markdown, no explanation):

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pencil Me In//EN
BEGIN:VEVENT
UID:unique-id@pencilmein
DTSTART:YYYYMMDD or YYYYMMDDTHHMMSS
DTEND:YYYYMMDD or YYYYMMDDTHHMMSS
SUMMARY:Event Title
LOCATION:Venue Address or "Streaming"
DESCRIPTION:Details and source URL
CATEGORIES:Community|Library|Sports|Streaming|Kids
END:VEVENT
END:VCALENDAR"""


def build_main_shortcut():
    actions = []

    actions.append(comment("=== Pencil Me In ==="))

    # 1. Load config
    actions.append(comment("1. Load config"))
    get_config, _ = get_file(CONFIG_PATH, error_if_not_found=True)
    actions.append(get_config)
    actions.append(set_variable("config"))

    # 2. Get busy times
    actions.append(comment("2. Get busy times"))
    calendar_events, _ = get_upcoming_events(count=50)
    actions.append(calendar_events)
    actions.append(set_variable("busy_events"))

    # 3. Ask ChatGPT
    actions.append(comment("3. Ask ChatGPT"))
    ai_action, _ = ask_apple_ai_with_variables(PROMPT, ["config", "busy_events"])
    actions.append(ai_action)
    actions.append(set_variable("ics_content"))

    # 4. Show results
    actions.append(comment("4. Show results"))
    actions.append(show_result_with_variable("📅 Events Found!\n\n", "ics_content", ""))

    # 5. Save ICS
    actions.append(comment("5. Save ICS"))
    get_ics, _ = get_variable("ics_content")
    actions.append(get_ics)
    actions.append(save_file("Shortcuts/pencil-me-in-events.ics", overwrite=True))

    actions.append(
        show_alert(
            "Events Saved!",
            "ICS file saved to iCloud > Shortcuts.\n\nOpen it to add events to your calendar.",
        )
    )

    return create_shortcut(
        "Pencil Me In",
        actions,
        icon_color=431817727,
        icon_glyph=59771,
    )


if __name__ == "__main__":
    shortcut = build_main_shortcut()
    output_path = "/Users/athal/code/pencil-me-in/shortcuts/Pencil-Me-In.shortcut"
    save_shortcut(shortcut, output_path)
    print(f"Created: {output_path}")
    print(f"Actions: {len(shortcut['WFWorkflowActions'])}")
