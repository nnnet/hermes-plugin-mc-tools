# hermes-plugin-mc-tools

External Hermes plugin — Mission Control integration primitives.

## About

A "Mission Control" instance is an external Next.js+SQLite execution
backend that exposes 143 REST endpoints (agents, pipelines, workflows,
cron, etc.) for multi-framework AI orchestration. This plugin ships 16
``mc_*`` tools that let a Hermes chief (or main:manager) delegate heavy
work to MC without pulling in any new Python dependencies.

```
human ─voice──▶  Hermes main:manager      ← single human-facing channel
                      │ chief_spawn(brief)
                      ▼
                 Chief (own kanban board + worker)
                      │
                      ├─ kanban_create — sub-tasks on own board
                      ├─ chief_spawn — sub-chief
                      └─ mc_pipeline_run — heavy workflow in MC
                            │
                            ▼
                      ┌──────────────────────────────────┐
                      │ MC (external execution backend)  │
                      │   /api/pipelines/run             │
                      │   CrewAI / LangGraph / AutoGen   │
                      │   agents inside MC               │
                      └──────────────────────────────────┘
```

The two systems are COMPLEMENTARY:
- **chief** — light in-Hermes coordination, immediate visibility via kanban
- **MC** — multi-framework execution, heavy long-running pipelines

## Tools

| Tool | Purpose |
|---|---|
| `mc_pipeline_run` | Trigger an MC pipeline by name |
| `mc_pipeline_list` | List available pipelines |
| `mc_pipeline_status` | Live status of a run |
| `mc_pipeline_cancel` | Stop a running pipeline |
| `mc_exec_approve_list` | List pending HITL approval gates |
| `mc_exec_approve` | Approve / reject a gate |
| `mc_agents_list` | List MC-side agents |
| `mc_agent_create` | Register a new MC agent |
| `mc_task_list` | List tasks (filter by status/assignee/board) |
| `mc_task_get` | Read one task |
| `mc_task_create` | Create a task |
| `mc_task_update` | Edit a task's fields |
| `mc_task_comment` | Append a comment |
| `mc_task_retry` | Reset failed/blocked → assigned, bumps retry_count (capped) |
| `mc_project_create` | Create an MC project |
| `mc_cost_summary` | Per-project / per-agent spend |

## Configuration

```bash
HERMES_MC_BASE_URL=http://localhost:3000   # no trailing slash
HERMES_MC_API_KEY=<operator-role key from MC web UI>
HERMES_MC_TIMEOUT_SEC=30                   # default; HTTP timeout
HERMES_MC_RETRY_COUNT=3                    # default; per-task retry budget
```

When `HERMES_MC_BASE_URL` is unset, every tool returns a graceful
"MC not configured" error and Hermes stays usable without MC.

## Activate

```yaml
# config.yaml
plugins:
  enabled:
    - mc-tools
```

## Mounting

```yaml
# docker-compose.hermes-core.yml
volumes:
  - ./sources/hermes-external-plugins/mc-tools:/opt/data/plugins/mc-tools:ro
```
