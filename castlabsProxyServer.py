from aiohttp import web, ClientSession, MultipartReader
import jwt
import secrets
from datetime import datetime
from wsgiref.handlers import format_date_time


routes = web.RouteTableDef()
secret = "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01 d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"

def jwt_factory(request_data):

    payload = {
    "iat": int(datetime.utcnow().timestamp()),
    "jti": secrets.token_hex(),
    "user": request_data["user"],
    "date": request_data["date"],
    }

    encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
    jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
    return encoded_jwt


@routes.post('/proxy-endpoint')
async def post_handler(request):

    try:

        if request.headers["content-type"] == "application/json":
            data = await request.json()
        else:
            data = await request.post()

        request_data = {}
        request_data["user"] = data["user"]
        request_data["date"] = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')

    except Exception as e:
        raise web.HTTPBadRequest(text="missing or malformed request param.")

    #upstream dummy server
    url = 'https://5v4rssbigg.execute-api.us-east-1.amazonaws.com/postendpoint'

    headers = {'x-my-jwt': jwt_factory(request_data)}

    session = ClientSession()

    async with session:
        async with session.post(url, json={'user': request_data['user']}, headers=headers) as response:
            response_text = await response.text()
            return web.Response(text=response_text)

app = web.Application()
app.add_routes([web.post('/proxy-endpoint', post_handler)])


if __name__ == '__main__':
    web.run_app(app)
