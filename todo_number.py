"""Async app for number requests."""
import json

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from httpx import AsyncClient

app = FastAPI()
async_client = AsyncClient()
headers = {'Access-Control-Allow-Origin': '*'}


@app.get('/todo/{number}')
async def get_todo(number):
    """
    Do get request to https://jsonplaceholder.typicode.com/todos/{number}.

    Parameters:
        number: number to request

    Returns:
        JSONResponse with response body or error if smth went wrong.
    """
    response = await async_client.get(
        'https://jsonplaceholder.typicode.com/todos/{0}'.format(number),
    )
    if response.is_error:
        return JSONResponse(
            content=json.loads('{"message": "Not found."}'),
            status_code=response.status_code,
            headers=headers,
        )
    # remove contend-encoding header to stop getting decode errors
    response.headers.pop('content-encoding')
    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
        headers=headers,
    )


if __name__ == '__main__':
    port = 8000
    uvicorn.run(app, host='0.0.0.0', port=port)
