from pydantic import BaseModel, Field

class UserInput(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation identifier")
    role: str = Field(..., pattern="^(user|assistant|system)$", description="Role of the message sender")
    message: str = Field(..., min_length=1, description="User message content")