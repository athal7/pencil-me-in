# Setup Guide

A detailed walkthrough for setting up Pencil Me In.

## Before You Start

Make sure you have:
- iPhone/iPad with iOS 17+ or Mac with Sonoma+
- Shortcuts app (comes pre-installed)
- An internet connection
- ChatGPT enabled in Shortcuts (Settings → Shortcuts → ChatGPT)

## Step 1: Download the Shortcuts

Visit [athal7.github.io/pencil-me-in](https://athal7.github.io/pencil-me-in) and download both shortcuts:

1. **Pencil Me In Setup** - Tap "Get Pencil Me In Setup"
2. **Pencil Me In** - Tap "Get Pencil Me In"

When prompted, tap "Add Shortcut" for each one.

## Step 2: Run Setup

Open the Shortcuts app and tap **Pencil Me In Setup**.

Select **🚀 Quick Start** to begin the configuration wizard.

## Step 3: Enter Your Location

When prompted, enter your city and state:

```
Where do you live? (city, state)
> Libertyville, IL
```

This helps the AI find local event sources and filter regional content.

## Step 4: Add Your Kids

Enter your children's ages, separated by commas:

```
Kids ages? (comma-separated, or 'none')
> 8, 11
```

This is used to:
- Filter age-appropriate events
- Match school calendars to the right child later

If you don't have kids, enter `none`.

## Step 5: Select Streaming Services

Pick all the streaming services you have access to:

```
☑️ ABC
☑️ Peacock
☐ Netflix
☐ Disney+
...
```

Select multiple by tapping each one, then tap "Done".

The AI may suggest regional services based on your location (like local sports networks). You can add those too.

## Step 6: Find Event Sources

When asked "Find local event sources now?", select **Yes, find sources**.

Choose the types of events you're interested in:

```
☑️ Libraries
☑️ Theatres & Venues
☑️ Community Events
☑️ Kids Activities
☐ Sports
```

The AI will search for calendar feeds in your area. This may take 15-30 seconds.

You'll see results like:

```
Found 5 potential sources:

☑️ Vernon Area Public Library
   ✅ ICS feed • Sample: "Storytime Jan 20"

☑️ Cook Memorial Library  
   🌐 Webpage • Sample: "Chess Club Jan 22"

☑️ Genesee Theatre
   ✅ RSS feed • Sample: "Comedy Night Jan 25"
```

Select the sources you want to add and tap "Add Selected".

### Understanding Source Types

- **✅ ICS feed**: Best option - direct calendar subscription
- **✅ RSS feed**: Good option - event listings that can be parsed
- **🌐 Webpage**: Fallback - AI will extract events from HTML (slower, less reliable)

## Step 7: Add School Calendars

After adding event sources, you can add school calendars for each child.

Go to **📅 Event Sources** → **🏫 School Calendars** → **Add School Calendar**.

Select which child the calendar is for, then enter the school or district name:

```
School or district name:
> Libertyville District 70
```

The AI will search for the calendar. If found, you'll see sample events:

```
Found: District 70 Official Calendar
Sample events:
• Jan 24 - Teacher Institute Day (No School)
• Feb 17 - Presidents Day (No School)
```

Tap "Add" to add the calendar.

## Step 8: Select Conflict Calendars

Choose which of your existing calendars to check for conflicts:

```
☑️ Work
☑️ Family
☑️ Personal
☐ Holidays
```

Events that overlap with your busy times on these calendars will be filtered out.

## Step 9: Configure Reminders

Set how many days before an event you want to be reminded to buy tickets:

```
Days before event to remind about tickets?
> 14
```

Then select which Reminders list to use:

```
○ Reminders
○ Shopping
○ Family
```

School day-off reminders are automatically set to 7 days in advance.

## Step 10: Review and Finish

You'll see a summary of your configuration:

```
✅ Setup Complete!

Location: Libertyville, IL
Kids: 8, 11
Streaming: 2 services
Sources: 4 feeds configured
Checking: 3 calendars
```

You can either:
- **Run Now** - Get your first event digest immediately
- **Done** - Exit and run later

## Running Pencil Me In

Now that setup is complete, run **Pencil Me In** to get your weekly digest.

The shortcut will:
1. Fetch all your configured sources
2. Check your calendar for conflicts
3. Process everything with AI
4. Show school alerts (days off, early dismissals)
5. Open an ICS file to add events to your calendar
6. Show advance ticket recommendations
7. Offer to share events with family

## Making Changes Later

Run **Pencil Me In Setup** anytime to:
- Change your location or kids' ages
- Add or remove streaming services
- Find new event sources
- Add more school calendars
- Test if sources are still working
- View or reset your configuration

## Next Steps

- [Set up weekly automation](automation.md) to run automatically every Sunday
- [Troubleshooting](troubleshooting.md) if you run into issues
