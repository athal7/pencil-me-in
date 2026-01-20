#!/usr/bin/env python3
"""
Build "Pencil Me In" main shortcut

Flow:
1. Load config JSON from iCloud
2. Get busy times from calendar
3. Ask ChatGPT to fetch sources and return events as JSON
4. Loop through events, letting user choose action for each
"""

import sys

sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    comment,
    set_variable_from_action,
    get_variable,
    show_alert,
    get_file,
    get_dictionary_from_input,
    get_dictionary_value_from_variable,
    get_upcoming_events,
    ask_apple_ai_with_variables,
    repeat_each_start,
    repeat_each_end,
    menu_item,
    menu_end,
    text_with_variable,
    add_calendar_event_from_variables,
    add_reminder_from_variable,
    share_variable,
    menu_start_with_variable_prompt,
)

CONFIG_PATH = "pencil-me-in-config.json"

PROMPT = """You are a family event assistant. Find upcoming events and return them as JSON.

## CONFIG
{config}

## BUSY TIMES (avoid conflicts)
{busy_events}

## INSTRUCTIONS
1. Read the config for location, kids' ages, sources, streaming services, and preferences.

2. For each enabled source:
   - If type is "ics": fetch the URL and parse VEVENT entries
   - If type is "webpage": fetch the page and extract events

3. Filter events:
   - Only events in the next 14 days
   - No conflicts with busy times
   - Age-appropriate for the kids listed

4. If preferences allow, also find:
   - Sports games on the user's streaming services
   - Family-friendly TV/movie premieres

## OUTPUT FORMAT
Return ONLY a JSON array (no markdown, no explanation):
[
  {
    "title": "Event Name",
    "date": "2024-01-20",
    "time": "2:00 PM",
    "location": "Venue Address",
    "description": "Brief description",
    "source": "Source name",
    "url": "https://...",
    "category": "Community|Library|Sports|Streaming|Kids",
    "needs_tickets": true,
    "ticket_date": "2024-01-15"
  }
]

Use human-readable date/time formats.
Include "needs_tickets": true and "ticket_date" for events requiring advance purchase.
Return empty array [] if no events found."""


def build_main_shortcut():
    actions = []

    actions.append(comment("=== Pencil Me In ==="))

    # 1. Load config
    actions.append(comment("1. Load config"))
    get_config, config_uuid = get_file(CONFIG_PATH, error_if_not_found=True)
    actions.append(get_config)
    actions.append(set_variable_from_action("config", config_uuid, "File"))

    # 2. Get busy times
    actions.append(comment("2. Get busy times"))
    calendar_events, cal_uuid = get_upcoming_events(count=50)
    actions.append(calendar_events)
    actions.append(set_variable_from_action("busy_events", cal_uuid, "Calendar Events"))

    # 3. Ask ChatGPT for events as JSON
    actions.append(comment("3. Ask ChatGPT"))
    ai_action, ai_uuid = ask_apple_ai_with_variables(PROMPT, ["config", "busy_events"])
    actions.append(ai_action)
    actions.append(set_variable_from_action("events_json", ai_uuid, "Text"))

    # Parse JSON
    actions.append(comment("4. Parse JSON"))
    get_json, json_var_uuid = get_variable("events_json")
    actions.append(get_json)
    parse_json, dict_uuid = get_dictionary_from_input()
    actions.append(parse_json)
    actions.append(set_variable_from_action("events", dict_uuid, "Dictionary"))

    # 4. Loop through events
    actions.append(comment("5. Loop through events"))
    repeat_start, group_id = repeat_each_start("events")
    actions.append(repeat_start)

    # Get current event details from Repeat Item
    get_title, title_uuid = get_dictionary_value_from_variable("title", "Repeat Item")
    actions.append(get_title)
    actions.append(
        set_variable_from_action("event_title", title_uuid, "Dictionary Value")
    )

    get_date, date_uuid = get_dictionary_value_from_variable("date", "Repeat Item")
    actions.append(get_date)
    actions.append(
        set_variable_from_action("event_date", date_uuid, "Dictionary Value")
    )

    get_time, time_uuid = get_dictionary_value_from_variable("time", "Repeat Item")
    actions.append(get_time)
    actions.append(
        set_variable_from_action("event_time", time_uuid, "Dictionary Value")
    )

    get_loc, loc_uuid = get_dictionary_value_from_variable("location", "Repeat Item")
    actions.append(get_loc)
    actions.append(
        set_variable_from_action("event_location", loc_uuid, "Dictionary Value")
    )

    get_desc, desc_uuid = get_dictionary_value_from_variable(
        "description", "Repeat Item"
    )
    actions.append(get_desc)
    actions.append(
        set_variable_from_action("event_description", desc_uuid, "Dictionary Value")
    )

    get_url_action, url_uuid = get_dictionary_value_from_variable("url", "Repeat Item")
    actions.append(get_url_action)
    actions.append(set_variable_from_action("event_url", url_uuid, "Dictionary Value"))

    # Build summary text for menu prompt
    summary, summary_uuid = text_with_variable("", "event_title", "")
    actions.append(summary)
    actions.append(set_variable_from_action("event_summary", summary_uuid, "Text"))

    # Show menu for this event
    menu_action, menu_id = menu_start_with_variable_prompt(
        ["📅 Add to Calendar", "⏰ Remind Me", "💬 Share", "⏭️ Skip"], "event_summary"
    )
    actions.append(menu_action)

    # Option 1: Add to Calendar
    actions.append(menu_item("📅 Add to Calendar", menu_id))
    actions.append(
        add_calendar_event_from_variables(
            title_var="event_title",
            start_date_var="event_date",
            location_var="event_location",
            notes_var="event_description",
        )
    )

    # Option 2: Set Reminder
    actions.append(menu_item("⏰ Remind Me", menu_id))
    actions.append(
        add_reminder_from_variable(title_var="event_title", notes_var="event_url")
    )

    # Option 3: Share
    actions.append(menu_item("💬 Share", menu_id))
    actions.append(share_variable("event_summary"))

    # Option 4: Skip
    actions.append(menu_item("⏭️ Skip", menu_id))
    # Nothing to do

    actions.append(menu_end(menu_id))
    actions.append(repeat_each_end(group_id))

    # Done
    actions.append(show_alert("All Done!", "Finished reviewing events."))

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
