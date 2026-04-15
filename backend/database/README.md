# Database Setup & Management

## seed.py

Initializes MongoDB with comprehensive mock data for development and testing.

### Usage

**Interactive mode (recommended):**
```bash
python3 database/seed.py
```

**Command-line modes:**
```bash
# Reset database and seed with fresh data
python3 database/seed.py --reset

# Preview data without writing to database
python3 database/seed.py --dry-run

# Show help
python3 database/seed.py --help
```

### What Gets Created

| Resource | Count | Details |
|----------|-------|---------|
| Users | 3 | Alice, Bob, Carol with email & Google IDs |
| Surveys | 3 | Customer, Product Features, Employee feedback |
| Questions | 7 | Mixed types: text, rating, multiple choice, checkbox |
| Responses | 5 | From different users (including anonymous) |
| Answers | 13 | Populated across all responses |

### Sample Data

**Users:**
- alice@example.com (Alice Johnson)
- bob@example.com (Bob Smith)  
- carol@example.com (Carol White)

**Survey Types:**
- Customer Satisfaction Survey (rating, text, checkbox questions)
- Product Feature Feedback (multiple choice, text)
- Employee Satisfaction Survey (rating, checkbox)

### Interactive Options

When running `python3 database/seed.py`:

1. **Seed database (reset)** - Clear all data, then seed fresh
2. **Seed database (keep)** - Append new data (does not clear)
3. **Dry run** - Preview what would be created (no write)
4. **Exit** - Cancel

### Prerequisites

- MongoDB running and accessible
- Connection string set in `.env` (defaults to `mongodb://admin:password@localhost:27017`)
- Python dependencies: motor, beanie, python-dotenv

### Example Workflow

```bash
# 1. Start fresh development environment
python3 database/seed.py
# → Select option 1: "Seed database (reset existing data)"

# 2. Preview data before applying
python3 database/seed.py --dry-run

# 3. Update frontend with sample survey IDs from output
# → Use IDs from "Survey IDs for testing" section
```

### Environment Variables

Set in `.env`:
```
DB_CONNECTION_STRING=mongodb://admin:password@localhost:27017
```

Defaults to local MongoDB if not set.

## docker-compose.yml

Docker setup for MongoDB development environment.

### Usage

```bash
# Start MongoDB service
docker-compose up -d

# Stop MongoDB service
docker-compose down

# View logs
docker-compose logs -f
```

## database_manager.py

Core database abstraction layer for direct collection operations when needed.
