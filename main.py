from fastapi import FastAPI, HTTPException
import traceback   #for detailed error logging
import logging     #for logging errors
from pathlib import Path     #for file path manipulations
import webbrowser           #for opening report in default browser

from src.utils.schemas import OptimizeRequest, OptimizeResponse    #for request/response models
from src.utils.optimizer import optimize_page              #for SEO optimization workflow   

app = FastAPI(title="On-page SEO Optimizer")       #API instance
logger = logging.getLogger(__name__)               #logger for error logging


#endpoint for SEO optimization requests that only returns JSON response
@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(data: OptimizeRequest) -> OptimizeResponse:
    try:
        return optimize_page(str(data.url), data.keyword)
    except ValueError as exc:
        logger.error(f"Validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.error(f"Runtime error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc



#endpoint for SEO optimization requests that also saves and opens report
@app.post("/optimize/save", response_model=OptimizeResponse)
async def optimize_and_save(data: OptimizeRequest) -> OptimizeResponse:
    """Return JSON and also write report.html locally, then open it in the browser."""

    try:
        result = optimize_page(str(data.url), data.keyword)
    except ValueError as exc:
        logger.error(f"Validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.error(f"Runtime error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}") from exc

    report_path = Path(__file__).resolve().with_name("report.html")
    report_path.write_text(result.report, encoding="utf-8")

    #attempt to open the report in the default web browser
    try:
        webbrowser.open(report_path.as_uri())   
    except Exception as open_exc:  #log warning if unable to open browser
        logger.warning(f"Could not open report in browser: {open_exc}")

    return result