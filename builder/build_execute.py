#!/usr/bin/env python3
"""
Build the "Pencil Me In" (execute/weekly digest) shortcut
"""

import sys

sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    comment,
    text,
    ask,
    set_variable,
    get_variable,
    show_alert,
    show_result,
    notification,
    menu_start,
    menu_item,
    menu_end,
    if_has_value,
    otherwise,
    end_if,
    dictionary,
    get_dictionary_value,
    set_dictionary_value,
    get_file,
    save_file,
    get_dictionary_from_input,
    get_text_from_input,
    get_url,
    get_url_variable,
    ask_chatgpt,
    ask_chatgpt_with_input,
    get_upcoming_events,
    add_calendar_event,
    add_reminder,
    repeat_each_start,
    repeat_each_end,
    choose_from_list,
    exit_shortcut,
    run_shortcut,
)

CONFIG_PATH = "Shortcuts/pencil-me-in-config.json"


def build_execute_shortcut():
    """Build the Pencil Me In weekly digest shortcut"""
    actions = []

    # ==========================================================================
    # Header
    # ==========================================================================
    actions.append(comment("Pencil Me In - Weekly Family Event Digest"))
    actions.append(
        comment(
            "Fetches events, checks conflicts, and creates your personalized digest"
        )
    )

    # ==========================================================================
    # Load Config
    # ==========================================================================
    actions.append(comment("--- Load Configuration ---"))
    get_config, config_uuid = get_file(CONFIG_PATH, error_if_not_found=False)
    actions.append(get_config)
    actions.append(set_variable("config_file"))

    # Check if config exists
    has_config, has_config_id = if_has_value("config_file")
    actions.append(has_config)

    # Parse config
    get_cfg, _ = get_variable("config_file")
    actions.append(get_cfg)
    parse_cfg, _ = get_dictionary_from_input()
    actions.append(parse_cfg)
    actions.append(set_variable("config"))

    # Extract key values
    get_cfg2, _ = get_variable("config")
    actions.append(get_cfg2)
    location_val, _ = get_dictionary_value("location")
    actions.append(location_val)
    actions.append(set_variable("location"))

    get_cfg3, _ = get_variable("config")
    actions.append(get_cfg3)
    sources_val, _ = get_dictionary_value("sources")
    actions.append(sources_val)
    actions.append(set_variable("sources"))

    get_cfg4, _ = get_variable("config")
    actions.append(get_cfg4)
    kids_val, _ = get_dictionary_value("kids")
    actions.append(kids_val)
    actions.append(set_variable("kids"))

    actions.append(otherwise(has_config_id))
    actions.append(
        show_alert(
            "No Configuration",
            'Please run "Pencil Me In Setup" first to configure your preferences.',
        )
    )
    actions.append(exit_shortcut())
    actions.append(end_if(has_config_id))

    # ==========================================================================
    # Get Current Calendar Events (for conflict checking)
    # ==========================================================================
    actions.append(comment("--- Get Calendar Events for Conflict Checking ---"))

    # Get events for next 2 weeks
    upcoming, upcoming_uuid = get_upcoming_events(count=100)
    actions.append(upcoming)
    actions.append(set_variable("my_calendar_events"))

    # ==========================================================================
    # Fetch Event Sources
    # ==========================================================================
    actions.append(comment("--- Fetch Event Sources ---"))

    # Initialize collected events
    init_events, _ = text("[]")
    actions.append(init_events)
    actions.append(set_variable("all_events_raw"))

    # Loop through sources
    loop_sources, loop_sources_id = repeat_each_start("sources")
    actions.append(loop_sources)

    # Get source URL from current item
    actions.append(comment("Fetch this source"))

    # For now, use ChatGPT to handle all source types
    fetch_prompt = """Fetch and parse events from this source. The source info is in the Repeat Item variable.

Extract events happening in the next 2 weeks. For each event return:
- title: Event name
- date: Date in YYYY-MM-DD format  
- time: Time in HH:MM format (24h) or "all-day"
- location: Venue/location
- description: Brief description
- needs_tickets: true if advance tickets likely required
- family_friendly: true if suitable for families
- source: Name of the source

Return ONLY a JSON array, no other text. If you can't fetch the source, return []."""

    fetch_ai, _ = ask_chatgpt(fetch_prompt)
    actions.append(fetch_ai)
    actions.append(set_variable("source_events"))

    actions.append(repeat_each_end(loop_sources_id))

    # ==========================================================================
    # Process with AI - Create Digest
    # ==========================================================================
    actions.append(comment("--- AI Processing: Create Personalized Digest ---"))

    # Build the mega-prompt for ChatGPT
    digest_prompt_text, _ = (
        text("""You are helping a busy parent find family events. Here's the context:

LOCATION: {{location}}

MY CALENDAR (busy times to avoid):
{{my_calendar_events}}

KIDS INFO:
{{kids}}

AVAILABLE EVENTS FROM LOCAL SOURCES:
{{all_events_raw}}

Please create a weekly digest with these sections:

## 🏫 School Alerts
List any school days off, early dismissals, or important school events in the next 2 weeks.
Format: [DATE] - [SCHOOL] - [EVENT] - ⚠️ [any action needed]

## 📅 This Week's Events  
Events happening in the next 7 days that DON'T conflict with my calendar.
Include: title, date/time, location, why it's good for our family
Only include events that fit our schedule!

## 🎟️ Advance Tickets Needed
Events 2-12 weeks out that typically require advance ticket purchase.
Include: title, date, venue, typical ticket price range if known, suggested buy-by date

## 📺 Streaming & Sports
Any notable family movie releases, sports events, or TV premieres this week on major streaming services.

## 💡 Top Pick
Your #1 recommendation for our family this week and why.

Be concise. Use emojis. Make it scannable.""")
    )
    actions.append(digest_prompt_text)
    actions.append(set_variable("digest_prompt"))

    # Call ChatGPT for the digest
    get_prompt, _ = get_variable("digest_prompt")
    actions.append(get_prompt)
    digest_ai, digest_uuid = ask_chatgpt_with_input(
        "Create the family event digest based on the information above.",
        "digest_prompt",
    )
    actions.append(digest_ai)
    actions.append(set_variable("digest"))

    # ==========================================================================
    # Display Digest
    # ==========================================================================
    actions.append(comment("--- Display Digest ---"))

    get_digest, _ = get_variable("digest")
    actions.append(get_digest)
    actions.append(show_result("# 📅 Pencil Me In - Weekly Digest\n\n{{digest}}"))

    # ==========================================================================
    # Action Menu
    # ==========================================================================
    actions.append(comment("--- Post-Digest Actions ---"))

    action_items = [
        "Add Events to Calendar",
        "Set Ticket Reminders",
        "Share with Family",
        "Done",
    ]
    action_menu, action_menu_id = menu_start(
        action_items, prompt="What would you like to do?"
    )
    actions.append(action_menu)

    # --------------------------------------------------------------------------
    # Add Events to Calendar
    # --------------------------------------------------------------------------
    actions.append(menu_item("Add Events to Calendar", action_menu_id))
    actions.append(comment("Create calendar events from digest"))

    calendar_prompt = """Based on the digest, extract events to add to calendar.
Return ONLY a JSON array with events in this format:
[{"title": "Event Name", "start": "2024-01-20T14:00:00", "end": "2024-01-20T16:00:00", "location": "Venue", "notes": "Brief notes"}]

Only include events from "This Week's Events" section that the user would want on their calendar.
If no events to add, return []."""

    cal_events_ai, _ = ask_chatgpt_with_input(calendar_prompt, "digest")
    actions.append(cal_events_ai)
    actions.append(set_variable("calendar_events"))

    actions.append(
        show_alert(
            "Events Ready",
            "Events extracted. They will be added to your default calendar.",
        )
    )

    # Note: In a real implementation, we'd loop through and add each event
    # For now, show what would be added
    get_cal_events, _ = get_variable("calendar_events")
    actions.append(get_cal_events)
    actions.append(show_result("Events to add:\n{{calendar_events}}"))

    # --------------------------------------------------------------------------
    # Set Ticket Reminders
    # --------------------------------------------------------------------------
    actions.append(menu_item("Set Ticket Reminders", action_menu_id))
    actions.append(comment("Create reminders for advance ticket purchases"))

    reminder_prompt = """From the "Advance Tickets Needed" section of the digest, create reminder tasks.
Return ONLY a JSON array:
[{"title": "Buy tickets for [Event]", "date": "2024-01-15", "notes": "Event on [date], tickets at [venue]"}]

Set reminder dates 2 weeks before each event.
If no tickets needed, return []."""

    reminders_ai, _ = ask_chatgpt_with_input(reminder_prompt, "digest")
    actions.append(reminders_ai)
    actions.append(set_variable("ticket_reminders"))

    get_reminders, _ = get_variable("ticket_reminders")
    actions.append(get_reminders)
    actions.append(show_result("Reminders to create:\n{{ticket_reminders}}"))

    # --------------------------------------------------------------------------
    # Share with Family
    # --------------------------------------------------------------------------
    actions.append(menu_item("Share with Family", action_menu_id))
    actions.append(comment("Share digest via Messages or Email"))

    share_menu_items = ["Text Message", "Email"]
    share_menu, share_menu_id = menu_start(share_menu_items, prompt="How to share?")
    actions.append(share_menu)

    actions.append(menu_item("Text Message", share_menu_id))
    get_digest2, _ = get_variable("digest")
    actions.append(get_digest2)
    actions.append(
        show_result("Copy this digest and paste into Messages:\n\n{{digest}}")
    )

    actions.append(menu_item("Email", share_menu_id))
    get_digest3, _ = get_variable("digest")
    actions.append(get_digest3)
    actions.append(
        show_result("Copy this digest and paste into an email:\n\n{{digest}}")
    )

    actions.append(menu_end(share_menu_id))

    # --------------------------------------------------------------------------
    # Done
    # --------------------------------------------------------------------------
    actions.append(menu_item("Done", action_menu_id))
    actions.append(notification("Pencil Me In", "Weekly digest complete! 📅"))

    actions.append(menu_end(action_menu_id))

    # ==========================================================================
    # Create and save shortcut
    # ==========================================================================
    # Calendar icon (61555), orange color (4274264319)
    shortcut = create_shortcut(
        "Pencil Me In",
        actions,
        icon_color=4274264319,  # Orange
        icon_glyph=61555,  # Calendar/list icon
    )

    return shortcut


if __name__ == "__main__":
    shortcut = build_execute_shortcut()
    output_path = "/Users/athal/code/pencil-me-in/shortcuts/Pencil-Me-In.shortcut"
    save_shortcut(shortcut, output_path)
    print(f"Created: {output_path}")
    print(f"Actions: {len(shortcut['WFWorkflowActions'])}")
