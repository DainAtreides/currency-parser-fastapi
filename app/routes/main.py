from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.exchange import get_exchange_rate

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@main_router.get("/", response_class=HTMLResponse)
async def get_index(request: Request, currency: str = "USD"):
    rate, date = await get_exchange_rate(currency)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "currency": currency,
        "rate": rate,
        "date": date
    })
