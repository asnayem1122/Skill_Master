# Output Schemas

## researcher_output
~~~json
{
  "status": "ok | insufficient_evidence",
  "environment_pinned": "e.g., C++20 / GCC 14 / Linux or Node 22 / TypeScript 5",
  "findings": [
    {
      "id": "F1",
      "claim": "Clear statement of fact or API behavior",
      "source": "url-or-file-path:line_range",
      "source_tier": "tier1 | tier2 | tier3",
      "version_or_date": "v2.4 / 2026-10",
      "excerpt": "1-3 sentence exact verbatim text from the source preserving context",
      "confidence": "high | medium | low"
    }
  ],
  "gaps": ["specific facts or APIs that could not be found"]
}
~~~

## writer_output
~~~json
{
  "status": "ok | insufficient_evidence",
  "deliverable_path": "path/to/output.md (required if >20 lines, else null)",
  "deliverable_inline": "short text answer (only if <=20 lines, else null)",
  "claim_map": [
    {
      "sentence": "Exact factual sentence from the deliverable",
      "evidence_ids": ["F1", "F3"]
    }
  ]
}
~~~

## coder_output
~~~json
{
  "status": "ok | insufficient_evidence",
  "files_changed": ["path/to/file.cpp"],
  "rollback_ref": "git-stash-ref or backup path",
  "implementation_map": [
    {
      "file_and_symbol": "path/to/file.cpp::functionName",
      "change_description": "What was added or modified",
      "apis_or_patterns_used": ["std::views::filter"],
      "evidence_ids": ["F1", "F2"]
    }
  ],
  "verification_run": {
    "command": "cmake --build build && ctest --output-on-failure",
    "exit_code": 0,
    "passed": true,
    "output_excerpt": "100% tests passed, 0 tests failed"
  }
}
~~~

## verifier_output
~~~json
{
  "verdicts": [
    {
      "item_id": "S1 or file_and_symbol",
      "claim_or_change": "The specific claim or code change checked",
      "evidence_ids": ["F1"],
      "exact_evidence_match": "Verbatim substring from F1 or test runner output",
      "version_and_tier_valid": true,
      "verdict": "supported | unsupported | contradicted",
      "note": "One-line explanation"
    }
  ],
  "locked_items": ["item_ids that passed and must not be modified on retry"],
  "overall": "accept | revise | reject"
}
~~~

## handoff_log
~~~json
{
  "step": 1,
  "from": "researcher",
  "to": "coder",
  "input_ref": ".orchestrator/runs/01/brief.json",
  "output_ref": ".orchestrator/runs/01/research.json",
  "gate": "pass | fail | short_circuit",
  "reason": "All findings have verbatim excerpts and tier1/tier2 sources"
}
~~~
