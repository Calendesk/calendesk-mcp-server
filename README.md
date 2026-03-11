# Calendesk MCP Server

Connect your [Calendesk](https://calendesk.com) booking platform to Claude, Claude Desktop, Claude Code, and other MCP-compatible AI tools.

## Prerequisites

- A Calendesk account

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
