# Calendesk MCP Server

Connect your [Calendesk](https://calendesk.com) booking platform to Claude, Claude Desktop, Claude Code, and other MCP-compatible AI tools. Manage bookings, customers, employees, services, and view business analytics — all through natural language. 32 tools, OAuth sign-in, no data leaves your Calendesk account.

## Prerequisites

- A [Calendesk](https://calendesk.com) account

## Setup

### Claude.ai (recommended)

No installation or API keys needed. Uses OAuth for secure authentication.

1. Go to [Settings → Connectors](https://claude.ai/customize/connectors) in Claude.ai
2. Click **Add custom connector**
3. Enter:
   - **Name:** Calendesk
   - **Remote MCP server URL:** `https://claude.calendesk.com`
4. Click **Add**
5. Log in with your Calendesk credentials when prompted (OAuth — no API keys to copy)

### Claude Desktop

Add to your config file (`~/.config/claude/claude_desktop_config.json` on macOS/Linux, `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
    "mcpServers": {
        "calendesk": {
            "url": "https://mcp.calendesk.com",
            "headers": {
                "X-Api-Key": "your-api-key",
                "X-Tenant": "your-tenant-id"
            }
        }
    }
}
```

Generate your API key in **Admin Panel → Settings → API**.

### Claude Code

```bash
claude mcp add calendesk https://mcp.calendesk.com \
  --transport http \
  --header "X-Api-Key: your-key" \
  --header "X-Tenant: your-tenant"
```

### Other MCP clients (STDIO proxy)

For clients that don't support HTTP transport:

```bash
pip install calendesk-mcp-server
# or: uvx calendesk-mcp-server
```

```json
{
    "mcpServers": {
        "calendesk": {
            "command": "uvx",
            "args": ["calendesk-mcp-server"],
            "env": {
                "CALENDESK_API_KEY": "your-api-key",
                "CALENDESK_TENANT": "your-tenant-id"
            }
        }
    }
}
```

## Supported Tools

### Events & Bookings
- `list_events` - List calendar events (bookings, blocks/vacation, group bookings) with filters
- `get_booking` - Get details of a specific booking by ID
- `create_booking` - Create a new booking/appointment
- `update_booking` - Update an existing booking
- `delete_booking` - Delete a booking
- `get_group_booking` - Get details of a group booking
- `check_event_overlaps` - Check for scheduling conflicts
- `get_unavailable_slot` - Get details of a block/vacation slot
- `create_unavailable_slot` - Create a block/vacation for an employee
- `update_unavailable_slot` - Update a block/vacation slot
- `delete_unavailable_slot` - Delete a block/vacation slot

### Customers
- `search_users` - Search customers by name, email, or phone
- `get_user` - Get customer details by ID
- `list_users` - List all customers with optional filtering
- `create_user` - Create a new customer
- `update_user` - Update customer information
- `delete_user` - Delete a customer

### Employees
- `list_employees` - List all employees/staff members
- `get_employee` - Get employee details
- `delete_employee` - Delete an employee

### Services & Availability
- `list_services` - List all available services
- `get_service` - Get service details including duration, price, and locations
- `get_available_slots` - Get available time slots for booking
- `list_availability` - Get availability schedules/working hours
- `get_availability` - Get a specific availability schedule
- `list_service_types` - Get all service categories with their services
- `list_products` - Get all products available for sale
- `list_tags` - Get all available tags

### Analytics & Statistics
- `get_stats` - Business analytics: dashboard KPIs, revenue, bookings, employee performance, services, customers, patterns, payments, subscriptions, locations, products, forecast. Use `type` parameter to select report.

### Settings & Notifications
- `get_settings` - Get business settings (timezone, currency, company info)
- `get_me` - Get current user profile and employee information
- `send_notification` - Send email, SMS, or push notification

## Permissions and access

Access mirrors your Calendesk role and permissions — the connector can only do what your own Calendesk user can do in the admin panel. An employee who connects their account sees exactly what they'd see when they log in, and nothing more.

- **Read tools** (listing, viewing, search, analytics) run without extra prompts.
- **Write tools** (create/update/delete bookings, customers, and blocks; send notifications) are marked as destructive, so Claude asks for your confirmation before each one.

If your email belongs to more than one Calendesk company, you choose which one to connect during sign-in. Every tool call is scoped to that single tenant.

## Data handling and security

- **First-party only.** Every tool call goes to Calendesk's own API over HTTPS. No third-party services are involved, and no data is sold or shared.
- **Your account data only.** The server reads and writes bookings, customers, employees, services, settings, and analytics within your Calendesk account. It never touches data outside your tenant.
- **OAuth, no shared keys.** Claude.ai connects with OAuth 2.1 (authorization code + PKCE, with Dynamic Client Registration). Access and refresh tokens are issued by Calendesk and used only to call the Calendesk API on your behalf. Self-hosted setups use an API key and tenant id you generate yourself.
- **No conversation storage.** The server processes each tool call and returns the result. It does not store, log, or forward your conversation, chat history, or messages.
- **You stay in control.** Disconnect the connector at any time from Claude.ai Settings → Connectors, or revoke the API key in your Calendesk admin panel.

Data collection and retention are described in the [Calendesk Privacy Policy](https://calendesk.com/privacy-policy).

## Examples

### Check today's schedule

**You:** "What does my schedule look like today?"

The assistant calls `list_events` with today's date and returns:

> You have 4 appointments today:
>
> | Time | Service | Customer | Status |
> |------|---------|----------|--------|
> | 09:00–10:00 | Haircut | Maria Kowalska | Approved |
> | 10:30–11:30 | Hair Coloring | Anna Wiśniewska | Approved |
> | 13:00–14:00 | Haircut | Jan Nowak | Approved |
> | 15:00–16:00 | Beard Trim | Tomasz Zieliński | Approved |

### Find available slots and book an appointment

**You:** "When can I schedule a 60-minute consultation with Dr. Kowalski next week?"

The assistant calls `get_available_slots` for the service and employee, then responds:

> Dr. Kowalski has these openings next week:
>
> **Monday:** 09:00, 11:00, 14:00
> **Tuesday:** 10:00, 13:00, 15:00
> **Thursday:** 09:00, 11:00
>
> Would you like me to book one of these?

**You:** "Book Monday at 11:00 for customer anna@example.com"

The assistant calls `search_users` to find the customer, then `check_event_overlaps` to verify no conflicts, and finally `create_booking`:

> Booking confirmed:
> - **Service:** Consultation (60 min)
> - **Employee:** Dr. Kowalski
> - **Customer:** Anna Wiśniewska (anna@example.com)
> - **When:** Monday, March 17 at 11:00–12:00
> - **Booking ID:** #4521

### View business performance

**You:** "How did the business do last month compared to the month before?"

The assistant calls `get_stats` (dashboard report) with the date range:

> **February 2026 vs January 2026:**
>
> | Metric | February | Change |
> |--------|----------|--------|
> | Revenue | €12 500 | +8.5% |
> | Bookings | 285 | +12 |
> | New customers | 18 | +5 |
> | Cancellation rate | 3.5% | −0.8pp |
>
> Revenue is trending up, driven mainly by an increase in Hair Coloring bookings (+22%).

### Search for a customer

**You:** "Find me the contact info for customer Kowalska"

The assistant calls `search_users`:

> Found 2 matches:
>
> 1. **Maria Kowalska** — maria@example.com, +48 512 345 678 (last visit: March 5)
> 2. **Ewa Kowalska** — ewa.k@example.com, +48 601 234 567 (last visit: February 12)

### Send a notification

**You:** "Send Maria Kowalska an email reminder about her appointment tomorrow"

The assistant calls `send_notification`:

> Email sent to Maria Kowalska (maria@example.com) with a reminder about her Haircut appointment tomorrow at 09:00.

## Environment Variables (STDIO mode only)

| Variable | Required | Description |
|----------|----------|-------------|
| `CALENDESK_API_KEY` | Yes | API key from Calendesk admin panel |
| `CALENDESK_TENANT` | Yes | Your tenant ID |
| `CALENDESK_GATEWAY_URL` | No | Gateway URL (defaults to `https://mcp.calendesk.com`) |

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/calendesk/calendesk-mcp-server.git
   cd calendesk-mcp-server
   ```

2. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your CALENDESK_API_KEY and CALENDESK_TENANT
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Start the MCP Inspector (requires Node.js):
   ```bash
   mcp dev calendesk_mcp/server.py:mcp
   ```
   Opens a web UI at `http://localhost:6274` where you can test tools interactively.

## Privacy Policy

[Calendesk Privacy Policy](https://calendesk.com/privacy-policy)

## Support

For questions or issues with the MCP server integration, contact us at **support@calendesk.com**.
