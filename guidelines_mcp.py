#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KiNoTch Guidelines MCP Server

想定配置:
C:\Users\kinok\PRG\.ai-guidelines\
├─ guidelines_mcp.py
├─ guidelines\
│  ├─ AI_CODING_POLICY.md
│  ├─ SPEC_POLICY.md
│  ├─ UI_UX_POLICY.md
│  └─ USABILITY_POLICY.md
└─ uiux_vibecoding_protocol_pack_v1\
   ├─ 00_START_HERE.md
   ├─ 01_AGENT_PROTOCOL.md
   └─ ...

既定では、このファイル自身が置かれたディレクトリを規約ルートとして使う。
別の場所を使う場合のみ、環境変数 GUIDELINES_ROOT で上書きする。

必要パッケージ:
    py -m pip install "mcp[cli]>=2,<3"

起動:
    py C:\Users\kinok\PRG\.ai-guidelines\guidelines_mcp.py
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from mcp.server import MCPServer


SERVER_NAME = "KiNoTch Guidelines"
SERVER_VERSION = "1.0.0"

SERVER_INSTRUCTIONS = """
このサーバーは、KiNoTchのコーディング・仕様管理・UI/UX規約を提供する読取専用MCPである。
作業種別が分かる場合は、get_guidelines_for_taskで該当規約だけを取得すること。
作業種別が不明な場合だけget_bootstrapを使い、返された案内に従って種別を判定すること。
UI作業では00_START_HERE.mdを入口とし、必要な資料だけを読むこと。UIを実装又は変更した場合は、
変更範囲に応じてget_review_checklistsを使用し、アクセシビリティ及びUIレビューを自己検収すること。
ユーザビリティを扱う場合は、guidelines/USABILITY_POLICY.mdを上位原則として、
uiux_vibecoding_protocol_pack_v1/07_USABILITY_BASELINE.mdの関係するカテゴリだけを参照すること。
実行環境上確認できない項目は、推測で合格とせず未確認として理由を報告すること。
資料の記載とユーザーの明示指示が衝突する場合は、ユーザーの直近の明示指示を優先すること。
このサーバーはファイルを変更しない。
""".strip()

ALLOWED_TOP_LEVEL = (
    "guidelines",
    "uiux_vibecoding_protocol_pack_v1",
)

SUPPORTED_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

MAX_FILE_BYTES = 1_000_000
MAX_RETURN_CHARS = 200_000
MAX_SEARCH_RESULTS = 100

EXPECTED_FILES = (
    "guidelines/AI_CODING_POLICY.md",
    "guidelines/SPEC_POLICY.md",
    "guidelines/UI_UX_POLICY.md",
    "guidelines/USABILITY_POLICY.md",
    "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
    "uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md",
    "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
    "uiux_vibecoding_protocol_pack_v1/03_DECISION_QUESTION_BANK.md",
    "uiux_vibecoding_protocol_pack_v1/04_COMPONENT_RULES.md",
    "uiux_vibecoding_protocol_pack_v1/05_LAYOUT_RULES.md",
    "uiux_vibecoding_protocol_pack_v1/06_ACCESSIBILITY_CHECKLIST.md",
    "uiux_vibecoding_protocol_pack_v1/07_USABILITY_BASELINE.md",
    "uiux_vibecoding_protocol_pack_v1/08_REVIEW_CHECKLIST.md",
    "uiux_vibecoding_protocol_pack_v1/09_HANDOFF_PROMPT.md",
    "uiux_vibecoding_protocol_pack_v1/prompts/COPY_ME_FIRST.txt",
)

BOOTSTRAP_FILES = (
    "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
)

