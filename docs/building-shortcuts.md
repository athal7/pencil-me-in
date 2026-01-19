# Building the Shortcuts

This guide provides step-by-step instructions to build both Pencil Me In shortcuts manually in the Apple Shortcuts app.

## Prerequisites

- iOS 17+ or macOS Sonoma+
- Shortcuts app
- Familiarity with adding actions in Shortcuts

## Shortcut 1: Pencil Me In Setup

This shortcut handles all configuration—location, kids, schools, streaming services, event sources, and preferences.

### Create the Shortcut

1. Open **Shortcuts** app
2. Tap **+** to create new shortcut
3. Tap the name at top → rename to **"Pencil Me In Setup"**
4. Tap the **ⓘ** icon → enable **"Show in Share Sheet"** (optional)

### Variables We'll Use

Throughout this shortcut, we'll use these variables:
- `Config` - The main configuration dictionary
- `ConfigPath` - Path to config file in iCloud

---

### Section 1: Load Existing Config

```
Action 1: Text
  └── Content: "Shortcuts/pencil-me-in-config.json"
  └── Set Variable: ConfigPath

Action 2: Get File
  └── Service: iCloud Drive
  └── File Path: ConfigPath
  └── Error: Continue (don't stop if file doesn't exist)

Action 3: If
  └── Condition: File Has Any Value
  
  Action 4: Get Dictionary from Input
    └── Input: File
    └── Set Variable: Config
    
  Action 5: Otherwise
  
  Action 6: Dictionary
    └── Add Item: version = 1 (Number)
    └── Set Variable: Config
    
  Action 7: End If
```

---

### Section 2: Main Menu

```
Action 8: Choose from Menu
  └── Prompt: "Pencil Me In Setup"
  └── Options:
      - "🚀 Quick Start"
      - "📍 Location & Family"
      - "📺 Streaming Services"
      - "📅 Event Sources"
      - "🏫 School Calendars"
      - "🗓️ Conflict Calendars"
      - "⏰ Reminder Settings"
      - "⚙️ View/Reset Config"
```

---

### Section 3: Quick Start Branch

```
Case: "🚀 Quick Start"

  Action 9: Ask for Input
    └── Prompt: "Where do you live? (city, state)"
    └── Input Type: Text
    └── Default: ""
    └── Set Variable: Location

  Action 10: Set Dictionary Value
    └── Dictionary: Config
    └── Key: location
    └── Value: Location
    └── Set Variable: Config

  Action 11: Ask for Input
    └── Prompt: "Kids ages? (comma-separated, or 'none')"
    └── Input Type: Text
    └── Default: "none"
    └── Set Variable: KidsAgesInput

  Action 12: If
    └── Condition: KidsAgesInput is not "none"
    
    Action 13: Split Text
      └── Input: KidsAgesInput
      └── Separator: ","
      └── Set Variable: KidsAgesList
      
    Action 14: Set Dictionary Value
      └── Dictionary: Config
      └── Key: kids_ages
      └── Value: KidsAgesList
      └── Set Variable: Config
    
    Action 15: End If

  Action 16: List
    └── Items:
        - "ABC"
        - "CBS"
        - "NBC"
        - "Fox"
        - "PBS"
        - "Netflix"
        - "Disney+"
        - "Hulu"
        - "Amazon Prime Video"
        - "Apple TV+"
        - "Max (HBO)"
        - "Paramount+"
        - "Peacock"
        - "YouTube TV"
        - "ESPN+"

  Action 17: Choose from List
    └── Input: List
    └── Prompt: "Select your streaming services"
    └── Select Multiple: ON
    └── Set Variable: StreamingServices

  Action 18: Set Dictionary Value
    └── Dictionary: Config
    └── Key: streaming_services
    └── Value: StreamingServices
    └── Set Variable: Config

  Action 19: Text
    └── Content: "Based on the user's location ([Location]), suggest any regional sports networks or streaming services they might have access to. Return as a simple comma-separated list, or 'none' if no regional suggestions. Examples: Marquee Sports (Chicago), NBC Sports Bay Area, YES Network (NY)."

  Action 20: Ask ChatGPT
    └── Input: Text
    └── Set Variable: RegionalSuggestions

  Action 21: If
    └── Condition: RegionalSuggestions is not "none"
    
    Action 22: Show Alert
      └── Title: "Regional Services"
      └── Message: "AI suggests you might have: [RegionalSuggestions]. Add these to your list?"
      └── Buttons: "Add" / "Skip"
    
    Action 23: If (button = "Add")
      └── (Add regional services logic - append to streaming list)
    Action 24: End If
    
    Action 25: End If

  Action 26: Choose from Menu
    └── Prompt: "Find local event sources now?"
    └── Options: "Yes, find sources" / "Skip for now"

  Case: "Yes, find sources"
    └── (Jump to Find Sources section - see Section 5)

  Case: "Skip for now"
    └── Continue

  Action 27: Find Calendar Events
    └── Filter: All Calendars
    └── Get: Calendar (property)
    └── Set Variable: AvailableCalendars
    
  Action 28: Choose from List
    └── Input: AvailableCalendars (unique values)
    └── Prompt: "Which calendars to check for conflicts?"
    └── Select Multiple: ON
    └── Set Variable: ConflictCalendars

  Action 29: Set Dictionary Value
    └── Dictionary: Config
    └── Key: calendars_to_check
    └── Value: ConflictCalendars
    └── Set Variable: Config

  Action 30: Ask for Input
    └── Prompt: "Days before event to remind about tickets?"
    └── Input Type: Number
    └── Default: 14
    └── Set Variable: ReminderLeadDays

  Action 31: Dictionary
    └── Add Item: reminder_lead_days = ReminderLeadDays
    └── Add Item: school_reminder_days = 7
    └── Add Item: family_friendly_only = true
    └── Add Item: advance_ticket_weeks = 12
    └── Set Variable: Preferences

  Action 32: Set Dictionary Value
    └── Dictionary: Config
    └── Key: preferences
    └── Value: Preferences
    └── Set Variable: Config

  Action 33: Get Current Date
    └── Format: ISO 8601
    └── Set Variable: Now

  Action 34: Set Dictionary Value
    └── Dictionary: Config
    └── Key: last_updated
    └── Value: Now
    └── Set Variable: Config

  Action 35: Save File
    └── Input: Config (as JSON)
    └── Service: iCloud Drive
    └── Path: ConfigPath
    └── Overwrite: ON

  Action 36: Show Alert
    └── Title: "✅ Setup Complete!"
    └── Message: "Location: [Location]\nStreaming: [count] services\nCalendars: [count] selected\n\nRun 'Pencil Me In' to get your digest!"
    └── Buttons: "Run Now" / "Done"

  Action 37: If (button = "Run Now")
    └── Run Shortcut: "Pencil Me In"
  Action 38: End If

End Case (Quick Start)
```

