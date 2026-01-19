#!/usr/bin/env python3
"""
Build the "Pencil Me In Setup" shortcut
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
    ask_chatgpt,
    ask_chatgpt_with_input,
    choose_from_list,
    exit_shortcut,
    run_shortcut,
)

CONFIG_PATH = "Shortcuts/pencil-me-in-config.json"


def build_setup_shortcut():
    """Build the Pencil Me In Setup shortcut"""
    actions = []

    # ==========================================================================
    # Header comment
    # ==========================================================================
    actions.append(
        comment("Pencil Me In Setup - Configure your family event discovery")
    )

    # ==========================================================================
    # Try to load existing config
    # ==========================================================================
    actions.append(comment("--- Load existing config (if any) ---"))
    get_config_action, config_uuid = get_file(CONFIG_PATH, error_if_not_found=False)
    actions.append(get_config_action)
    actions.append(set_variable("existing_config"))

    # ==========================================================================
    # Main Menu
    # ==========================================================================
    actions.append(comment("--- Main Menu ---"))

    menu_items = [
        "Quick Start",
        "Add Event Source",
        "Manage Sources",
        "Edit Settings",
        "View Config",
    ]
    main_menu, main_menu_id = menu_start(menu_items, prompt="Pencil Me In Setup")
    actions.append(main_menu)

    # --------------------------------------------------------------------------
    # Quick Start
    # --------------------------------------------------------------------------
    actions.append(menu_item("Quick Start", main_menu_id))
    actions.append(comment("Quick Start wizard for first-time setup"))

    # Check if config already exists
    has_config, has_config_id = if_has_value("existing_config")
    actions.append(has_config)
    actions.append(
        show_alert(
            "Config Already Exists",
            'You already have a configuration. Running Quick Start will replace it. Use "Edit Settings" instead to modify your existing setup.',
            show_cancel=True,
        )
    )
    actions.append(end_if(has_config_id))

    # Ask for location
    location_ask, location_uuid = ask(
        "What city/area do you live in?", default="Libertyville, IL"
    )
    actions.append(location_ask)
    actions.append(set_variable("location"))

    # Ask about kids
    kids_ask, kids_uuid = ask("How many children do you have?", input_type="Number")
    actions.append(kids_ask)
    actions.append(set_variable("num_kids"))

    # Create base config
    actions.append(comment("Create initial config structure"))
    base_config_text, _ = text("""{
  "version": 1,
  "location": "",
  "kids": [],
  "streaming_services": [],
  "sources": [],
  "calendars_to_check": [],
  "preferences": {
    "advance_ticket_weeks": 12,
    "reminder_lead_days": 14,
    "school_reminder_days": 7
  }
}""")
    actions.append(base_config_text)
    config_dict, config_dict_uuid = get_dictionary_from_input()
    actions.append(config_dict)
    actions.append(set_variable("config"))

    # Set location in config
    get_config_var, _ = get_variable("config")
    actions.append(get_config_var)
    actions.append(set_dictionary_value("location", "{{location}}"))
    actions.append(set_variable("config"))

    # Ask ChatGPT to find local event sources
    actions.append(comment("AI-powered source discovery"))
    ai_prompt = """I live in {{location}}. Find me calendar feeds (ICS or RSS) for local family events. Look for:
1. Public libraries in my area
2. Local theatres and performing arts centers
3. Community centers and park districts
4. Children's museums

For each source, provide:
- Name
- URL to their calendar feed (ICS preferred, RSS if no ICS)
- Type (ics or rss)

Return ONLY a JSON array like this, no other text:
[{"name": "Example Library", "url": "https://...", "type": "ics"}]

