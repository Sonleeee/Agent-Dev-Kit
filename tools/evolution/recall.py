"""
ADK Evolution Database - Contextual Experience Recall (Retriever Strategy Pattern)
Provides conditional, zero-noise 2-aspect recall cards (what_went_wrong + how_to_resolve)
with SQLite In-Query fs_exists() pruning and Time-Decay scoring.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import sqlite3
import sys
from typing import Any

from .connection import get_connection

sys.dont_write_bytecode = True


def _extract_verified_cmd(conn: sqlite3.Connection, trace_id: str | None) -> str | None:
    """Extract the most recent verification command from a trace's acceptance_evidence JSON."""
    if not trace_id:
        return None
    row = conn.execute(
        "SELECT acceptance_evidence FROM traces WHERE id = ? AND outcome = 'SUCCESS'",
        (trace_id,),
    ).fetchone()
    if not row or not row["acceptance_evidence"]:
        return None
    try:
        ev = json.loads(row["acceptance_evidence"])
        cmds = ev.get("verification_commands") or []
        if cmds and isinstance(cmds[-1], dict):
            return cmds[-1].get("command")
    except Exception:
        pass
    return None


def _build_recall_card(
    conn: sqlite3.Connection,
    raw: dict[str, Any],
    strategy_name: str,
) -> dict[str, Any]:
    """Transform a raw friction/graph row into a structured 2-aspect recall card."""
    fp_code = raw.get("fingerprint") or raw.get("friction_name") or "tool_error"
    frict_node_id = f"friction:{fp_code}"

    # Look up skills that resolved this friction via (skill) --[RESOLVES]--> (friction)
    res_rows = conn.execute(
        """
        SELECT s.name AS skill_name, e.hit_count, e.last_trace_id
        FROM graph_edges e
        JOIN graph_nodes s ON s.id = e.source_id
        WHERE e.target_id = ?
          AND e.edge_type = 'RESOLVES'
          AND s.node_type = 'skill'
        ORDER BY e.hit_count DESC, e.last_seen DESC
        LIMIT 3;
        """,
        (frict_node_id,),
    ).fetchall()
    resolving_skills = [r["skill_name"] for r in res_rows]
    best_trace_id = res_rows[0]["last_trace_id"] if res_rows else raw.get("last_trace_id")

    # Fallback: check implementation skills used with the file if no explicit RESOLVES edge yet
    rel_file = raw.get("related_file")
    if not resolving_skills and rel_file:
        used_rows = conn.execute(
            """
            SELECT sk.name AS skill_name
            FROM graph_edges es
            JOIN graph_nodes sk ON sk.id = es.target_id
            WHERE es.source_id = ?
              AND es.edge_type = 'USED_WITH_SKILL'
              AND sk.name NOT IN ('adk-code-review', 'adk-git-content', 'adk-regression-checklist')
            ORDER BY es.hit_count DESC
            LIMIT 2;
            """,
            (f"file:{rel_file}",),
        ).fetchall()
        resolving_skills = [r["skill_name"] for r in used_rows]

    concrete_fix = (raw.get("suggested_fix") or raw.get("friction_summary") or "").strip()
    verified_cmd = _extract_verified_cmd(conn, best_trace_id)
    is_resolved = bool(res_rows or concrete_fix)

    return {
        "strategy": strategy_name,
        "effective_score": float(raw.get("effective_score", 1.0)),
        "is_resolved": is_resolved,
        "what_went_wrong": {
            "error_fingerprint": fp_code,
            "category": raw.get("category") or fp_code,
            "severity": raw.get("severity") or "medium",
            "related_file": rel_file,
            "related_skill": raw.get("related_skill"),
            "symptom": (raw.get("symptom") or raw.get("friction_summary") or fp_code)[:200],
            "hit_count": int(raw.get("hit_count", 1)),
            "last_seen": raw.get("last_seen"),
        },
        "how_to_resolve": {
            "status": "RESOLVED" if is_resolved else "UNRESOLVED",
            "concrete_fix": concrete_fix or "Chưa có mẫu sửa chuẩn — cần kiểm tra kỹ trước khi thay đổi.",
            "resolving_skills": resolving_skills,
            "verified_cmd": verified_cmd,
        },
    }


