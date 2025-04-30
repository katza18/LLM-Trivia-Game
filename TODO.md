# TODO
## Root
- [x] Write docker-compose.yml
- [x] Build docker containers

## Backend
- [x] Install SuperTokens python SDK
- [x] Add SuperTokens connection to backend (backend/main.py)
- [x] Configure CORS to allow frontend
- [x] Update alembic database location
- [x] User crud functions
- [x] Check user quota in generate questions endpoint (api/questions.py)
- [x] Add token_log create, read and delete
- [ ] Create a universal get and delete function.
- [x] Add favorite question create, read and delete
- [x] Add list create, read, update, delete
- [ ] Add list_item create, read, delete
- [x] Pass the quota into generate quiz and then before submitting to the API, check if theres enough quota left
- [ ] Add username logic to account setup
- [x] Override SuperTokens signup endpoint to add User in app database
- [ ] Add non-logged in routes like a fetch quiz for users who arent logged in that uses stored questions.


## Frontend
- [ ] Install SuperTokens React SDK
- [ ] Implement Login page with create account form
- [ ] Implement User subscribe page
