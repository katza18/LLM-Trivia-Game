from supertokens_python.recipe.session.framework.fastapi import verify_session
from fastapi import APIRouter, Depends, HTTPException
from supertokens_python.recipe.session import SessionContainer
from backend.db.database import SessionLocal
from backend.crud import user


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_user_profile(session: SessionContainer = Depends(verify_session())):
    """
    Endpoint to get the user profile information.
    """
    # Check that the user is logged in
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get the user ID from the session
    user_id = session.get_user_id()

    try:
        db = SessionLocal()
        user_profile = await user.get_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"user_profile": user_profile}
