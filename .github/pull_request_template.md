# Домашнє завдання — Agentic Engineering: Greenfield

## Автор

_(впиши своє справжнє ім'я)_

## Проєкт

**askdocs** — локальний RAG-інструмент «чат з документацією» на Python. Відповідає
на питання по корпусу локальних `.md`, спираючись лише на нього, з посиланням на
джерело; якщо відповіді в корпусі немає — чесно каже про це. Уся система в Docker
(docker-compose): qdrant як окремий vector store, локальний embedding
(`sentence-transformers`), LLM через OpenAI-сумісний API (LM Studio на хості).

## Відео-демо (1–2 хв)

Video: _(посилання на YouTube / Loom / Google Drive)_

## Які практики Agentic Engineering застосовано

- **Специфікації наперед (SDD)** — кожен capability (ingest, retrieve, answer, cli,
  eval, sync, docs) проведено окремим OpenSpec change через цикл
  propose → apply → sync → archive; proposal/design/specs/tasks для кожного.
- **Контекст-інженерія** — статичний контекст у `AGENTS.md`/`CLAUDE.md`,
  `openspec/project.md` і продуктовій мапі `docs/prd.md` зі статусами вимог
  (`accepted`/`proposed`): агент реалізує лише `accepted`, `proposed` не чіпає.
- **Цикли (loop engineering)** — усі 6 capability прогнано автономним циклом
  (реалізація → тести → sync spec → archive → окремий git-коміт), а не покроковим
  ручним промптингом.
- **Верифікація замість «здається працює»** — pytest у контейнері (готовність
  capability = зелені тести); eval з golden set по домену ГущоЛіт: retrieval
  hit-rate і anti-hallucination refusal-rate.
- **Архітектурні межі** — три інтерфейси (`DocSource`, `Retriever`, `LLMProvider`),
  над якими код не залежить від реалізації.
- **Інструменти** — Claude Code, OpenSpec CLI, Docker/qdrant, LM Studio.

## (Опційно) Посилання на код

Код у цьому ж репозиторії.

---

### Чекліст

- [ ] Вказано справжнє ім'я
- [ ] Додано посилання на відео-демо (1–2 хв)
- [ ] Описано застосовані практики Agentic Engineering
- [ ] Результат робочий і доведений до кінця
