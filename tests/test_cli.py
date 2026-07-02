"""Unit tests for CLI rendering (pure, no LLM/store)."""

from askdocs.answer import Answer
from askdocs.cli import render_answer


def test_found_answer_lists_sources_in_order():
    answer = Answer(
        text="Заборонена робуста [1].", sources=["dvyhun/palyvo.md", "bezpeka.md"], found=True
    )
    out = render_answer(answer)

    assert "Заборонена робуста [1]." in out
    assert "Джерела:" in out
    assert out.index("dvyhun/palyvo.md") < out.index("bezpeka.md")


def test_refusal_shows_text_and_explicit_no_sources():
    answer = Answer(text="Цього в документації немає.", sources=[], found=False)
    out = render_answer(answer)

    assert "Цього в документації немає." in out
    assert "Джерела: —" in out
