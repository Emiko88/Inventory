from pathlib import Path
from typing import Optional

from litestar import Litestar, get
from litestar.response import Template
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router

from .logic import inventory_service

current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
frontend_dir = root_dir / "frontend"

@get("/")
async def index(q: Optional[str] = None) -> Template:
    results = []
    if q:
        results = inventory_service.search(q)

    return Template(
        template_name="index.html",
        context={
            "query": q,
            "results": results
        }
    )

template_config = TemplateConfig(
    directory=str(frontend_dir),
    engine=JinjaTemplateEngine,
)

static_router = create_static_files_router(
    path="/static",
    directories=[str(frontend_dir)],
)

app = Litestar(
    route_handlers=[index, static_router],
    template_config=template_config,
    debug=True
)