from supertokens_python import init, SupertokensConfig, InputAppInfo
from supertokens_python.recipe import session, emailpassword
import os
from backend.auth.overrides import override_emailpassword_functions

def setup_auth():
    init(
        app_info=InputAppInfo(
            app_name="QuizGen",
            api_domain=os.getenv('BACKEND_URL'),  # Your FastAPI backend domain (local dev)
            website_domain=os.getenv('SUPERTOKENS_URI'),  # Your React frontend domain (local dev)
            api_base_path="/auth",  # Path where auth APIs will be exposed
            website_base_path="/auth",  # Path for the frontend SDK
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=os.getenv('SUPERTOKENS_URI'),
            api_key=None  # Optional if you have one set
        ),
        framework="fastapi",
        recipe_list=[
            emailpassword.init(
            override=emailpassword.InputOverrideConfig(
                functions=override_emailpassword_functions
            ),
            ),  # Enable email-password login
            session.init(),        # Enable session management
        ],
        mode="asgi"
    )
