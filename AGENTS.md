# AGENTS.md

Настанови для агентів (і людей), що працюють у цьому репозиторії.

## Що це

askdocs — локальний RAG-інструмент «чат з документацією». Відповідає на питання
по корпусу `.md`, спираючись **тільки** на нього, з посиланням на джерело.
Продуктова мапа — [docs/prd.md](docs/prd.md), контекст проєкту —
[openspec/project.md](openspec/project.md).

## Золоті правила

1. **Реалізуй тільки вимоги зі статусом `accepted`.** Вимоги зі статусом
   `proposed` в [docs/prd.md](docs/prd.md) — записані, але не чіпаються, поки
   власник продукту вручну не перемкне статус. `dropped` — не реалізуються.
2. **Усе — в Docker.** У системний Python хоста нічого не встановлюється.
   Будь-який запуск (`ingest`, `cli`, `sync`, `pytest`, `eval`) — у контейнері,
   напр. `docker compose run --rm app pytest`.
3. **Готовність = зелені тести**, не «здається працює». Критерій завершення
   capability — зелена батарея pytest у контейнері.
4. **Відповідь без джерела = баг.** «Немає в корпусі» — валідна відповідь, не
   помилка.
5. **Не порушуй межі інтерфейсів.** Код над `DocSource` / `Retriever` /
   `LLMProvider` не знає про конкретну реалізацію. Один embedding-провайдер,
   один vector store, одна LLM у v1.
6. **Vector store — окремий сервіс** у docker-compose (не embedded). Тести
   ідемпотентності ganяються проти чистого стану store (фікстура `clean_store`
   дропає колекцію перед кожним тестом).

## Робочий процес (OpenSpec)

Кожен capability проводиться окремим OpenSpec change через цикл:

```
/opsx:propose <name>   # proposal.md + design.md + specs + tasks.md
/opsx:apply <name>     # реалізація по tasks, зелені тести
/opsx:sync <name>      # delta spec -> openspec/specs/<capability>/spec.md
/opsx:archive <name>   # у openspec/changes/archive/
```

Після archive — перемкни відповідні FR у [docs/prd.md](docs/prd.md) на `shipped`
і закомить capability окремим комітом.

## Структура коду

```
askdocs/
  sources.py     # DocSource + LocalMarkdownSource
  chunking.py    # structure-aware розбиття markdown (блоки не ріжуться)
  embeddings.py  # EmbeddingProvider + SentenceTransformersProvider
  store.py       # VectorStore + QdrantStore
  retriever.py   # Retriever + VectorRetriever
  llm.py         # LLMProvider + OpenAICompatibleProvider
  answer.py      # конвеєр відповіді з цитуванням / чесна відмова
  cli.py         # термінальний інтерфейс
  sync.py        # безперервна синхронізація корпусу
  eval.py        # golden set + метрики
tests/           # pytest; tests/corpus — фікстурний ГущоЛіт, tests/golden.yaml
corpus/          # користувацький корпус, монтується у /corpus при `docker compose up`
```

## Команди

```bash
docker compose up                                      # qdrant + sync watcher над ./corpus
docker compose run --rm app pytest                     # уся батарея
docker compose run --rm app python -m askdocs.cli "…"  # питання
docker compose run --rm app python -m askdocs.eval     # звіт метрик
docker compose run --rm app python -m askdocs.ingest <dir>   # ручний ingest
```
