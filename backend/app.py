import re
from pathlib import Path
from typing import Optional

from litestar import Litestar, get
from litestar.response import Template
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router
from markupsafe import Markup

from .logic import inventory_service

current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
frontend_dir = root_dir / "frontend"


def highlight_core_loose(text: str, query: str) -> str:
    if not text or not query:
        return text

    tokens = [t for t in query.split() if t.strip()]
    if not tokens:
        return text

    escaped_tokens = [re.escape(t) for t in tokens]
    escaped_tokens.sort(key=len, reverse=True)

    pattern_str = '|'.join(escaped_tokens)

    pattern = re.compile(f"({pattern_str})", re.IGNORECASE)

    style = 'background-color: #ffeb3b; color: #d63384; font-weight: 800; border-radius: 2px; padding: 0 1px;'
    replacement = f'<span style="{style}">\\1</span>'

    return pattern.sub(replacement, text)


def highlight_filter(text: str, query: Optional[str]) -> Markup:
    if not text:
        return Markup("")
    text_str = str(text)
    if not query:
        return Markup(text_str)

    return Markup(highlight_core_loose(text_str, query))


def description_filter(text: str, query: Optional[str]) -> Markup:
    if not text:
        return Markup("")

    text_str = str(text)
    segments = text_str.split(',')

    html_segments = []

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        processed_segment = segment
        is_match = False

        if query:
            temp_result = highlight_core_loose(segment, query)

            if temp_result != segment:
                processed_segment = temp_result
                is_match = True

        css_class = "desc-segment match" if is_match else "desc-segment"

        html_segments.append(f'<div class="{css_class}">{processed_segment}</div>')

    return Markup("".join(html_segments))


class CustomJinjaTemplateEngine(JinjaTemplateEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine.filters["highlight"] = highlight_filter
        self.engine.filters["format_desc"] = description_filter


template_config = TemplateConfig(
    directory=str(frontend_dir),
    engine=CustomJinjaTemplateEngine,
)

static_router = create_static_files_router(
    path="/static",
    directories=[str(frontend_dir)],
)


@get("/")
async def index(q: Optional[str] = None) -> Template:
    results = []
    if q:
        q = q.strip()
        results = inventory_service.search(q)

    return Template(
        template_name="index.html",
        context={
            "query": q,
            "results": results
        }
    )


app = Litestar(
    route_handlers=[index, static_router],
    template_config=template_config,
    debug=True
)