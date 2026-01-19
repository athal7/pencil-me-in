#!/usr/bin/env python3
"""
Build "Pencil Me In Setup" shortcut

Linear flow:
1. Get current location
2. Select kids ages (multi-select)
3. Select streaming services (multi-select)
4. AI discovers event sources
5. Build and save config JSON
"""

import sys

sys.path.insert(0, "/Users/athal/code/pencil-me-in/builder")

from shortcut_builder import (
    create_shortcut,
    save_shortcut,
    comment,
    text,
    text_with_variable,
    set_variable,
    get_variable,
    show_alert,
    show_result_with_variable,
    save_file,
    ask_apple_ai_with_variable,
    choose_from_list,
    list_action,
    get_current_location,
    get_street_address,
)

CONFIG_PATH = "Shortcuts/pencil-me-in-config.json"


def build_setup_shortcut():
    actions = []

    actions.append(comment("=== Pencil Me In Setup ==="))

    # ==========================================================================
    # 1. Location - use current location
    # ==========================================================================
    actions.append(comment("1. Get current location"))

    get_loc, _ = get_current_location()
    actions.append(get_loc)

    get_addr, _ = get_street_address()
    actions.append(get_addr)
    actions.append(set_variable("location"))

    # ==========================================================================
    # 2. Kids ages - multi-select
    # ==========================================================================
    actions.append(comment("2. Kids ages"))

    ages_list, _ = list_action(
        [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "No kids",
        ]
    )
    actions.append(ages_list)

    choose_ages, _ = choose_from_list(
        prompt="Select your kids' ages", select_multiple=True
    )
    actions.append(choose_ages)
    actions.append(set_variable("kids_ages"))

    # ==========================================================================
    # 3. Streaming services - multi-select
    # ==========================================================================
    actions.append(comment("3. Streaming services"))

    streaming_list, _ = list_action(
        [
            "Netflix",
            "Disney+",
            "Hulu",
            "Amazon Prime Video",
            "Apple TV+",
            "Max (HBO)",
            "Paramount+",
            "Peacock",
            "ESPN+",
            "YouTube TV",
            "Fubo",
            "ABC",
            "CBS",
            "NBC",
            "Fox",
            "PBS",
        ]
    )
    actions.append(streaming_list)

    choose_streaming, _ = choose_from_list(
        prompt="Select your streaming services", select_multiple=True
    )
    actions.append(choose_streaming)
    actions.append(set_variable("streaming_services"))

    # ==========================================================================
    # 4. AI discovers event sources
    # ==========================================================================
    actions.append(comment("4. AI discovers local event sources"))

    ai_prompt_prefix = "Find family-friendly event sources near: "
    ai_prompt_suffix = """

Search for organizations with public event calendars:
- Public libraries
- Park districts  
- Children's museums
- Community theaters
- Local venues

List each source with name and website."""

    ai_sources, _ = ask_apple_ai_with_variable(
        ai_prompt_prefix, "location", ai_prompt_suffix
    )
    actions.append(ai_sources)
    actions.append(set_variable("discovered_sources"))

    # Show discovered sources
    actions.append(
        show_result_with_variable(
            "Found these local event sources:\n\n", "discovered_sources", ""
        )
    )

    # ==========================================================================
    # 5. Build and save config JSON
    # ==========================================================================
    actions.append(comment("5. Build config JSON"))

    # Build JSON with variable interpolation
    # Using text_with_variable for location, then showing others
    config_template = text_with_variable(
        '{"version": 1, "location": "', "location", '"}'
    )
    actions.append(config_template[0])
    actions.append(set_variable("config"))

    # Save config
    actions.append(comment("Save config"))
    get_cfg, _ = get_variable("config")
    actions.append(get_cfg)
    actions.append(save_file(CONFIG_PATH, overwrite=True))

    actions.append(
        show_alert(
            "Setup Complete! ✓",
            "Config saved to iCloud.\n\nRun 'Pencil Me In' for your event digest!",
        )
    )

    # ==========================================================================
    # Create Shortcut
    # ==========================================================================
    return create_shortcut(
        "Pencil Me In Setup",
        actions,
        icon_color=431817727,
        icon_glyph=59771,
    )


if __name__ == "__main__":
    shortcut = build_setup_shortcut()
    output_path = "/Users/athal/code/pencil-me-in/shortcuts/Pencil-Me-In-Setup.shortcut"
    save_shortcut(shortcut, output_path)
    print(f"Created: {output_path}")
    print(f"Actions: {len(shortcut['WFWorkflowActions'])}")