TASK_FILES: dict[str, tuple[str, ...]] = {
    "coding": (
        "guidelines/AI_CODING_POLICY.md",
        "guidelines/SPEC_POLICY.md",
    ),
    "specification": (
        "guidelines/SPEC_POLICY.md",
        "guidelines/AI_CODING_POLICY.md",
    ),
    "new_ui": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md",
        "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/03_DECISION_QUESTION_BANK.md",
        "guidelines/USABILITY_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/07_USABILITY_BASELINE.md",
        "uiux_vibecoding_protocol_pack_v1/04_COMPONENT_RULES.md",
        "uiux_vibecoding_protocol_pack_v1/05_LAYOUT_RULES.md",
        "uiux_vibecoding_protocol_pack_v1/templates/mock_generation.md",
        "guidelines/UI_UX_POLICY.md",
        "guidelines/AI_CODING_POLICY.md",
    ),
    "ui_improvement": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md",
        "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
        "guidelines/USABILITY_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/07_USABILITY_BASELINE.md",
        "uiux_vibecoding_protocol_pack_v1/04_COMPONENT_RULES.md",
        "uiux_vibecoding_protocol_pack_v1/05_LAYOUT_RULES.md",
        "uiux_vibecoding_protocol_pack_v1/06_ACCESSIBILITY_CHECKLIST.md",
        "uiux_vibecoding_protocol_pack_v1/08_REVIEW_CHECKLIST.md",
        "uiux_vibecoding_protocol_pack_v1/templates/ui_repair_prompt.md",
        "guidelines/UI_UX_POLICY.md",
        "guidelines/AI_CODING_POLICY.md",
    ),
    "ui_review": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
        "guidelines/USABILITY_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/07_USABILITY_BASELINE.md",
        "uiux_vibecoding_protocol_pack_v1/06_ACCESSIBILITY_CHECKLIST.md",
        "uiux_vibecoding_protocol_pack_v1/08_REVIEW_CHECKLIST.md",
        "uiux_vibecoding_protocol_pack_v1/templates/review_output.md",
        "guidelines/UI_UX_POLICY.md",
    ),
    "ui_policy": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/03_DECISION_QUESTION_BANK.md",
        "uiux_vibecoding_protocol_pack_v1/templates/question_summary.md",
        "uiux_vibecoding_protocol_pack_v1/project/ui_answers.sample.yaml",
        "uiux_vibecoding_protocol_pack_v1/project/ui_policy.sample.yaml",
        "uiux_vibecoding_protocol_pack_v1/project/ui_config.sample.json",
        "uiux_vibecoding_protocol_pack_v1/schemas/ui_policy.schema.json",
        "uiux_vibecoding_protocol_pack_v1/schemas/ui_config.schema.json",
        "guidelines/UI_UX_POLICY.md",
        "guidelines/USABILITY_POLICY.md",
    ),
    "component_rules": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/04_COMPONENT_RULES.md",
        "uiux_vibecoding_protocol_pack_v1/05_LAYOUT_RULES.md",
        "guidelines/UI_UX_POLICY.md",
    ),
    "ui_config": (
        "uiux_vibecoding_protocol_pack_v1/00_START_HERE.md",
        "uiux_vibecoding_protocol_pack_v1/02_DEFAULT_UI_POLICY.md",
        "uiux_vibecoding_protocol_pack_v1/project/ui_config.sample.json",
        "uiux_vibecoding_protocol_pack_v1/schemas/ui_config.schema.json",
        "guidelines/UI_UX_POLICY.md",
    ),
}

TaskType = Literal[
    "coding",
    "specification",
    "new_ui",
    "ui_improvement",
    "ui_review",
    "ui_policy",
    "component_rules",
    "ui_config",
]

ChecklistType = Literal["accessibility", "ui_review", "all"]


def _guidelines_root() -> Path:
    """規約ルートを決定する。環境変数が無ければ本ファイルの親ディレクトリ。"""
    configured = os.environ.get("GUIDELINES_ROOT", "").strip()
    root = Path(configured) if configured else Path(__file__).resolve().parent
    return root.expanduser().resolve()


ROOT = _guidelines_root()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(SERVER_NAME)

mcp = MCPServer(
    SERVER_NAME,
    version=SERVER_VERSION,
    instructions=SERVER_INSTRUCTIONS,
    log_level="INFO",
)