If you can't find a calendar feed for a venue, omit it. Only include sources with working calendar URLs."""

    ai_sources, ai_sources_uuid = ask_chatgpt(ai_prompt)
    actions.append(ai_sources)
    actions.append(set_variable("ai_sources"))

    # Show what was found and let user confirm
    actions.append(
        show_alert(
            "Sources Found",
            "AI found some local event sources. Review them on the next screen.",
        )
    )

    get_ai_sources, _ = get_variable("ai_sources")
    actions.append(get_ai_sources)
    actions.append(show_result("Found sources:\n\n{{ai_sources}}"))

    # Save config
    actions.append(comment("Save configuration"))
    get_final_config, _ = get_variable("config")
    actions.append(get_final_config)
    actions.append(save_file(CONFIG_PATH, overwrite=True))

    actions.append(
        show_alert(
            "Setup Complete!",
            'Your Pencil Me In configuration has been saved. Run "Pencil Me In" to get your first weekly digest!',
        )
    )

    # --------------------------------------------------------------------------
    # Add Event Source
    # --------------------------------------------------------------------------
    actions.append(menu_item("Add Event Source", main_menu_id))
    actions.append(comment("Manually add a new event source"))

    source_name_ask, _ = ask('Source name (e.g., "Vernon Area Library")')
    actions.append(source_name_ask)
    actions.append(set_variable("source_name"))

    source_url_ask, _ = ask("Calendar URL (ICS, RSS, or webpage)")
    actions.append(source_url_ask)
    actions.append(set_variable("source_url"))

    # Ask AI to detect source type
    detect_prompt = """What type of calendar source is this URL: {{source_url}}

Respond with ONLY one word: ics, rss, or webpage"""
    detect_type, _ = ask_chatgpt(detect_prompt)
    actions.append(detect_type)
    actions.append(set_variable("source_type"))

    actions.append(
        show_alert(
            "Source Added",
            "Added {{source_name}} ({{source_type}})\n\nNote: Run Quick Start first if you haven't set up your config yet.",
        )
    )

    # --------------------------------------------------------------------------
    # Manage Sources
    # --------------------------------------------------------------------------
    actions.append(menu_item("Manage Sources", main_menu_id))
    actions.append(comment("View and manage configured sources"))

    # Check if config exists
    has_config2, has_config2_id = if_has_value("existing_config")
    actions.append(has_config2)

    get_cfg, _ = get_variable("existing_config")
    actions.append(get_cfg)
    cfg_dict, _ = get_dictionary_from_input()
    actions.append(cfg_dict)
    sources_val, _ = get_dictionary_value("sources")
    actions.append(sources_val)
    actions.append(show_result("Current sources:\n\n{{Sources}}"))

    actions.append(otherwise(has_config2_id))
    actions.append(
        show_alert("No Config", "Run Quick Start first to create your configuration.")
    )
    actions.append(end_if(has_config2_id))

    # --------------------------------------------------------------------------
    # Edit Settings
    # --------------------------------------------------------------------------
    actions.append(menu_item("Edit Settings", main_menu_id))
    actions.append(comment("Edit preferences"))

    settings_menu_items = ["Change Location", "Streaming Services", "Reminder Settings"]
    settings_menu, settings_menu_id = menu_start(
        settings_menu_items, prompt="Edit Settings"
    )
    actions.append(settings_menu)

    # Change Location
    actions.append(menu_item("Change Location", settings_menu_id))
    new_loc, _ = ask("Enter your new location")
    actions.append(new_loc)
    actions.append(set_variable("new_location"))
    actions.append(show_alert("Location Updated", "Location set to {{new_location}}"))

    # Streaming Services
    actions.append(menu_item("Streaming Services", settings_menu_id))
    streaming_prompt = """List the streaming services available in {{location}} that show live sports and have family content.
Return as a simple comma-separated list, nothing else.
Example: Netflix, Disney+, Hulu, Peacock, ABC, ESPN+"""
    streaming_ai, _ = ask_chatgpt(streaming_prompt)
    actions.append(streaming_ai)
    actions.append(set_variable("available_streaming"))
    actions.append(
        show_result(
            "Available services in your area:\n{{available_streaming}}\n\nSelect which ones you have in the next prompt."
        )
    )

    # Reminder Settings
    actions.append(menu_item("Reminder Settings", settings_menu_id))
    reminder_days, _ = ask(
        "Days before event to remind about tickets?", default="14", input_type="Number"
    )
    actions.append(reminder_days)
    actions.append(set_variable("reminder_days"))
    actions.append(
        show_alert(
            "Reminder Updated",
            "Will remind {{reminder_days}} days before events that need advance tickets.",
        )
    )

    actions.append(menu_end(settings_menu_id))

    # --------------------------------------------------------------------------
    # View Config
    # --------------------------------------------------------------------------
    actions.append(menu_item("View Config", main_menu_id))
    actions.append(comment("Display current configuration"))

    has_config3, has_config3_id = if_has_value("existing_config")
    actions.append(has_config3)
    get_cfg2, _ = get_variable("existing_config")
    actions.append(get_cfg2)
    actions.append(show_result("Current Configuration:\n\n{{existing_config}}"))
    actions.append(otherwise(has_config3_id))
    actions.append(
        show_alert(
            "No Config", "No configuration found. Run Quick Start to create one."
        )
    )
    actions.append(end_if(has_config3_id))

    # --------------------------------------------------------------------------
    # End Main Menu
    # --------------------------------------------------------------------------
    actions.append(menu_end(main_menu_id))

    # ==========================================================================
    # Create and save shortcut
    # ==========================================================================
    # Pencil icon (59771), teal color (431817727)
    shortcut = create_shortcut(
        "Pencil Me In Setup",
        actions,
        icon_color=431817727,  # Teal
        icon_glyph=59771,  # Pencil
    )

    return shortcut


if __name__ == "__main__":
    shortcut = build_setup_shortcut()
    output_path = "/Users/athal/code/pencil-me-in/shortcuts/Pencil-Me-In-Setup.shortcut"
    save_shortcut(shortcut, output_path)
    print(f"Created: {output_path}")
    print(f"Actions: {len(shortcut['WFWorkflowActions'])}")