---

### Section 4: Location & Family Branch

```
Case: "📍 Location & Family"

  Action: Get Dictionary Value
    └── Key: location
    └── Set Variable: CurrentLocation

  Action: Get Dictionary Value
    └── Key: kids
    └── Set Variable: CurrentKids

  Action: Choose from Menu
    └── Prompt: "Location & Family"
    └── Options:
        - "Change Location (current: [CurrentLocation])"
        - "Add/Edit Kids"
        - "Back"

  Case: "Change Location"
    Action: Ask for Input
      └── Prompt: "Where do you live?"
      └── Default: CurrentLocation
      └── Set Variable: NewLocation
    
    Action: Set Dictionary Value
      └── Key: location
      └── Value: NewLocation
    
    Action: Save File (config)

  Case: "Add/Edit Kids"
    Action: Choose from Menu
      └── Options: "Add Child" / "Edit Child" / "Remove Child" / "Back"
    
    Case: "Add Child"
      Action: Ask for Input
        └── Prompt: "Child's name"
        └── Set Variable: ChildName
      
      Action: Ask for Input
        └── Prompt: "Child's age"
        └── Input Type: Number
        └── Set Variable: ChildAge
      
      Action: Dictionary
        └── name = ChildName
        └── age = ChildAge
        └── Set Variable: NewChild
      
      Action: Get Dictionary Value
        └── Key: kids
        └── Set Variable: KidsList
      
      Action: If (KidsList has no value)
        Action: List (empty)
          └── Set Variable: KidsList
      End If
      
      Action: Add to Variable
        └── Variable: KidsList
        └── Value: NewChild
      
      Action: Set Dictionary Value
        └── Key: kids
        └── Value: KidsList
      
      Action: Save File (config)

End Case (Location & Family)
```

---

### Section 5: Event Sources Branch (with AI Discovery)

