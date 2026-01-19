# Weekly Automation Setup

Set up Pencil Me In to run automatically every week so you always have a fresh event digest.

## Recommended: Sunday Morning

Running on Sunday morning gives you time to plan the week ahead and share events with family.

## Setup Instructions

### On iPhone/iPad

1. Open the **Shortcuts** app
2. Tap the **Automation** tab at the bottom
3. Tap **+** in the top right
4. Select **Create Personal Automation**
5. Choose **Time of Day**
6. Set the time (e.g., **9:00 AM**)
7. Under "Repeat", select **Weekly**
8. Choose **Sunday** (or your preferred day)
9. Tap **Next**
10. Tap **Add Action**
11. Search for **Run Shortcut**
12. Tap **Shortcut** and select **Pencil Me In**
13. Tap **Next**
14. **Turn OFF** "Ask Before Running" (so it runs automatically)
15. Tap **Done**

### On Mac

1. Open the **Shortcuts** app
2. Click **Automation** in the sidebar
3. Click **+** to create new automation
4. Select **Time of Day**
5. Configure the schedule (Sunday 9:00 AM)
6. Add the **Run Shortcut** action
7. Select **Pencil Me In**
8. Disable "Ask Before Running"

## What Happens When It Runs

1. Fetches all your configured event sources
2. Checks your calendar for conflicts
3. Sends data to ChatGPT for processing
4. Opens an ICS file with this week's events
5. Shows advance ticket alerts
6. Creates reminders for tickets and school days off

## Notifications

When the automation runs, you'll see:
- A notification that the shortcut is running
- The Calendar app will open with an import dialog for the events
- A Quick Look window with advance ticket information

## Tips

### Run When You're Available
Choose a time when you're typically free to review the results and add events to your calendar.

### Keep Phone Unlocked
Some Shortcut actions require the device to be unlocked. If you run it first thing in the morning, unlock your phone first.

### Wi-Fi Connection
Make sure you have a good internet connection since the shortcut needs to fetch calendar feeds and call ChatGPT.

## Troubleshooting

### Automation Didn't Run

- Check that "Ask Before Running" is **OFF**
- Verify the automation is enabled (not grayed out)
- Make sure the shortcut hasn't been renamed or deleted

### Shortcut Errors

If the automation fails, run "Pencil Me In" manually to see the error. Common issues:
- No internet connection
- Config file missing (run Setup again)
- Source URL no longer working (run Setup → Test Sources)

## Alternative Triggers

You can also run Pencil Me In:

- **Manually**: Just tap the shortcut when you want a digest
- **From Siri**: Say "Hey Siri, Pencil Me In"
- **From Home Screen**: Add the shortcut to your home screen
- **From Widget**: Add Shortcuts widget to see it at a glance
