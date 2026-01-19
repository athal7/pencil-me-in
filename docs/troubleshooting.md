# Troubleshooting

Common issues and how to fix them.

## Setup Issues

### "No config found" Error

**Problem**: When running "Pencil Me In", you get an error about missing config.

**Solution**: Run "Pencil Me In Setup" first and complete the Quick Start wizard.

---

### AI Source Discovery Returns No Results

**Problem**: When searching for event sources, ChatGPT returns nothing or an error.

**Solutions**:
1. Check your internet connection
2. Try a more specific location (e.g., "Libertyville, IL" instead of just "IL")
3. Try different source types (Libraries often have better feeds than community events)
4. Add sources manually if AI can't find them

---

### Can't Select Calendars

**Problem**: The calendar picker shows no calendars or is missing some.

**Solutions**:
1. Make sure Shortcuts has Calendar access (Settings → Shortcuts → Calendars)
2. Check that your calendars are synced (Settings → Calendar → Accounts)
3. iCloud calendars may take time to sync

---

## Execution Issues

### Source Fetch Failed

**Problem**: One or more sources fail to load when running Pencil Me In.

**Solutions**:
1. Run Setup → Test Sources to see which ones are broken
2. Check if the website is down (try the URL in Safari)
3. The feed URL may have changed - search for a new one
4. Remove broken sources and find alternatives

---

### ChatGPT Not Responding

**Problem**: The shortcut hangs or times out during AI processing.

**Solutions**:
1. Check your internet connection
2. Try running again - ChatGPT may have been temporarily overloaded
3. Make sure ChatGPT is enabled in Settings → Shortcuts
4. If you have too many sources, try disabling some to reduce the prompt size

---

### ICS File Won't Open

**Problem**: The calendar file doesn't open or shows an error.

**Solutions**:
1. Make sure Calendar app is installed and working
2. Check that the ICS file isn't empty (if no events were found)
3. Try opening the file manually from Files app
4. Restart the Calendar app and try again

---

### Reminders Not Created

**Problem**: Ticket or school reminders aren't appearing.

**Solutions**:
1. Check Shortcuts has Reminders access (Settings → Shortcuts → Reminders)
2. Verify the correct Reminders list exists
3. Check the Reminders app - they may be in a different list
4. Run Setup → Reminder Settings to reconfigure

---

### Share Fails to Send

**Problem**: Text or email sharing doesn't work.

**Solutions**:
1. Make sure Messages/Mail app is set up
2. Check that contacts are accessible to Shortcuts
3. Try using the Share Sheet option instead
4. Verify you have cellular/internet connection

---

## School Calendar Issues

### School Calendar Not Found

**Problem**: AI can't find your school's calendar.

**Solutions**:
1. Search for the district calendar instead of individual school
2. Check the school website manually for a calendar link
3. Look for "Subscribe" or "Add to Calendar" buttons on school site
4. Add the URL manually if you can find it

---

### Wrong School Events Showing

**Problem**: Events from wrong school or irrelevant events appear.

**Solutions**:
1. Make sure you've assigned the calendar to the correct child
2. The calendar may include district-wide events - this is normal
3. Check if you accidentally added the same calendar twice

---

## Config Issues

### Config File Corrupted

**Problem**: Shortcuts crash or show strange errors.

**Solution**: Reset the config:
1. Run Setup → View/Reset Config → Reset Config
2. Run Quick Start again to reconfigure

---

### Settings Not Saving

**Problem**: Changes made in Setup don't persist.

**Solutions**:
1. Make sure iCloud Drive is enabled and synced
2. Check available iCloud storage
3. Wait a moment for sync before closing Shortcuts
4. Try running Setup again

---

## Performance Issues

### Shortcut Runs Slowly

**Problem**: Pencil Me In takes a long time to complete.

**Solutions**:
1. Reduce the number of sources (fewer = faster)
2. Prefer ICS/RSS feeds over webpage scraping
3. Webpage sources require AI parsing which is slower
4. Check internet connection speed

---

### Too Many Events

**Problem**: The digest has too many events to be useful.

**Solutions**:
1. Add more calendars to conflict checking
2. Be more specific about kids' ages
3. Remove sources that aren't relevant
4. AI should prioritize family-friendly events automatically

---

## Getting Help

If you're still having issues:

1. **Check the config**: Run Setup → View Config to see current settings
2. **Test sources**: Run Setup → Test Sources to verify feeds work
3. **Start fresh**: Reset config and run Quick Start again
4. **Open an issue**: [GitHub Issues](https://github.com/athal7/pencil-me-in/issues)

When reporting an issue, include:
- iOS/macOS version
- What you were trying to do
- The error message (if any)
- Which sources you have configured