```
Case: "📅 Event Sources"

  Action: Choose from Menu
    └── Prompt: "Event Sources"
    └── Options:
        - "🔍 Find Sources (AI)"
        - "➕ Add Manually"
        - "🧪 Test Sources"
        - "➖ Remove Source"
        - "📋 List Sources"
        - "Back"

  Case: "🔍 Find Sources (AI)"
  
    Action: List
      └── Items:
          - "Libraries"
          - "Theatres & Venues"
          - "Community Events"
          - "Kids Activities"
          - "Sports"
    
    Action: Choose from List
      └── Prompt: "What types of sources?"
      └── Select Multiple: ON
      └── Set Variable: SourceTypes
    
    Action: Get Dictionary Value
      └── Key: location
      └── Set Variable: Location
    
    Action: Text
      └── Content: 
          """
          Find calendar feeds and event sources for [SourceTypes] near [Location].
          
          For each source, provide:
          - name: Organization/venue name
          - url: Direct URL to calendar feed or events page
          - type: "ics" (calendar feed), "rss" (RSS feed), or "webpage" (HTML page)
          - description: Brief description
          
          Prefer ICS and RSS feeds when available. For webpages, verify the URL is accessible.
          
          Return as valid JSON array:
          [
            {"name": "", "url": "", "type": "", "description": ""}
          ]
          
          Return at least 3-5 sources if possible.
          """
    
    Action: Ask ChatGPT
      └── Input: Text
      └── Set Variable: AIResponse
    
    Action: Get Dictionary from Input
      └── Input: AIResponse
      └── Set Variable: FoundSources
    
    Action: Repeat with Each (FoundSources)
      └── Set Variable: Source
      
      Action: Get Dictionary Value (name from Source)
      Action: Get Dictionary Value (type from Source)
      Action: Get Dictionary Value (description from Source)
      
      Action: Text
        └── "[name] ([type])\n[description]"
        └── Add to Variable: SourceDisplayList
      
    End Repeat
    
    Action: Choose from List
      └── Input: SourceDisplayList
      └── Prompt: "Select sources to add"
      └── Select Multiple: ON
      └── Set Variable: SelectedSources
    
    Action: Repeat with Each (SelectedSources)
      └── (Match back to original FoundSources by name)
      └── (Test URL)
      └── (Get sample event via ChatGPT if webpage)
      └── (Add to config sources array)
    End Repeat
    
    Action: Save File (config)
    
    Action: Show Alert
      └── "Added [count] sources!"

  Case: "➕ Add Manually"
  
    Action: Ask for Input
      └── Prompt: "Source name"
      └── Set Variable: SourceName
    
    Action: Ask for Input
      └── Prompt: "URL"
      └── Input Type: URL
      └── Set Variable: SourceURL
    
    Action: Choose from Menu
      └── Prompt: "Source type"
      └── Options: "ICS (Calendar Feed)" / "RSS Feed" / "Webpage"
      └── Set Variable: SourceType
    
    Action: (Map menu choice to type value: ics/rss/webpage)
    
    Action: Get Contents of URL
      └── URL: SourceURL
      └── Set Variable: TestContent
    
    Action: If (error or no content)
      Action: Show Alert
        └── "Could not fetch URL. Add anyway?"
        └── Buttons: "Add Anyway" / "Cancel"
    End If
    
    Action: If (SourceType = "webpage")
      Action: Text
        └── "Extract one sample event from this HTML. Return: title, date, time, location. If no events found, return 'no events'.\n\n[TestContent]"
      Action: Ask ChatGPT
        └── Set Variable: SampleEvent
      Action: Show Alert
        └── "Sample event: [SampleEvent]"
    Else
      Action: (Parse ICS/RSS to show sample)
    End If
    
    Action: Get Current Date
      └── Format: yyyy-MM-dd
      └── Set Variable: Today
    
    Action: Dictionary
      └── name = SourceName
      └── url = SourceURL
      └── type = SourceType
      └── enabled = true
      └── added = Today
      └── Set Variable: NewSource
    
    Action: Get Dictionary Value
      └── Key: sources
      └── Set Variable: SourcesList
    
    Action: If (SourcesList has no value)
      Action: List (empty)
        └── Set Variable: SourcesList
    End If
    
    Action: Add to Variable
      └── Variable: SourcesList
      └── Value: NewSource
    
    Action: Set Dictionary Value
      └── Key: sources
      └── Value: SourcesList
    
    Action: Save File (config)

  Case: "🧪 Test Sources"
  
    Action: Get Dictionary Value
      └── Key: sources
      └── Set Variable: Sources
    
    Action: If (Sources is empty)
      Action: Show Alert
        └── "No sources configured. Add some first!"
      Action: Stop
    End If
    
    Action: Set Variable: TestResults = ""
    
    Action: Repeat with Each (Sources)
      └── Set Variable: Source
      
      Action: Get Dictionary Value (name from Source)
        └── Set Variable: SourceName
      Action: Get Dictionary Value (url from Source)
        └── Set Variable: SourceURL
      Action: Get Dictionary Value (type from Source)
        └── Set Variable: SourceType
      
      Action: Get Contents of URL
        └── URL: SourceURL
        └── Set Variable: Content
        └── Error: Continue
      
      Action: If (error)
        Action: Text
          └── "❌ [SourceName]: Failed to fetch\n"
          └── Add to Variable: TestResults
      Else
        Action: If (SourceType = "webpage")
          Action: Text
            └── "Extract one upcoming event from this HTML. Return format: 'Title - Date at Time'. If none found, return 'No events found'.\n\n[first 5000 chars of Content]"
          Action: Ask ChatGPT
            └── Set Variable: SampleEvent
        Else If (SourceType = "ics")
          Action: (Parse first VEVENT from ICS)
          └── Set Variable: SampleEvent
        Else (rss)
          Action: (Parse first item from RSS)
          └── Set Variable: SampleEvent
        End If
        
        Action: Text
          └── "✅ [SourceName] ([SourceType])\n   Sample: [SampleEvent]\n\n"
          └── Add to Variable: TestResults
      End If
      
    End Repeat
    
    Action: Quick Look
      └── Input: TestResults

  Case: "➖ Remove Source"
    
    Action: Get Dictionary Value
      └── Key: sources
      └── Set Variable: Sources
    
    Action: (Build list of source names)
    
    Action: Choose from List
      └── Prompt: "Which source to remove?"
      └── Set Variable: SourceToRemove
    
    Action: (Filter Sources to remove selected)
    
    Action: Set Dictionary Value
      └── Key: sources
    
    Action: Save File (config)

  Case: "📋 List Sources"
    
    Action: Get Dictionary Value
      └── Key: sources
      └── Set Variable: Sources
    
    Action: (Format as readable list)
    
    Action: Quick Look

End Case (Event Sources)
```

