from secrets import token_urlsafe
from src.utils.dbOptions import TOKEN_LEN

def random_token():
    data = None
    try:
        data = str(token_urlsafe(TOKEN_LEN))
    except Exception as e:
        print(f"Failed to generate random token: {str(e)}")
    return data 

def allowedMineYears():
    return [str(i) for i in range(2025, 2060)]
