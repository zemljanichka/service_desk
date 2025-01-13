from utils import generate_token


class OperatorService:

    @staticmethod
    async def get_token(username: str):
        return {"token": generate_token(username)}
