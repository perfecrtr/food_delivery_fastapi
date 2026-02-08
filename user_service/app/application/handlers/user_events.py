from app.domain.events import UserRegisteredEvent
from app.application.commands.create_user_profile import CreateUserProfileCommand, CreateUserProfileHandler
from app.infrastructure.db.repository import UserProfileRepository
from app.infrastructure.db.database import AsyncSessionLocal

class UserEventsHandler:
    
    async def handle_user_registered(self, message: dict):

        async with AsyncSessionLocal() as session:
            try:

                repository = UserProfileRepository(db=session) 
                handler = CreateUserProfileHandler(repository)
                
                event_data = message["data"]

                command = CreateUserProfileCommand(
                    id=event_data["user_id"],
                    phone_number=event_data["phone_number"],
                    fullname=event_data["fullname"]
                )

                saved_user_profile = await handler.handle(command)

                await session.commit()
                
                print(f"User profile created: {saved_user_profile}")
                return {"msg": "success"}
                
            except Exception as e:

                await session.rollback()
                print(f"Error creating user profile: {e}")
                raise
            finally:

                await session.close()


