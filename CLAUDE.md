# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

**life_jorney** — proyecto en definición. Ver `INGENIERIA_SW.md` para el documento de ingeniería completo (HU, RF, RNF, arquitectura, UI, patrones).

## Estado

Proyecto nuevo — sin código aún. El stack tecnológico y los comandos de build/test/lint se añadirán aquí una vez definidos en `INGENIERIA_SW.md § 5.2`.

## Guía de trabajo

- Toda decisión técnica relevante debe quedar documentada en `INGENIERIA_SW.md`.
- Ante cualquier duda de alcance, referirse primero a las HU y RF del documento de ingeniería.

## Coding standards

All code generated in this repository — by humans or AI agents — must follow the rules defined in `.claude/instructions.md`. Key mandatory rules:

- Docstrings on every module, class, method, and function (Google style, English).
- Type hints on all function signatures (Python, TypeScript, Dart).
- No PHI in logs, no hardcoded secrets, no real patient data in fixtures.
- English identifiers with `snake_case` / `PascalCase` / `camelCase` per language convention.

See `.claude/instructions.md` for the full guide, including correct/incorrect examples.