---

### Section 6: School Calendars Branch

```
Case: "🏫 School Calendars"

  Action: Choose from Menu
    └── Prompt: "School Calendars"
    └── Options:
        - "Add School Calendar"
        - "Remove School Calendar"
        - "List School Calendars"
        - "Back"

  Case: "Add School Calendar"
  
    Action: Get Dictionary Value
      └── Key: kids
      └── Set Variable: Kids
    
    Action: If (Kids is empty)
      Action: Show Alert
        └── "Add children first in Location & Family"
      Action: Stop
    End If
    
    Action: (Build list of kid names)
    
    Action: Choose from List
      └── Prompt: "Which child?"
      └── Set Variable: SelectedKid
    
    Action: Ask for Input
      └── Prompt: "School or district name"
      └── Set Variable: SchoolName
    
    Action: Get Dictionary Value
      └── Key: location
      └── Set Variable: Location
    
    Action: Text
      └── """
          Find the calendar feed for [SchoolName] near [Location].
          
          Look for:
          1. Direct ICS/iCal feed URL
          2. RSS feed for events
          3. Main calendar webpage URL
          
          Return JSON:
          {
            "name": "Full school/district name",
            "url": "calendar URL",
            "type": "ics" or "rss" or "webpage",
            "sample_events": ["Event 1 - Date", "Event 2 - Date"]
          }
          
          If no calendar found, return {"error": "No calendar found"}
          """
    
    Action: Ask ChatGPT
      └── Set Variable: SchoolResult
    
    Action: Get Dictionary from Input
      └── Set Variable: SchoolCalendar
    
    Action: Get Dictionary Value (error)
    
    Action: If (error exists)
      Action: Show Alert
        └── "Couldn't find calendar automatically. Add manually?"
        └── Buttons: "Add Manually" / "Cancel"
      
      Case: "Add Manually"
        Action: Ask for Input
          └── Prompt: "Calendar URL"
          └── Set Variable: SchoolURL
        Action: Choose from Menu
          └── Options: "ICS" / "RSS" / "Webpage"
          └── Set Variable: SchoolType
    Else
      Action: Get Dictionary Value (sample_events)
        └── Set Variable: Samples
      Action: Show Alert
        └── "Found: [name]\n\nSample events:\n[Samples]\n\nAdd this calendar?"
        └── Buttons: "Add" / "Cancel"
    End If
    
    Action: (Find the kid in Kids array)
    Action: (Add school object to that kid's record)
    Action: Set Dictionary Value (update kids array)
    Action: Save File (config)

End Case (School Calendars)
```

---

### Section 7: Conflict Calendars Branch

```
Case: "🗓️ Conflict Calendars"

  Action: Get Dictionary Value
    └── Key: calendars_to_check
    └── Set Variable: CurrentCalendars
  
  Action: Show Alert
    └── "Currently checking: [CurrentCalendars]"
  
  Action: Find Calendar Events
    └── (to get list of available calendars)
  
  Action: (Extract unique calendar names)
  
  Action: Choose from List
    └── Prompt: "Select calendars to check for conflicts"
    └── Select Multiple: ON
    └── Set Variable: NewCalendars
  
  Action: Set Dictionary Value
    └── Key: calendars_to_check
    └── Value: NewCalendars
  
  Action: Save File (config)

End Case
```

---

### Section 8: Reminder Settings Branch

```
Case: "⏰ Reminder Settings"

  Action: Get Dictionary Value
    └── Key: preferences
    └── Set Variable: Prefs
  
  Action: Get Dictionary Value (reminder_lead_days from Prefs)
    └── Set Variable: CurrentLeadDays
  
  Action: Get Dictionary Value (school_reminder_days from Prefs)
    └── Set Variable: CurrentSchoolDays
  
  Action: Ask for Input
    └── Prompt: "Days before event to remind about tickets"
    └── Input Type: Number
    └── Default: CurrentLeadDays
    └── Set Variable: NewLeadDays
  
  Action: Set Dictionary Value
    └── Dictionary: Prefs
    └── Key: reminder_lead_days
    └── Value: NewLeadDays
  
  Action: (Note: school_reminder_days is fixed at 7)
  
  Action: Get All Reminder Lists
  
  Action: Choose from List
    └── Prompt: "Which list for reminders?"
    └── Set Variable: ReminderList
  
  Action: Set Dictionary Value
    └── Dictionary: Prefs
    └── Key: reminder_list
    └── Value: ReminderList
  
  Action: Set Dictionary Value
    └── Dictionary: Config
    └── Key: preferences
    └── Value: Prefs
  
  Action: Save File (config)

End Case
```

---

### Section 9: View/Reset Config Branch

```
Case: "⚙️ View/Reset Config"

  Action: Choose from Menu
    └── Options: "View Config" / "Reset Config" / "Back"

  Case: "View Config"
    Action: Quick Look
      └── Input: Config (formatted as JSON)

  Case: "Reset Config"
    Action: Show Alert
      └── "Delete all settings? This cannot be undone."
      └── Buttons: "Delete" / "Cancel"
    
    Case: "Delete"
      Action: Delete File
        └── Path: ConfigPath
      Action: Show Alert
        └── "Config reset. Run Quick Start to set up again."

End Case
```

