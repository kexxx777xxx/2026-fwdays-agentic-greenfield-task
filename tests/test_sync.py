"""Reconciliation tests for sync against real qdrant."""

from askdocs.sync import sync_once, watch
from askdocs.sources import LocalMarkdownSource


def _sources(store):
    return {payload["source_path"] for _, payload in store.get_all()}


def test_new_file_is_indexed(clean_store, embedder, tmp_path):
    (tmp_path / "a.md").write_text("# A\n\nвміст про гущу", encoding="utf-8")
    source = LocalMarkdownSource(tmp_path)

    summary = sync_once(source, embedder, clean_store)

    assert summary.added == ["a.md"]
    assert _sources(clean_store) == {"a.md"}


def test_edited_file_is_updated_without_stale_chunks(clean_store, embedder, tmp_path):
    doc = tmp_path / "a.md"
    doc.write_text("# A\n\nстарий вміст", encoding="utf-8")
    source = LocalMarkdownSource(tmp_path)
    sync_once(source, embedder, clean_store)

    doc.write_text("# A\n\nновий вміст про ротори", encoding="utf-8")
    summary = sync_once(source, embedder, clean_store)

    assert summary.updated == ["a.md"]
    texts = [p["text"] for _, p in clean_store.get_all()]
    assert any("новий вміст" in t for t in texts)
    assert not any("старий вміст" in t for t in texts)


def test_deleted_file_leaves_no_chunks(clean_store, embedder, tmp_path):
    (tmp_path / "a.md").write_text("# A\n\nвміст", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B\n\nінший вміст", encoding="utf-8")
    source = LocalMarkdownSource(tmp_path)
    sync_once(source, embedder, clean_store)
    assert _sources(clean_store) == {"a.md", "b.md"}

    (tmp_path / "b.md").unlink()
    summary = sync_once(source, embedder, clean_store)

    assert summary.deleted == ["b.md"]
    assert _sources(clean_store) == {"a.md"}


def test_noop_pass_changes_nothing(clean_store, embedder, tmp_path):
    (tmp_path / "a.md").write_text("# A\n\nвміст про гущу", encoding="utf-8")
    source = LocalMarkdownSource(tmp_path)
    sync_once(source, embedder, clean_store)
    before = _store_snapshot(clean_store)

    summary = sync_once(source, embedder, clean_store)

    assert not summary.changed
    assert _store_snapshot(clean_store) == before


def test_watch_runs_exactly_one_pass(clean_store, embedder, tmp_path):
    (tmp_path / "a.md").write_text("# A\n\nвміст", encoding="utf-8")
    source = LocalMarkdownSource(tmp_path)

    watch(source, embedder, clean_store, interval=0, max_iterations=1)

    assert _sources(clean_store) == {"a.md"}


def _store_snapshot(store):
    return {pid: payload["content_hash"] for pid, payload in store.get_all()}
