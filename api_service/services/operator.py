from utils import generate_token


class OperatorService:

    @staticmethod
    async def get_token(username: str):
        """Генерация токена оператора"""
        return {"token": generate_token(username)}