---

## Shortcut 2: Pencil Me In (Execute)

This is the main shortcut that runs weekly to generate your event digest.

### Create the Shortcut

1. Open **Shortcuts** app
2. Tap **+** to create new shortcut
3. Rename to **"Pencil Me In"**

---

### Section 1: Load Config

```
Action 1: Text
  └── Content: "Shortcuts/pencil-me-in-config.json"
  └── Set Variable: ConfigPath

Action 2: Get File
  └── Service: iCloud Drive
  └── File Path: ConfigPath
  └── Error: Stop and Respond

Action 3: If (error / no file)
  Action: Show Alert
    └── "No config found. Run 'Pencil Me In Setup' first?"
    └── Buttons: "Run Setup" / "Cancel"
  
  Case: "Run Setup"
    Action: Run Shortcut
      └── Name: "Pencil Me In Setup"
    Action: Stop
  
  Case: "Cancel"
    Action: Stop
End If

Action 4: Get Dictionary from Input
  └── Set Variable: Config
```

---

### Section 2: Extract Config Values

```
Action 5: Get Dictionary Value
  └── Key: location
  └── Set Variable: Location

Action 6: Get Dictionary Value
  └── Key: kids
  └── Set Variable: Kids

Action 7: Get Dictionary Value
  └── Key: streaming_services
  └── Set Variable: StreamingServices

Action 8: Get Dictionary Value
  └── Key: sources
  └── Set Variable: Sources

Action 9: Get Dictionary Value
  └── Key: calendars_to_check
  └── Set Variable: CalendarsToCheck

Action 10: Get Dictionary Value
  └── Key: preferences
  └── Set Variable: Preferences
```

---

### Section 3: Fetch All Sources

```
Action 11: Set Variable: FeedContent = ""
Action 12: Set Variable: FailedSources = []

Action 13: Repeat with Each (Sources)
  └── Set Variable: Source
  
  Action: Get Dictionary Value (name from Source)
    └── Set Variable: SourceName
  Action: Get Dictionary Value (url from Source)
    └── Set Variable: SourceURL
  Action: Get Dictionary Value (type from Source)
    └── Set Variable: SourceType
  Action: Get Dictionary Value (enabled from Source)
    └── Set Variable: SourceEnabled
  
  Action: If (SourceEnabled ≠ false)
    
    Action: Get Contents of URL
      └── URL: SourceURL
      └── Set Variable: Content
      └── Error: Continue
    
    Action: If (error)
      Action: Add to Variable
        └── Variable: FailedSources
        └── Value: SourceName
    Else
      Action: Text
        └── "### [SourceName] ([SourceType])\n[Content]\n\n"
        └── Add to Variable: FeedContent
    End If
    
  End If
  
End Repeat
```

---

### Section 4: Fetch School Calendars

```
Action 14: Set Variable: SchoolContent = ""
Action 15: Set Variable: KidsAges = []

Action 16: Repeat with Each (Kids)
  └── Set Variable: Kid
  
  Action: Get Dictionary Value (name from Kid)
    └── Set Variable: KidName
  Action: Get Dictionary Value (age from Kid)
    └── Set Variable: KidAge
  Action: Get Dictionary Value (school from Kid)
    └── Set Variable: School
  
  Action: Add to Variable
    └── Variable: KidsAges
    └── Value: KidAge
  
  Action: If (School has value)
    Action: Get Dictionary Value (calendar_url from School)
      └── Set Variable: SchoolURL
    Action: Get Dictionary Value (name from School)
      └── Set Variable: SchoolName
    Action: Get Dictionary Value (calendar_type from School)
      └── Set Variable: SchoolType
    
    Action: Get Contents of URL
      └── URL: SchoolURL
      └── Set Variable: SchoolCalContent
      └── Error: Continue
    
    Action: If (no error)
      Action: Text
        └── "### [KidName]'s School: [SchoolName] ([SchoolType])\n[SchoolCalContent]\n\n"
        └── Add to Variable: SchoolContent
    End If
  End If
  
End Repeat
```

---

### Section 5: Get Busy Times

```
Action 17: Get Current Date
  └── Set Variable: Today

Action 18: Adjust Date
  └── Input: Today
  └── Add: 7 days
  └── Set Variable: WeekEnd

Action 19: Find Calendar Events
  └── Filter: 
      - Start Date is between Today and WeekEnd
      - Calendar is in CalendarsToCheck
  └── Sort by: Start Date
  └── Set Variable: BusyEvents

Action 20: Set Variable: BusyTimes = ""

Action 21: Repeat with Each (BusyEvents)
  └── Set Variable: Event
  
  Action: Get Details of Calendar Event
    └── Get: Title
    └── Set Variable: EventTitle
  
  Action: Get Details of Calendar Event
    └── Get: Start Date
    └── Format: "EEE MMM d h:mm a"
    └── Set Variable: EventStart
  
  Action: Get Details of Calendar Event
    └── Get: End Date
    └── Format: "h:mm a"
    └── Set Variable: EventEnd
  
  Action: Text
    └── "- [EventStart] - [EventEnd]: [EventTitle]\n"
    └── Add to Variable: BusyTimes

End Repeat
```

