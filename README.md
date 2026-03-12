# Calendesk MCP Server

Connect your [Calendesk](https://calendesk.com) booking platform to Claude, Claude Desktop, Claude Code, and other MCP-compatible AI tools. Manage bookings, customers, employees, services, and view business analytics — all through natural language.

## Prerequisites

- A [Calendesk](https://calendesk.com) account

## Setup

### Claude.ai (recommended)

No installation or API keys needed. Uses OAuth for secure authentication.

1. Go to [Settings → Connectors](https://claude.ai/customize/connectors) in Claude.ai
2. Click **Add custom connector**
3. Enter:
   - **Name:** Calendesk
   - **Remote MCP server URL:** `https://mcp.calendesk.com`
4. Click **Add**
5. Log in with your Calendesk credentials when prompted

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

### Bookings
- `list_bookings` - List bookings/appointments with optional filters
- `get_booking` - Get details of a specific booking by ID
- `create_booking` - Create a new booking/appointment
- `update_booking` - Update an existing booking
- `delete_booking` - Delete a booking
- `get_group_booking` - Get details of a group booking
- `check_event_overlaps` - Check for scheduling conflicts

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
- `list_service_types` - Get all service categories
- `list_products` - Get all products available for sale
- `list_tags` - Get all available tags
- `list_user_groups` - Get all customer groups

### Analytics & Statistics
- `get_statistics` - Get business statistics (booking counts, revenue)
- `get_dashboard_stats` - Get dashboard KPIs (revenue, bookings, customers, cancellations)
- `get_revenue_report` - Get revenue analysis with breakdown by source
- `get_booking_analytics` - Get booking analytics by status, trends, and service
- `get_employee_performance` - Get staff performance comparison
- `get_service_analytics` - Get service popularity metrics
- `get_customer_insights` - Get customer analytics and segments
- `get_booking_patterns` - Get time-based booking patterns and peak hours
- `get_payment_analytics` - Get payment and transaction analytics
- `get_subscription_analytics` - Get subscription metrics and renewal rates
- `get_location_analytics` - Get location and delivery type analytics
- `get_product_analytics` - Get product sales analytics
- `get_revenue_forecast` - Get revenue forecast for next 1-3 months

### Settings & Notifications
- `get_settings` - Get business settings (timezone, currency, company info)
- `get_me` - Get current user profile and employee information
- `send_notification` - Send email, SMS, or push notification

## Examples

### Check today's schedule

**You:** "What does my schedule look like today?"

The assistant calls `list_bookings` with today's date and returns:

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

The assistant calls `get_dashboard_stats` with the date range:

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
