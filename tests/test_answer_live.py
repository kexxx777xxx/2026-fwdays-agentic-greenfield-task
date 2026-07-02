"""End-to-end smoke: retriever + real LLM (LM Studio on the host).

Proves the wiring only; pipeline logic is covered by fakes in test_answer.py.
Skips automatically when the LLM endpoint is unreachable, so the suite stays
green on machines without LM Studio.
"""

import os
from pathlib import Path

import httpx
import pytest

from askdocs.answer import answer_question
from askdocs.ingest import ingest
from askdocs.llm import DEFAULT_BASE_URL, OpenAICompatibleProvider
from askdocs.retriever import VectorRetriever
from askdocs.sources import LocalMarkdownSource

CORPUS_DIR = Path(__file__).parent / "corpus"


def _llm_available() -> bool:
    base_url = os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    try:
        return httpx.get(f"{base_url}/models", timeout=3).status_code == 200
    except httpx.HTTPError:
        return False


pytestmark = pytest.mark.skipif(not _llm_available(), reason="LLM endpoint unreachable")


@pytest.fixture
def retriever(clean_store, embedder):
    ingest(LocalMarkdownSource(CORPUS_DIR), embedder, clean_store)
    return VectorRetriever(embedder, clean_store)


def test_corpus_question_answered_with_source(retriever):
    answer = answer_question(
        "Який сорт кавової гущі заборонений як паливо?", retriever, OpenAICompatibleProvider()
    )

    assert answer.found
    assert answer.text
    assert "dvyhun/palyvo.md" in answer.sources


def test_out_of_corpus_question_refused(retriever):
    answer = answer_question(
        "Хто виграв чемпіонат світу з футболу 2022 року?", retriever, OpenAICompatibleProvider()
    )

    assert not answer.found
    assert answer.sources == []
