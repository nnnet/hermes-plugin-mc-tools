"""mc-tools — Mission Control integration primitives.

Exposes 16 ``mc_*`` tools (mc_pipeline_run/list/status/cancel,
mc_exec_approve/_list, mc_agents_list, mc_task_*, mc_project_create,
mc_agent_create, mc_cost_summary) for the Hermes ↔ Mission Control
bridge. Each tool gates on HERMES_MC_BASE_URL — without that env var
the tools surface a clean "MC not configured" error and Hermes stays
usable.

Replaces the in-fork ``tools/mc_tools.py`` + the ``mc_*`` block in
``toolsets._HERMES_CORE_TOOLS`` so future upstream merges of
``toolsets.py`` don't conflict on the MC block.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


_MC_TOOL_NAMES = (
    "mc_pipeline_run", "mc_pipeline_list", "mc_pipeline_status",
    "mc_pipeline_cancel",
    "mc_exec_approve", "mc_exec_approve_list",
    "mc_agents_list",
    "mc_task_list", "mc_task_get", "mc_task_create",
    "mc_task_update", "mc_task_comment", "mc_task_retry",
    "mc_project_create", "mc_agent_create",
    "mc_cost_summary",
)


def register(ctx: Any) -> None:
    """Plugin entry point — called by Hermes plugin loader at startup.

    1. Import ``mc_tools`` so its top-level ``registry.register(...)``
       calls run as side effects.
    2. Extend ``toolsets._HERMES_CORE_TOOLS`` with the 16 mc_* names so
       every composite toolset that references it picks them up.
    """
    try:
        from . import mc_tools  # noqa: F401 — module is the side-effect
    except Exception as exc:
        logger.error("mc-tools: failed to load mc_tools module: %s", exc)
        return

    try:
        import toolsets

        added = 0
        for name in _MC_TOOL_NAMES:
            if name not in toolsets._HERMES_CORE_TOOLS:
                toolsets._HERMES_CORE_TOOLS.append(name)
                added += 1
        logger.info(
            "mc-tools: registered %d tools (%d added to _HERMES_CORE_TOOLS)",
            len(_MC_TOOL_NAMES), added,
        )
    except Exception as exc:
        logger.warning(
            "mc-tools: tools registered but _HERMES_CORE_TOOLS extension "
            "failed (%s) — set enabled_toolsets: [kanban] manually", exc,
        )