---

### Section 6: Build and Send ChatGPT Prompt

```
Action 22: Format Date
  └── Input: Today
  └── Format: "EEEE, MMMM d, yyyy"
  └── Set Variable: TodayFormatted

Action 23: Get Dictionary Value
  └── Dictionary: Preferences
  └── Key: advance_ticket_weeks
  └── Set Variable: AdvanceWeeks

Action 24: Text
  └── Content:
      """
      You are Pencil Me In, a family event assistant. Today is [TodayFormatted].
      
      ## USER PROFILE
      - Location: [Location]
      - Kids ages: [KidsAges]
      - Streaming services: [StreamingServices]
      
      ## BUSY TIMES THIS WEEK
      [BusyTimes]
      
      ## EVENT SOURCES
      [FeedContent]
      
      ## SCHOOL CALENDARS
      [SchoolContent]
      
      For any source marked as "webpage", extract events from the HTML.
      
      ## TASKS
      
      ### Task 1: School Alerts
      From the school calendars, identify:
      - Days with NO SCHOOL (teacher institutes, holidays, breaks)
      - Early dismissal days
      - School events (concerts, conferences, games)
      Flag these prominently.
      
      ### Task 2: This Week's Events (next 7 days)
      Find events that:
      - Don't conflict with busy times
      - Are appropriate for kids ages [KidsAges]
      - Would interest a family in [Location]
      
      For no-school days, suggest activities to fill the time.
      
      Also recommend:
      - Sports games available on [StreamingServices]
      - New TV show premieres on [StreamingServices]
      
      ### Task 3: Advance Tickets (next [AdvanceWeeks] weeks)
      Find events that:
      - Require advance ticket purchase
      - Typically sell out
      - Are special/limited engagements
      
      ## OUTPUT FORMAT
      Return ONLY valid JSON, no other text:
      {
        "school_alerts": [
          {
            "kid_name": "",
            "school_name": "",
            "date": "YYYY-MM-DD",
            "alert_type": "no_school" | "early_dismissal" | "school_event",
            "description": "",
            "suggested_activity": ""
          }
        ],
        "this_week": [
          {
            "title": "",
            "start": "YYYY-MM-DDTHH:MM:SS",
            "end": "YYYY-MM-DDTHH:MM:SS",
            "location": "",
            "description": "",
            "url": "",
            "category": "Library" | "Theatre" | "Sports" | "TV" | "Community" | "School",
            "source": ""
          }
        ],
        "advance_tickets": [
          {
            "title": "",
            "date": "YYYY-MM-DD",
            "location": "",
            "ticket_url": "",
            "why_advance": "",
            "category": ""
          }
        ]
      }
      """
  └── Set Variable: Prompt

Action 25: Ask ChatGPT
  └── Input: Prompt
  └── Set Variable: AIResponse

Action 26: Get Dictionary from Input
  └── Input: AIResponse
  └── Set Variable: Results
```

---

### Section 7: Process School Alerts

```
Action 27: Get Dictionary Value
  └── Key: school_alerts
  └── Set Variable: SchoolAlerts

Action 28: Set Variable: SchoolAlertText = ""

Action 29: Get Dictionary Value
  └── Dictionary: Preferences
  └── Key: school_reminder_days
  └── Set Variable: SchoolReminderDays

Action 30: Repeat with Each (SchoolAlerts)
  └── Set Variable: Alert
  
  Action: Get Dictionary Value (date from Alert)
    └── Set Variable: AlertDate
  Action: Get Dictionary Value (alert_type from Alert)
    └── Set Variable: AlertType
  Action: Get Dictionary Value (kid_name from Alert)
    └── Set Variable: KidName
  Action: Get Dictionary Value (description from Alert)
    └── Set Variable: AlertDesc
  Action: Get Dictionary Value (suggested_activity from Alert)
    └── Set Variable: SuggestedActivity
  
  Action: If (AlertType = "no_school")
    Action: Text
      └── "⚠️ [AlertDate] - NO SCHOOL ([KidName])\n   [AlertDesc]\n   💡 Suggested: [SuggestedActivity]\n\n"
      └── Add to Variable: SchoolAlertText
    
    Action: Date
      └── Input: AlertDate
      └── Set Variable: AlertDateObj
    
    Action: Adjust Date
      └── Input: AlertDateObj
      └── Subtract: [SchoolReminderDays] days
      └── Set Variable: ReminderDate
    
    Action: Get Dictionary Value
      └── Dictionary: Preferences
      └── Key: reminder_list
      └── Set Variable: ReminderList
    
    Action: Add New Reminder
      └── Title: "No school [AlertDate] ([KidName]) - [AlertDesc]"
      └── Due Date: ReminderDate
      └── List: ReminderList
      └── Notes: "Arrange childcare or activities"
      
  Else If (AlertType = "early_dismissal")
    Action: Text
      └── "⚠️ [AlertDate] - EARLY DISMISSAL ([KidName])\n   [AlertDesc]\n\n"
      └── Add to Variable: SchoolAlertText
  Else
    Action: Text
      └── "📅 [AlertDate] - [AlertDesc] ([KidName])\n\n"
      └── Add to Variable: SchoolAlertText
  End If
  
End Repeat
```

