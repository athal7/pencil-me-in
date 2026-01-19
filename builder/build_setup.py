#!/usr/bin/env python3
"""
Build the "Pencil Me In Setup" shortcut

Flow:
- No config found → Run Quick Start automatically
- Config exists → Show menu (Edit Settings, Manage Sources, View Config, Re-run Quick Start)
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
    show_result_with_variable,
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
    choose_from_list,
    exit_shortcut,
)

CONFIG_PATH = "Shortcuts/pencil-me-in-config.json"


def build_quick_start_actions():
    """Build the Quick Start wizard actions"""
    actions = []

    actions.append(comment("=== Quick Start Wizard ==="))

    # Ask for location
    location_ask, _ = ask("What city/area do you live in?", default="Libertyville, IL")
    actions.append(location_ask)
    actions.append(set_variable("location"))

    # Create base config with location
    actions.append(comment("Create config with location"))
    config_template, _ = text(
        """{
  "version": 1,
  "location": "",
  "kids": [],
  "streaming_services": [],
  "sources": [],
  "calendars_to_check": ["Calendar"],
  "preferences": {
    "advance_ticket_weeks": 12,
    "reminder_lead_days": 14,
    "school_reminder_days": 7
  }
}"""
    )
    actions.append(config_template)
    parse_config, _ = get_dictionary_from_input()
    actions.append(parse_config)
    actions.append(set_variable("config"))

    # Set location in config
    get_cfg, _ = get_variable("config")
    actions.append(get_cfg)
    actions.append(
        set_dictionary_value("location", "￼")
    )  # Will be replaced by variable
    actions.append(set_variable("config"))

    # Ask ChatGPT to find local event sources
    actions.append(comment("AI-powered source discovery"))
    ai_prompt = """I need calendar feeds for family events near the location I'll provide.

Find ICS or RSS calendar feeds for:
1. Public libraries 
2. Local theatres and performing arts centers
3. Community centers and park districts

For each source found, provide:
- name: Organization name
- url: Direct URL to calendar feed (ICS preferred)
- type: "ics" or "rss"

Return ONLY a valid JSON array, no explanation:
[{"name": "Example Library", "url": "https://...", "type": "ics"}]

If you cannot find feeds, return: []

Location: """

    # Create prompt with location variable
    prompt_text, _ = text(ai_prompt)
    actions.append(prompt_text)
    actions.append(set_variable("ai_prompt_base"))

    ai_sources, _ = ask_chatgpt(
        ai_prompt + "{{location}}"
    )  # Note: this won't interpolate, but AI will see location context
    actions.append(ai_sources)
    actions.append(set_variable("ai_sources"))

    # Show what was found
    actions.append(
        show_result_with_variable("AI found these sources:\n\n", "ai_sources", "")
    )

    # Save config
    actions.append(comment("Save configuration"))
    get_final_config, _ = get_variable("config")
    actions.append(get_final_config)
    actions.append(save_file(CONFIG_PATH, overwrite=True))

    actions.append(
        show_alert(
            "Setup Complete! ✓",
            'Your configuration is saved.\n\nRun "Pencil Me In" to get your first weekly digest!',
        )
    )

    return actions


def build_setup_shortcut():
    """Build the Pencil Me In Setup shortcut"""
    actions = []

    # ==========================================================================
    # Header
    # ==========================================================================
    actions.append(comment("Pencil Me In Setup"))

    # ==========================================================================
    # Try to load existing config
    # ==========================================================================
    actions.append(comment("--- Check for existing config ---"))
    get_config_action, _ = get_file(CONFIG_PATH, error_if_not_found=False)
    actions.append(get_config_action)
    actions.append(set_variable("existing_config"))

    # ==========================================================================
    # Branch: Config exists vs doesn't exist
    # ==========================================================================
    has_config, has_config_id = if_has_value("existing_config")
    actions.append(has_config)

    # --------------------------------------------------------------------------
    # CONFIG EXISTS: Show management menu
    # --------------------------------------------------------------------------
    actions.append(comment("Config found - show management menu"))

    menu_items = [
        "View Config",
        "Edit Location",
        "Manage Sources",
        "Re-run Quick Start",
    ]
    main_menu, main_menu_id = menu_start(menu_items, prompt="Pencil Me In Setup")
    actions.append(main_menu)

    # --- View Config ---
    actions.append(menu_item("View Config", main_menu_id))
    actions.append(
        show_result_with_variable("Current Configuration:\n\n", "existing_config", "")
    )

    # --- Edit Location ---
    actions.append(menu_item("Edit Location", main_menu_id))
    new_loc, _ = ask("Enter your location:", default="")
    actions.append(new_loc)
    actions.append(set_variable("new_location"))

    # Load, modify, save config
    get_cfg, _ = get_variable("existing_config")
    actions.append(get_cfg)
    parse_cfg, _ = get_dictionary_from_input()
    actions.append(parse_cfg)
    actions.append(set_dictionary_value("location", "￼"))  # new_location
    actions.append(save_file(CONFIG_PATH, overwrite=True))
    actions.append(show_alert("Updated", "Location has been updated."))

    # --- Manage Sources ---
    actions.append(menu_item("Manage Sources", main_menu_id))
    get_cfg2, _ = get_variable("existing_config")
    actions.append(get_cfg2)
    parse_cfg2, _ = get_dictionary_from_input()
    actions.append(parse_cfg2)
    sources_val, _ = get_dictionary_value("sources")
    actions.append(sources_val)
    actions.append(
        show_result_with_variable(
            "Current sources:\n\n",
            "sources",
            "\n\nTo add/remove sources, edit the config file in iCloud Drive/Shortcuts/",
        )
    )

    # --- Re-run Quick Start ---
    actions.append(menu_item("Re-run Quick Start", main_menu_id))
    actions.append(
        show_alert(
            "Re-run Quick Start?",
            "This will replace your current configuration.",
            show_cancel=True,
        )
    )
    # Add Quick Start actions inline
    actions.extend(build_quick_start_actions())

    actions.append(menu_end(main_menu_id))

    # --------------------------------------------------------------------------
    # NO CONFIG: Run Quick Start automatically
    # --------------------------------------------------------------------------
    actions.append(otherwise(has_config_id))
    actions.append(comment("No config found - run Quick Start"))
    actions.append(
        show_alert(
            "Welcome to Pencil Me In!",
            "Let's set up your family event discovery.\n\nThis will only take a minute.",
        )
    )
    actions.extend(build_quick_start_actions())

    actions.append(end_if(has_config_id))

    # ==========================================================================
    # Create and save shortcut
    # ==========================================================================
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
