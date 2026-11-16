# OpsPilot

OpsPilot is a small operations intelligence MVP for manufacturing inventory. It exposes product and inventory-risk data through a FastAPI service and includes a Python, Ollama-backed agent that can answer inventory questions from the database.

## Current scope

- Product creation and listing, plus inventory-risk summaries for all stored inventory.
- A callable agent workflow with two tools: look up risk for one SKU, or list all items classified as `HIGH` risk.
- PostgreSQL models for products and inventory. A demand-history model, migration, and sample seeder are present, but no current route, risk calculation, or agent tool reads that history.
- The agent is a Python function, not an endpoint wired into FastAPI. The API and agent use the same database but run as separate entry points.

Risk uses days of stock (`current_stock / daily_demand`): below 5 days is `HIGH`, 5 through 10 is `MEDIUM`, and above 10 is `LOW`. A non-positive demand is treated as `LOW` with infinite days of stock. These thresholds are implemented in `apps/api/app/services/inventory_risk.py`.

## Tech stack

- **Python, FastAPI, Pydantic** – API routes and request/response schemas.
- **SQLAlchemy, Alembic, PostgreSQL, psycopg** – ORM, schema migrations, and persistence.
- **Ollama (`llama3.2:3b`)** – local chat model and function/tool selection in the agent.
- **Docker Compose** – local PostgreSQL service.

## Architecture and agent workflow

The API serves products and computed inventory risk. Separately, `agents/inventory_agent.py` accepts a question, asks Ollama to select from the two inventory tools, runs selected Python functions against PostgreSQL, returns tool results to Ollama, and returns the model's final text. The model does not query the database directly.

See [architecture](docs/architecture.md) and [agent workflow](docs/agent-workflow.md). [Future workflow](docs/future-workflow.md) is a proposal, not part of the MVP.

## Project structure

```text
apps/api/app/          FastAPI app, database setup, models, schemas, routes, and risk service
agents/                Ollama inventory agent
tools/                 Database-backed functions exposed to the agent
migrations/            Alembic environment and schema revisions
docs/                  Architecture and workflow diagrams
docker-compose.yml     Local PostgreSQL service
alembic.ini            Migration configuration and default database URL
```

## Local setup

The repository does not include a Python dependency manifest. These steps install the packages imported by the current code; use Python 3.10 or newer.

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install fastapi uvicorn sqlalchemy 'psycopg[binary]' alembic ollama pytest
   ```

2. Start PostgreSQL. The Compose file creates `opspilot` database/user/password on port `5432`:

   ```bash
   docker compose up -d postgres
   ```

3. The default database URL in the code and `alembic.ini` matches that Compose service. To use a different URL, set `DATABASE_URL` in your shell; the app does not automatically load `.env`:

   ```bash
   export DATABASE_URL='postgresql+psycopg://opspilot:opspilot@localhost:5432/opspilot'
   ```

4. Apply migrations and load the sample products/inventory:

   ```bash
   alembic upgrade head
   python -m apps.api.app.seed
   ```

   To also load the sample demand-history rows for `MTR-4821`, run `python -m apps.api.app.seed_demand`. This data is not currently used by the API or agent.

5. Start the API:

   ```bash
   python -m uvicorn apps.api.app.main:app --reload
   ```

   The health check is `GET /health`; interactive API documentation is at `/docs`. The implemented data endpoints are `GET /products/`, `POST /products/`, and `GET /inventory/risks`.

6. For agent calls, install and start Ollama separately, then fetch the model used in code:

   ```bash
   ollama pull llama3.2:3b
   ```

   From the repository root, open Python and call the function:

   ```python
   from agents.inventory_agent import investigate_inventory_risk

   print(investigate_inventory_risk("What is the inventory risk for SKU SEN-7712?"))
   ```

   The repository does not provide an agent CLI or HTTP endpoint.

## Example questions

With the seeded inventory, the agent can answer questions such as:

- “What is the inventory risk for SKU SEN-7712?”
- “Which products are currently classified as high risk?”
- “How many days of stock does MTR-4821 have, and why is it classified that way?”

The agent grounds inventory facts in tool results. It cannot answer historical-demand trends, create purchase orders, or take actions.

## Limitations and possible next steps

The MVP has no authentication, frontend, agent API endpoint, automated purchasing, or human approval flow. Risk is based on the current `daily_demand` field rather than the stored demand history. The agent handles the tool calls returned in a single model response and does not add a tool result for unknown tool names. Possible future work includes using demand history, exposing the agent through an API, and adding document validation, approval, action, and audit stages; these are not implemented.