def _normalise_relative_path(relative_path: str) -> PurePosixPath:
    raw = relative_path.strip().replace("\\", "/")
    if not raw:
        raise ValueError("relative_pathが空です。")

    path = PurePosixPath(raw)

    if path.is_absolute():
        raise ValueError("絶対パスは指定出来ません。規約ルートからの相対パスを指定してください。")
    if ".." in path.parts:
        raise ValueError("親ディレクトリへの移動 '..' は使用出来ません。")
    if not path.parts or path.parts[0] not in ALLOWED_TOP_LEVEL:
        allowed = ", ".join(ALLOWED_TOP_LEVEL)
        raise ValueError(f"許可された先頭ディレクトリは {allowed} です。")

    return path


def _resolve_file(relative_path: str) -> Path:
    rel = _normalise_relative_path(relative_path)
    candidate = (ROOT / Path(*rel.parts)).resolve()

    if not candidate.is_relative_to(ROOT):
        raise ValueError("規約ルート外のパスは使用出来ません。")
    if not candidate.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {rel.as_posix()}")
    if not candidate.is_file():
        raise ValueError(f"ファイルではありません: {rel.as_posix()}")
    if candidate.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"未対応のファイル形式です: {candidate.suffix}")
    if candidate.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(
            f"ファイルが上限 {MAX_FILE_BYTES:,} bytes を超えています: "
            f"{candidate.stat().st_size:,} bytes"
        )

    return candidate


def _resolve_directory(relative_path: str) -> Path:
    rel = _normalise_relative_path(relative_path)
    candidate = (ROOT / Path(*rel.parts)).resolve()

    if not candidate.is_relative_to(ROOT):
        raise ValueError("規約ルート外のパスは使用出来ません。")
    if not candidate.exists():
        raise FileNotFoundError(f"ディレクトリが見つかりません: {rel.as_posix()}")
    if not candidate.is_dir():
        raise ValueError(f"ディレクトリではありません: {rel.as_posix()}")

    return candidate


def _read_text(path: Path) -> tuple[str, str]:
    data = path.read_bytes()

    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"ファイルが上限 {MAX_FILE_BYTES:,} bytes を超えています。")

    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue

    raise ValueError(
        f"文字コードを判定出来ません: {path.relative_to(ROOT).as_posix()} "
        "(UTF-8又はCP932へ変換してください)"
    )


def _iter_guideline_files(base: Path | None = None) -> list[Path]:
    files: list[Path] = []

    scan_roots = [base] if base is not None else [ROOT / name for name in ALLOWED_TOP_LEVEL]

    for scan_root in scan_roots:
        if scan_root is None or not scan_root.exists() or not scan_root.is_dir():
            continue

        for path in scan_root.rglob("*"):
            if (
                path.is_file()
                and path.suffix.lower() in SUPPORTED_SUFFIXES
                and path.stat().st_size <= MAX_FILE_BYTES
            ):
                files.append(path)

    return sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix().casefold())


def _file_metadata(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "suffix": path.suffix.lower(),
        "bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(),
    }


def _combine_files(relative_paths: tuple[str, ...] | list[str]) -> dict[str, Any]:
    documents: list[dict[str, Any]] = []
    missing: list[str] = []
    returned_chars = 0
    truncated = False

    for relative_path in relative_paths:
        try:
            path = _resolve_file(relative_path)
            text, encoding = _read_text(path)
        except (FileNotFoundError, ValueError) as exc:
            missing.append(f"{relative_path}: {exc}")
            continue

        remaining = MAX_RETURN_CHARS - returned_chars
        if remaining <= 0:
            truncated = True
            break

        document_truncated = len(text) > remaining
        returned_text = text[:remaining]
        returned_chars += len(returned_text)
        truncated = truncated or document_truncated

        documents.append(
            {
                **_file_metadata(path),
                "encoding": encoding,
                "truncated": document_truncated,
                "content": returned_text,
            }
        )

        if document_truncated:
            break

    return {
        "root": str(ROOT),
        "documents": documents,
        "missing": missing,
        "total_documents": len(documents),
        "returned_chars": returned_chars,
        "return_limit_chars": MAX_RETURN_CHARS,
        "truncated": truncated,
    }


