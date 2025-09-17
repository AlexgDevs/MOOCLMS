from fastapi import HTTPException, status

class CustomExeptions:
    '''JWT exeptions'''
    @staticmethod
    async def invalid_token():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token'
        )


    @staticmethod
    async def invalid_token_type():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token type'
        )


    @staticmethod
    async def token_not_found():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token not found'
        )


    '''Models not found'''
    @staticmethod
    async def user_not_found():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )

    @staticmethod
    async def course_not_found():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='course not found'
        )


    @staticmethod
    async def module_not_found():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='module not found'
        )


    @staticmethod
    async def lesson_not_found():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='lesson not found'
        )


    '''other'''
    @staticmethod
    async def invalid_password():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='invalid password'
        )


    @staticmethod
    async def alredy_logined():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='you are already logged in'
        )


    @staticmethod
    async def you_not_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not is admin!'
        )