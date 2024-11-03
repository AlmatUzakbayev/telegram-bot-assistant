from pydantic import BaseModel

class UserInput(BaseModel):
    user_input: str

class UserVoiceInput(BaseModel):
    file_path: str

class UserImageInput(BaseModel):
    image_input: str