def _setup_status() -> dict[str, Any]:
    missing = [relative for relative in EXPECTED_FILES if not (ROOT / relative).is_file()]
    existing_top_level = {
        name: {
            "exists": (ROOT / name).exists(),
            "is_directory": (ROOT / name).is_dir(),
        }
        for name in ALLOWED_TOP_LEVEL
    }

    files = _iter_guideline_files()

    return {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "root": str(ROOT),
        "root_exists": ROOT.exists(),
        "top_level": existing_top_level,
        "file_count": len(files),
        "expected_file_count": len(EXPECTED_FILES),
        "missing_expected_files": missing,
        "ready": ROOT.exists() and not missing,
    }


@mcp.tool()
def check_setup() -> dict[str, Any]:
    """
    規約ルート、必須ディレクトリ、主要ファイルの配置状態を確認する。

    MCP接続直後、又はファイルを追加・移動した後の診断に使用する。
    """
    return _setup_status()


@mcp.tool()
def get_bootstrap() -> dict[str, Any]:
    """
    作業種別が未確定な場合に、入口文書と種別判定の案内を取得する。

    種別が分かっている場合はget_guidelines_for_taskを優先する。
    """
    result = _combine_files(BOOTSTRAP_FILES)
    result["setup"] = _setup_status()
    result["usage"] = (
        "UI作業は00_START_HERE.mdで種別を判定し、以後は"
        "get_guidelines_for_taskで必要資料だけを取得してください。"
    )
    result["available_task_types"] = list(TASK_FILES)
    return result


@mcp.tool()
def get_guidelines_for_task(task_type: TaskType) -> dict[str, Any]:
    """
    作業種別に対応する規約・テンプレート・チェックリストをまとめて取得する。

    task_type:
    - coding: 通常の実装・修正
    - specification: 要件定義・仕様作成・仕様変更
    - new_ui: 新規UI作成
    - ui_improvement: 既存UI改善
    - ui_review: コード変更を伴わないUIレビュー
    - ui_policy: UI思想・方針・設定値の策定
    - component_rules: コンポーネント規約作成
    - ui_config: UI設定ファイル作成
    """
    paths = TASK_FILES[task_type]
    result = _combine_files(paths)
    result["task_type"] = task_type
    result["requested_paths"] = list(paths)
    if task_type in {"new_ui", "ui_improvement"}:
        result["follow_up"] = (
            "実装後は get_review_checklists('all') を呼び、"
            "06_ACCESSIBILITY_CHECKLIST.md と 08_REVIEW_CHECKLIST.md を使って"
            "変更範囲に応じた検収を行ってください。"
        )
    return result


@mcp.tool()
def list_guidelines(folder: str = "") -> dict[str, Any]:
    """
    利用可能な規約ファイルを一覧する。

    folderを省略すると全規約を返す。
    例:
    - guidelines
    - uiux_vibecoding_protocol_pack_v1/templates
    """
    if folder.strip():
        base = _resolve_directory(folder)
        files = _iter_guideline_files(base)
    else:
        files = _iter_guideline_files()

    return {
        "root": str(ROOT),
        "folder": folder.strip() or ".",
        "count": len(files),
        "files": [_file_metadata(path) for path in files],
    }


@mcp.tool()
def read_guideline(
    relative_path: str,
    start_line: int = 1,
    end_line: int = 0,
    include_line_numbers: bool = False,
) -> dict[str, Any]:
    """
    指定した規約ファイルを行範囲付きで読む。

    relative_pathは規約ルートからの相対パス。
    end_line=0は最終行までを意味する。
    """
    if start_line < 1:
        raise ValueError("start_lineは1以上にしてください。")
    if end_line < 0:
        raise ValueError("end_lineは0以上にしてください。")
    if end_line and end_line < start_line:
        raise ValueError("end_lineはstart_line以上、又は0にしてください。")

    path = _resolve_file(relative_path)
    text, encoding = _read_text(path)
    lines = text.splitlines()

    start_index = min(start_line - 1, len(lines))
    end_index = len(lines) if end_line == 0 else min(end_line, len(lines))
    selected = lines[start_index:end_index]

    if include_line_numbers:
        rendered = "\n".join(
            f"{line_number}: {line}"
            for line_number, line in enumerate(selected, start=start_index + 1)
        )
    else:
        rendered = "\n".join(selected)

    truncated = False
    if len(rendered) > MAX_RETURN_CHARS:
        rendered = rendered[:MAX_RETURN_CHARS]
        truncated = True

    return {
        **_file_metadata(path),
        "encoding": encoding,
        "total_lines": len(lines),
        "requested_start_line": start_line,
        "requested_end_line": end_line,
        "returned_start_line": start_index + 1 if selected else 0,
        "returned_end_line": start_index + len(selected) if selected else 0,
        "include_line_numbers": include_line_numbers,
        "truncated": truncated,
        "content": rendered,
    }