---

### Section 8: Generate ICS for This Week

```
Action 31: Get Dictionary Value
  └── Key: this_week
  └── Set Variable: ThisWeekEvents

Action 32: If (ThisWeekEvents is empty)
  Action: Show Alert
    └── "No events found for this week!"
  Action: (Skip to advance tickets section)
End If

Action 33: Text
  └── """
      BEGIN:VCALENDAR
      VERSION:2.0
      PRODID:-//Pencil Me In//EN
      CALSCALE:GREGORIAN
      METHOD:PUBLISH
      """
  └── Set Variable: ICSContent

Action 34: Repeat with Each (ThisWeekEvents)
  └── Set Variable: Event
  
  Action: Generate UUID
    └── Set Variable: EventUID
  
  Action: Get Dictionary Value (title from Event)
    └── Set Variable: EventTitle
  Action: Get Dictionary Value (start from Event)
    └── Set Variable: EventStart
  Action: Get Dictionary Value (end from Event)
    └── Set Variable: EventEnd
  Action: Get Dictionary Value (location from Event)
    └── Set Variable: EventLocation
  Action: Get Dictionary Value (description from Event)
    └── Set Variable: EventDesc
  Action: Get Dictionary Value (url from Event)
    └── Set Variable: EventURL
  Action: Get Dictionary Value (category from Event)
    └── Set Variable: EventCategory
  
  Action: Format Date
    └── Input: EventStart
    └── Format: "yyyyMMdd'T'HHmmss"
    └── Set Variable: ICSStart
  
  Action: Format Date
    └── Input: EventEnd
    └── Format: "yyyyMMdd'T'HHmmss"
    └── Set Variable: ICSEnd
  
  Action: Get Current Date
    └── Format: "yyyyMMdd'T'HHmmss'Z'"
    └── Set Variable: ICSStamp
  
  Action: Text
    └── """
        BEGIN:VEVENT
        UID:[EventUID]
        DTSTAMP:[ICSStamp]
        DTSTART:[ICSStart]
        DTEND:[ICSEnd]
        SUMMARY:[EventTitle]
        LOCATION:[EventLocation]
        DESCRIPTION:[EventDesc]\\n\\n[EventURL]
        CATEGORIES:[EventCategory]
        END:VEVENT
        """
    └── Add to Variable: ICSContent

End Repeat

Action 35: Text
  └── "END:VCALENDAR"
  └── Add to Variable: ICSContent

Action 36: Format Date
  └── Input: Today
  └── Format: "yyyy-MM-dd"
  └── Set Variable: TodayShort

Action 37: Set Name
  └── Input: ICSContent
  └── Name: "pencil-me-in-[TodayShort].ics"
  └── Set Variable: ICSFile

Action 38: Open File
  └── Input: ICSFile
  (This opens Calendar app with import dialog)
```

---

### Section 9: Process Advance Tickets

```
Action 39: Get Dictionary Value
  └── Key: advance_tickets
  └── Set Variable: AdvanceTickets

Action 40: If (AdvanceTickets is empty)
  Action: (Skip to share section)
End If

Action 41: Count
  └── Input: AdvanceTickets
  └── Set Variable: TicketCount

Action 42: Choose from Menu
  └── Prompt: "Found [TicketCount] events needing advance tickets"
  └── Options:
      - "Show & Add Reminders"
      - "Show Only"
      - "Add Reminders Only"
      - "Skip"

Case: "Show & Add Reminders" or "Show Only"
  
  Action: Set Variable: TicketText = "🎟️ ADVANCE TICKETS NEEDED\n\n"
  
  Action: Repeat with Each (AdvanceTickets)
    └── Set Variable: Ticket
    
    Action: Get Dictionary Value (title from Ticket)
    Action: Get Dictionary Value (date from Ticket)
    Action: Get Dictionary Value (location from Ticket)
    Action: Get Dictionary Value (ticket_url from Ticket)
    Action: Get Dictionary Value (why_advance from Ticket)
    
    Action: Text
      └── "• [title]\n  📍 [location]\n  📅 [date]\n  ⚠️ [why_advance]\n  🎟️ [ticket_url]\n\n"
      └── Add to Variable: TicketText
    
  End Repeat
  
  Action: Quick Look
    └── Input: TicketText

Case: "Show & Add Reminders" or "Add Reminders Only"
  
  Action: Get Dictionary Value
    └── Dictionary: Preferences
    └── Key: reminder_lead_days
    └── Set Variable: LeadDays
  
  Action: Get Dictionary Value
    └── Dictionary: Preferences
    └── Key: reminder_list
    └── Set Variable: ReminderList
  
  Action: Repeat with Each (AdvanceTickets)
    └── Set Variable: Ticket
    
    Action: Get Dictionary Value (title from Ticket)
      └── Set Variable: TicketTitle
    Action: Get Dictionary Value (date from Ticket)
      └── Set Variable: TicketDate
    Action: Get Dictionary Value (ticket_url from Ticket)
      └── Set Variable: TicketURL
    Action: Get Dictionary Value (location from Ticket)
      └── Set Variable: TicketLocation
    
    Action: Date
      └── Input: TicketDate
      └── Set Variable: TicketDateObj
    
    Action: Adjust Date
      └── Input: TicketDateObj
      └── Subtract: [LeadDays] days
      └── Set Variable: ReminderDate
    
    Action: Add New Reminder
      └── Title: "🎟️ Buy tickets: [TicketTitle]"
      └── Due Date: ReminderDate
      └── List: ReminderList
      └── Notes: "[TicketDate] @ [TicketLocation]\n[TicketURL]"
    
  End Repeat
  
  Action: Show Notification
    └── "Created [TicketCount] ticket reminders"

End Case
```

