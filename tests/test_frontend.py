from pathlib import Path


def test_frontend_assets_exist_and_contain_required_ui() -> None:
    static = Path(__file__).parents[1] / "app" / "static"
    html = (static / "index.html").read_text(encoding="utf-8")
    javascript = (static / "app.js").read_text(encoding="utf-8")
    assert "conversation-list" in html
    assert "message-form" in html
    assert "renderMarkdown" in javascript
    assert "escapeHtml" in javascript
    assert "systemInstruction" not in javascript
