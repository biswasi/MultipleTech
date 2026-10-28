!pip install fastapi uvicorn PyJWT

import jwt
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI(title="Secure Protected Microservice")

# Security configuration (This secret must match your Auth Service provider)
# In production, load this securely from environment variables
SHARED_SECRET_KEY = "keep-secret"
ALGORITHM = "HS256"

# Security scheme helper to automatically parse 'Authorization: Bearer <token>'
security_recipient = HTTPBearer()

# Pydantic schemas for structured inputs/outputs
class TokenData(BaseModel):
    user_id: int
    username: str
    role: str

class ResourceResponse(BaseModel):
    message: str
    accessed_by: str
    user_role: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_recipient)) -> TokenData:
    """
    Dependency function to extract, validate, and decode the incoming JWT token.
    Throws a 401 exception immediately if the token is invalid or expired.
    """
    token = credentials.credentials
    try:
        # Decode token and automatically verify signature & expiration ('exp')
        payload = jwt.decode(token, SHARED_SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")
        
        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload is missing identity metadata",
            )
            
        return TokenData(user_id=user_id, username=username, role=role)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authentication token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token"
        )
# --- API Endpoints ---

@app.get("/api/public")
def public_endpoint():
    """An open microservice endpoint accessible without a token."""
    return {"status": "Publicly accessible information"}


@app.get("/api/protected-resource", response_model=ResourceResponse)
def protected_endpoint(current_user: TokenData = Depends(get_current_user)):
    """A secure endpoint. Access is granted only if get_current_user resolves successfully."""
    return ResourceResponse(
        message="Successfully retrieved secure microservice resource!",
        accessed_by=current_user.username,
        user_role=current_user.role
    )


if __name__ == "__main__":
    import uvicorn
    # Start the microservice on port 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)


import jwt
from datetime import datetime, timedelta, timezone

SHARED_SECRET_KEY = "your-super-shared-secret-key-change-me"

# Construct payload representing user info and token metadata
payload = {
    "sub": 42,                         # User Unique ID
    "username": "alice_developer",     # Subject info
    "role": "administrator",           # RBAC details
    "exp": datetime.now(timezone.utc) + timedelta(hours=1) # Expiration
}

token = jwt.encode(payload, SHARED_SECRET_KEY, algorithm="HS256")
print(f"Your Bearer Token:\n{token}")

# Testing without credentials (Returns 401 Unauthorized)
#curl -i http://localhost:8001/api/protected-resource

# Testing with valid token payload (Returns 200 OK)
#curl -i -H "Authorization: Bearer <YOUR_GENERATED_TOKEN>" http://localh