---

### Section 10: Share Events

```
Action 43: Choose from Menu
  └── Prompt: "Share events with family?"
  └── Options:
      - "📤 Share this week's events"
      - "🎟️ Share advance tickets alert"
      - "✓ All done"

Case: "📤 Share this week's events"
  
  Action: (Build list of event titles from ThisWeekEvents)
  
  Action: Choose from List
    └── Prompt: "Which events to share?"
    └── Select Multiple: ON
    └── Set Variable: EventsToShare
  
  Action: Choose from Menu
    └── Prompt: "How to share?"
    └── Options: "Text Message" / "Email" / "Share Sheet"
  
  Case: "Text Message"
    
    Action: Set Variable: MessageText = "Want to join us? 🎭\n\n"
    
    Action: Repeat with Each (EventsToShare)
      └── (Find matching event in ThisWeekEvents)
      └── Set Variable: Event
      
      Action: Text
        └── "• [title]\n  📍 [location]\n  📅 [start formatted]\n  🔗 [url]\n\n"
        └── Add to Variable: MessageText
    End Repeat
    
    Action: Text
      └── "Let me know if you're in!"
      └── Add to Variable: MessageText
    
    Action: Choose from Menu
      └── Prompt: "Include calendar file?"
      └── Options: "Yes" / "No"
    
    Case: "Yes"
      Action: (Generate ICS for just selected events)
        └── Set Variable: ShareICS
    End Case
    
    Action: Select Contact
      └── Select Multiple: ON
      └── Set Variable: Recipients
    
    Action: Send Message
      └── To: Recipients
      └── Body: MessageText
      └── Attachment: ShareICS (if included)
  
  Case: "Email"
    Action: (Similar to text, but use Send Email action)
  
  Case: "Share Sheet"
    Action: Share
      └── Input: MessageText

Case: "🎟️ Share advance tickets alert"
  
  Action: Set Variable: AlertText = "Heads up! 🎟️\n\nThese events might need advance tickets:\n\n"
  
  Action: Repeat with Each (AdvanceTickets)
    Action: Text
      └── "• [title] - [date]\n  📍 [location]\n  🎟️ [ticket_url]\n\n"
      └── Add to Variable: AlertText
  End Repeat
  
  Action: Text
    └── "Want to go together?"
    └── Add to Variable: AlertText
  
  Action: Choose from Menu
    └── Options: "Text Message" / "Email" / "Share Sheet"
  
  Action: (Send via selected method, similar to above)

End Case
```

---

### Section 11: Finish Up

```
Action 44: If (FailedSources is not empty)
  Action: Count
    └── Input: FailedSources
    └── Set Variable: FailedCount
  
  Action: Show Alert
    └── "[FailedCount] sources failed to load. Run Setup > Test Sources to troubleshoot."
End If

Action 45: Get Current Date
  └── Format: ISO 8601
  └── Set Variable: Now

Action 46: Set Dictionary Value
  └── Dictionary: Config
  └── Key: last_run
  └── Value: Now

Action 47: Save File
  └── Input: Config
  └── Path: ConfigPath
  └── Overwrite: ON

Action 48: If (SchoolAlertText is not empty)
  Action: Show Alert
    └── Title: "🏫 School Alerts This Week"
    └── Message: SchoolAlertText
End If

Action 49: Stop
```

---

## Tips for Building

1. **Test incrementally**: Build and test one section at a time before moving on.

2. **Use comments**: Add "Comment" actions to mark sections for easier navigation.

3. **Variable naming**: Be consistent with variable names to avoid confusion.

4. **Error handling**: Always add "Continue on Error" for network requests.

5. **JSON parsing**: The "Get Dictionary from Input" action handles JSON automatically.

6. **Date formatting**: Pay attention to date format strings—they're critical for ICS files.

7. **ChatGPT context**: Keep prompts focused; too much content may hit limits.

## Testing Checklist

### Setup Shortcut
- [ ] Quick Start creates valid config file
- [ ] AI source discovery returns parseable JSON
- [ ] Source testing shows sample events
- [ ] School calendar search works
- [ ] Config saves and loads correctly

### Execute Shortcut
- [ ] Loads config successfully
- [ ] Handles missing config gracefully
- [ ] Fetches all source types (ICS, RSS, webpage)
- [ ] ChatGPT returns valid JSON
- [ ] ICS file opens in Calendar
- [ ] Reminders are created correctly
- [ ] Share via text/email works
- [ ] Failed sources are reported

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues.
