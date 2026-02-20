from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from datetime import datetime
from app.database import Base, engine
from app.routes import auth, documents, users
from app.core.exceptions import DocumentAPIException
from app.schemas.responses import ErrorResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Document Management API",
    description="Complete Document Management System with Role-Based Access Control",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ==================================================
# Custom Exception Handler
# ==================================================
@app.exception_handler(DocumentAPIException)
async def document_api_exception_handler(request: Request, exc: DocumentAPIException):
    """Handle custom DocumentAPI exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error_code=exc.error_code,
            message=exc.detail,
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details=str(exc) if str(exc) else None,
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


# ==================================================
# Routes
# ==================================================
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)


# ==================================================
# Health Check
# ==================================================
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================================================
# Root Endpoint
# ==================================================
@app.get("/", tags=["Home"])
def root():
    """Welcome to Document Management API"""
    return {
        "message": "Welcome to Document Management API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


# ==================================================
# Swagger Documentation Customization
# ==================================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Document Management API",
        version="1.0.0",
        
 
        routes=app.routes,
    )
    
    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "description": "JWT Bearer token"
        }
    }
    
    # Apply security to all endpoints that need it
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict) and operation.get("tags"):
                # Apply security to protected endpoints
                if operation.get("tags")[0] not in ["Auth", "Home", "Health"]:
                    operation["security"] = [{"HTTPBearer": []}]
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

