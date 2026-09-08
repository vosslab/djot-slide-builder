# Slide AI agent review

- Local snapshot: `OTHER_REPOS/slide-ai-agent`
- Upstream: [slide-ai-agent](https://github.com/leminhnguyen/slide-ai-agent)
- Local version: 0.1.0
- Content type: Full-stack AI deck-authoring web application
- License found: None; the README's MIT statement is not a license file
- Recommendation: Do not reuse

## What it contains

This project combines FastAPI, React, Vite, LangGraph, OpenAI services, MongoDB, Qdrant, retrieval,
file uploads, image and chart generation, live Marp preview, and multi-format export. It is an
application platform rather than a focused slide converter.

## Reuse assessment

- Ideas: Human review between generated source and export, explicit source selection, provenance,
  and chart assets kept separate from Markdown are reasonable product concepts.
- Code and functions: No license file grants permission to copy the implementation. Its export
  wrapper duplicates narrower local functionality.
- Security: `run_python_code.py` executes supplied Python as an ordinary subprocess with a timeout.
  That is not a security sandbox and must not be reused or run on untrusted material.
- Fit: Network services, databases, persistent server state, JavaScript UI code, and agent
  orchestration contradict the local instructor-owned Python and Djot workflow.

## Decision

Do not adopt, execute, or copy this application. Any future assisted-authoring work should be a
separate, explicitly scoped project with source provenance and real code-execution isolation.
