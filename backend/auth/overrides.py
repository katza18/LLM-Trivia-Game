from supertokens_python.recipe.emailpassword.interfaces import (
    RecipeInterface,
    SignUpOkResult,
)
from typing import Dict, Any, Union
from supertokens_python.recipe.session.interfaces import SessionContainer
from backend.crud.user import create_user, UserSchema
from backend.db.database import SessionLocal


def override_emailpassword_functions(original_implementation: RecipeInterface) -> RecipeInterface:
    original_sign_up = original_implementation.sign_up

    async def sign_up(
        email: str,
        password: str,
        tenant_id: str,
        session: Union[SessionContainer, None],
        should_try_linking_with_session_user: Union[bool, None],
        user_context: Dict[str, Any],
    ):
        result = await original_sign_up(
            email,
            password,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            user_context,
        )

        if isinstance(result, SignUpOkResult) and len(result.user.login_methods) == 1:
            id = result.user.id
            email = result.user.emails[0].email

            # Add use to app database
            db = SessionLocal()

            try:
                user_data = UserSchema(id, email)
                create_user(db, user_data)
            except:
                raise
            finally:
                db.close()

        return result

    original_implementation.sign_up = sign_up

    return original_implementation