class RecallStrategy(ABC):
    """Abstract base strategy for retrieving contextual experience cards."""

    name: str = "base"

    @abstractmethod
    def retrieve(
        self,
        conn: sqlite3.Connection,
        request: dict[str, Any],
        min_score: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Retrieve candidate recall cards matching the request."""


class FileGraphRecallStrategy(RecallStrategy):
    """Strategy 1: Graph traversal from touched file paths -> SUFFERED_FROM friction nodes."""

    name = "file_graph"

    def retrieve(
        self,
        conn: sqlite3.Connection,
        request: dict[str, Any],
        min_score: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        files: list[str] = []
        raw_files = request.get("files") or request.get("file") or request.get("target") or []
        if isinstance(raw_files, str):
            files = [raw_files]
        elif isinstance(raw_files, list):
            files = [str(x) for x in raw_files if x]

        clean_files = [
            f.strip().replace("\\\\", "/").replace("\\", "/").strip("/")
            for f in files
            if f and isinstance(f, str)
        ]
        if not clean_files:
            return []

        cards: list[dict[str, Any]] = []
        for cf in clean_files:
            rows = conn.execute(
                """
                SELECT
                    s.name AS related_file,
                    t.name AS fingerprint,
                    t.summary AS friction_summary,
                    e.hit_count,
                    e.last_trace_id,
                    e.last_seen,
                    ROUND(
                        CAST(e.hit_count AS REAL) /
                        (1.0 + 0.1 * MAX(0.0, julianday('now') - julianday(COALESCE(e.last_seen, 'now')))),
                        2
                    ) AS effective_score,
                    (
                        SELECT fp.description FROM friction_points fp
                        WHERE fp.related_file = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS symptom,
                    (
                        SELECT fp.suggested_fix FROM friction_points fp
                        WHERE fp.related_file = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS suggested_fix,
                    (
                        SELECT fp.severity FROM friction_points fp
                        WHERE fp.related_file = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS severity
                FROM graph_edges e
                JOIN graph_nodes s ON s.id = e.source_id
                JOIN graph_nodes t ON t.id = e.target_id
                WHERE s.node_type = 'file'
                  AND e.edge_type = 'SUFFERED_FROM'
                  AND fs_exists(s.name) = 1
                  AND (s.name = ? OR s.name LIKE ?)
                ORDER BY effective_score DESC, e.hit_count DESC
                LIMIT ?;
                """,
                (cf, f"%{cf}", limit),
            ).fetchall()
            for r in rows:
                d = dict(r)
                if float(d.get("effective_score") or 0.0) >= min_score:
                    cards.append(_build_recall_card(conn, d, self.name))
        return cards


class SkillRecallStrategy(RecallStrategy):
    """Strategy 2: Graph traversal from active skills -> SUFFERED_FROM friction nodes."""

    name = "skill_graph"

    def retrieve(
        self,
        conn: sqlite3.Connection,
        request: dict[str, Any],
        min_score: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        raw_skills = request.get("skills") or request.get("skill") or []
        if isinstance(raw_skills, str):
            skills = [raw_skills.strip()]
        elif isinstance(raw_skills, list):
            skills = [str(s).strip() for s in raw_skills if s]
        else:
            skills = []
        if not skills:
            return []

        cards: list[dict[str, Any]] = []
        for sk in skills:
            rows = conn.execute(
                """
                SELECT
                    s.name AS related_skill,
                    t.name AS fingerprint,
                    t.summary AS friction_summary,
                    e.hit_count,
                    e.last_trace_id,
                    e.last_seen,
                    ROUND(
                        CAST(e.hit_count AS REAL) /
                        (1.0 + 0.1 * MAX(0.0, julianday('now') - julianday(COALESCE(e.last_seen, 'now')))),
                        2
                    ) AS effective_score,
                    (
                        SELECT fp.description FROM friction_points fp
                        WHERE fp.related_skill = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS symptom,
                    (
                        SELECT fp.suggested_fix FROM friction_points fp
                        WHERE fp.related_skill = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS suggested_fix,
                    (
                        SELECT fp.related_file FROM friction_points fp
                        WHERE fp.related_skill = s.name AND fp.error_fingerprint = t.name
                        ORDER BY fp.id DESC LIMIT 1
                    ) AS related_file
                FROM graph_edges e
                JOIN graph_nodes s ON s.id = e.source_id
                JOIN graph_nodes t ON t.id = e.target_id
                WHERE s.node_type = 'skill'
                  AND e.edge_type = 'SUFFERED_FROM'
                  AND s.name = ?
                ORDER BY effective_score DESC, e.hit_count DESC
                LIMIT ?;
                """,
                (sk, limit),
            ).fetchall()
            for r in rows:
                d = dict(r)
                rel_f = d.get("related_file")
                if rel_f:
                    exists_row = conn.execute("SELECT fs_exists(?)", (rel_f,)).fetchone()
                    if exists_row and exists_row[0] == 0:
                        d["related_file"] = None
                if float(d.get("effective_score") or 0.0) >= min_score:
                    cards.append(_build_recall_card(conn, d, self.name))
        return cards


class KeywordFtsRecallStrategy(RecallStrategy):
    """Strategy 3: FTS5 search over friction_fts when a free-text query is provided."""

    name = "keyword_fts"

    def retrieve(
        self,
        conn: sqlite3.Connection,
        request: dict[str, Any],
        min_score: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        query = str(request.get("query") or request.get("q") or "").strip()
        if not query:
            return []

        # Sanitize FTS5 query tokens
        tokens = [t for t in query.replace('"', " ").replace("'", " ").split() if len(t) >= 2]
        if not tokens:
            return []
        fts_expr = " OR ".join(f'"{t}"' for t in tokens[:6])

        try:
            rows = conn.execute(
                """
                SELECT
                    fp.category,
                    fp.description AS symptom,
                    fp.severity,
                    fp.related_skill,
                    fp.related_file,
                    COALESCE(fp.error_fingerprint, fp.category) AS fingerprint,
                    fp.suggested_fix,
                    fp.trace_id AS last_trace_id,
                    t.created_at AS last_seen,
                    COUNT(*) OVER (PARTITION BY COALESCE(fp.error_fingerprint, fp.category), fp.related_file) AS hit_count,
                    ROUND(
                        1.0 / (1.0 + 0.1 * MAX(0.0, julianday('now') - julianday(COALESCE(t.created_at, 'now')))),
                        2
                    ) AS effective_score
                FROM friction_fts f
                JOIN friction_points fp ON fp.id = f.rowid
                LEFT JOIN traces t ON t.id = fp.trace_id
                WHERE friction_fts MATCH ?
                  AND (fp.related_file IS NULL OR fs_exists(fp.related_file) = 1)
                ORDER BY f.rank, effective_score DESC
                LIMIT ?;
                """,
                (fts_expr, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            return []

        cards: list[dict[str, Any]] = []
        for r in rows:
            d = dict(r)
            if float(d.get("effective_score") or 0.0) >= min_score:
                cards.append(_build_recall_card(conn, d, self.name))
        return cards


STRATEGIES: list[RecallStrategy] = [
    FileGraphRecallStrategy(),
    SkillRecallStrategy(),
    KeywordFtsRecallStrategy(),
]


def cmd_recall(args: Any = None) -> dict[str, Any]:
    """
    Contextual Experience Recall (Silence-by-Default).
    Only returns cards (`should_inject: True`) when non-expired, existing-file friction matches.
    """
    request: dict[str, Any] = {}
    if isinstance(args, str) and args.strip():
        s = args.strip()
        if "/" in s or "\\" in s or s.endswith((".py", ".ts", ".js", ".md", ".ps1", ".json", ".sql")):
            request = {"files": [s]}
        elif s.startswith(("adk-", "sk-")):
            request = {"skills": [s]}
        else:
            request = {"files": [s], "query": s}
    elif isinstance(args, dict):
        request = dict(args)

    min_score = float(request.get("min_score", 0.35))
    limit = max(1, min(10, int(request.get("limit", 5))))

    with get_connection() as conn:
        # 1. Zero-Daemon In-Query Pruning: remove deleted file nodes (cascades to graph_edges)
        conn.execute("DELETE FROM graph_nodes WHERE node_type = 'file' AND fs_exists(name) = 0;")

        # 2. Run Retriever Strategy Pipeline & deduplicate by (fingerprint, related_file)
        deduped: dict[tuple[str, str], dict[str, Any]] = {}
        for strategy in STRATEGIES:
            for card in strategy.retrieve(conn, request, min_score=min_score, limit=limit):
                w = card["what_went_wrong"]
                key = (w["error_fingerprint"], w.get("related_file") or "")
                if key not in deduped or card["effective_score"] > deduped[key]["effective_score"]:
                    deduped[key] = card

        # 3. Sort: RESOLVED cards with concrete fix first, then by effective_score DESC
        sorted_cards = sorted(
            deduped.values(),
            key=lambda c: (1 if c["is_resolved"] else 0, c["effective_score"]),
            reverse=True,
        )[:limit]

        return {
            "status": "ok",
            "should_inject": len(sorted_cards) > 0,
            "count": len(sorted_cards),
            "min_score": min_score,
            "cards": sorted_cards,
        }
