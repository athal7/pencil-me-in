# ✏️ Pencil Me In

**Find family events that actually fit your schedule.**

Pencil Me In is a pair of Apple Shortcuts that helps busy parents discover local events, check for calendar conflicts, and coordinate with family—all powered by AI.

## 📲 Get the Shortcuts

**[athal7.github.io/pencil-me-in](https://athal7.github.io/pencil-me-in)** — Mobile-friendly download page

## Features

- **Local Events**: Libraries, theatres, community centers—discovered automatically for your area
- **School Calendars**: Track days off, early dismissals, and school events for each kid
- **Conflict-Free**: Only suggests events that fit your actual schedule
- **Sports & Streaming**: Games and premieres on your streaming services
- **Advance Tickets**: Alerts for events that need early booking (12-week lookahead)
- **Reminders**: Automatic reminders for tickets and school days off (1 week notice)
- **Share with Family**: Text or email events to coordinate, with optional calendar attachments

## Quick Start

1. **Download both shortcuts** from [athal7.github.io/pencil-me-in](https://athal7.github.io/pencil-me-in)

2. **Run "Pencil Me In Setup"** and choose **Quick Start**
   - Enter your location
   - Add your kids and their schools
   - Select your streaming services
   - Let AI find local event sources
   - Pick which calendars to check for conflicts

3. **Run "Pencil Me In"** to get your weekly digest
   - Events are added to your calendar
   - Advance tickets shown with reminder option
   - Share events with family via text or email

## Requirements

- iOS 17+ or macOS Sonoma+
- Shortcuts app
- ChatGPT enabled in Shortcuts (uses Apple's built-in integration)
- Calendar access
- Reminders access (optional, for ticket/school reminders)

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         PENCIL ME IN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Setup (once)              Execute (weekly)                     │
│  ┌──────────────┐          ┌──────────────┐                     │
│  │ • Location   │          │ • Fetch feeds│                     │
│  │ • Kids/School│   ───►   │ • Check busy │                     │
│  │ • Streaming  │ config   │ • AI process │                     │
│  │ • Sources    │          │ • Output ICS │                     │
│  │ • Calendars  │          │ • Reminders  │                     │
│  └──────────────┘          │ • Share      │                     │
│         │                  └──────────────┘                     │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                    │
│  │   iCloud: pencil-me-in-config.json      │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Source Discovery

When you run "Find Sources" in Setup, AI searches for calendar feeds in your area:

- **ICS feeds** (best): Direct calendar subscriptions from libraries, venues
- **RSS feeds**: Event listings that can be parsed
- **Webpages** (fallback): AI extracts events from HTML when no feed exists

### School Calendars

Add a school calendar for each child. The shortcut will:
- Flag days off and early dismissals in your digest
- Create reminders 1 week before days off
- Include school events (concerts, conferences) in recommendations

### Conflict Checking

Events are checked against your selected calendars. Only events that fit your actual free time are suggested.

## Weekly Automation

Set up automatic Sunday morning digests:

1. Open **Shortcuts** app
2. Go to **Automation** tab
3. Tap **+** → **Create Personal Automation**
4. Choose **Time of Day** → Sunday, 9:00 AM
5. Add action: **Run Shortcut** → **Pencil Me In**
6. Disable "Ask Before Running"

See [docs/automation.md](docs/automation.md) for detailed instructions.

## Documentation

- [Setup Guide](docs/setup-guide.md) - Detailed walkthrough
- [Automation](docs/automation.md) - Weekly trigger setup
- [Troubleshooting](docs/troubleshooting.md) - Common issues and fixes

## Configuration

Your config is stored in iCloud at:
```
iCloud Drive/Shortcuts/pencil-me-in-config.json
```

See [schema/config-schema.json](schema/config-schema.json) for the full schema.

## Privacy

- All processing happens on-device via Apple's Shortcuts + ChatGPT integration
- Your config stays in your personal iCloud
- Calendar data is only used locally for conflict checking
- No data is sent to external servers (except ChatGPT for AI processing)

## Contributing

Found a bug or have an idea? Open an issue!

## License

MIT License - see [LICENSE](LICENSE)