@mcp.tool()
def search_guidelines(
    query: str,
    max_results: int = 20,
    context_lines: int = 2,
    case_sensitive: bool = False,
) -> dict[str, Any]:
    """
    全規約を全文検索し、該当行と前後文脈を返す。

    完全なquery一致を優先し、一致しない場合も空白区切り語の部分一致を候補化する。
    日本語は通常、探したい語句をそのままqueryへ指定する。
    """
    query = query.strip()
    if not query:
        raise ValueError("queryが空です。")
    if not 1 <= max_results <= MAX_SEARCH_RESULTS:
        raise ValueError(f"max_resultsは1〜{MAX_SEARCH_RESULTS}にしてください。")
    if not 0 <= context_lines <= 10:
        raise ValueError("context_linesは0〜10にしてください。")

    normalized_query = query if case_sensitive else query.casefold()
    terms = [term for term in normalized_query.split() if term]
    if not terms:
        terms = [normalized_query]

    matches: list[dict[str, Any]] = []
    searched_files = 0

    for path in _iter_guideline_files():
        text, _encoding = _read_text(path)
        lines = text.splitlines()
        searched_files += 1

        for index, line in enumerate(lines):
            haystack = line if case_sensitive else line.casefold()

            exact_count = haystack.count(normalized_query)
            matched_terms = [term for term in terms if term in haystack]

            if exact_count:
                score = 100 + exact_count
                match_kind = "exact"
            elif len(terms) > 1 and len(matched_terms) == len(terms):
                score = 70 + len(matched_terms)
                match_kind = "all_terms"
            elif matched_terms:
                score = 20 + len(matched_terms)
                match_kind = "partial"
            else:
                continue

            context_start = max(0, index - context_lines)
            context_end = min(len(lines), index + context_lines + 1)
            snippet = "\n".join(
                f"{line_no}: {lines[line_no - 1]}"
                for line_no in range(context_start + 1, context_end + 1)
            )

            matches.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "line": index + 1,
                    "score": score,
                    "match_kind": match_kind,
                    "matched_terms": matched_terms,
                    "snippet": snippet,
                }
            )

    matches.sort(
        key=lambda item: (
            -int(item["score"]),
            str(item["path"]).casefold(),
            int(item["line"]),
        )
    )

    limited = matches[:max_results]

    return {
        "query": query,
        "case_sensitive": case_sensitive,
        "searched_files": searched_files,
        "total_matches": len(matches),
        "returned_matches": len(limited),
        "max_results": max_results,
        "results": limited,
    }


@mcp.tool()
def get_review_checklists(
    checklist_type: ChecklistType = "all",
) -> dict[str, Any]:
    """
    実装後又はレビュー時に使う検収票を取得する。

    checklist_type:
    - accessibility: アクセシビリティ検収のみ
    - ui_review: UIレビュー検収のみ
    - all: 両方
    """
    mapping = {
        "accessibility": (
            "uiux_vibecoding_protocol_pack_v1/06_ACCESSIBILITY_CHECKLIST.md",
        ),
        "ui_review": (
            "uiux_vibecoding_protocol_pack_v1/08_REVIEW_CHECKLIST.md",
        ),
        "all": (
            "uiux_vibecoding_protocol_pack_v1/06_ACCESSIBILITY_CHECKLIST.md",
            "uiux_vibecoding_protocol_pack_v1/08_REVIEW_CHECKLIST.md",
        ),
    }

    result = _combine_files(mapping[checklist_type])
    result["checklist_type"] = checklist_type
    return result


if __name__ == "__main__":
    logger.info("Starting %s %s; root=%s", SERVER_NAME, SERVER_VERSION, ROOT)
    mcp.run()
