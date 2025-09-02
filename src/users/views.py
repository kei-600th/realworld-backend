from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer


def error_response(messages, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY):
    """
    RealWorld形式のエラー: { "errors": { "body": ["..."] } }
    messages: str | list[str]
    """
    if isinstance(messages, str):
        messages = [messages]
    return Response({"errors": {"body": messages}}, status=status_code)


class RegisterView(APIView):
    """
    POST /api/users
    Request:  { "user": { "username": "...", "email": "...", "password": "..." } }
    Response: { "user": { "email": "...", "token": "<jwt>", "username": "...", "bio": null, "image": null } }
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data.get("user")
        if payload is None or not isinstance(payload, dict):
            return error_response("`user` object is required", status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationSerializer(data=payload)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except ValidationError as e:
            # DRFのValidationError -> 422 + RealWorld形式に整形
            # e.detail は dict or list のことがあるので、各メッセージを平坦化
            def flatten(err):
                if isinstance(err, (list, tuple)):
                    for v in err:
                        yield from flatten(v)
                elif isinstance(err, dict):
                    for v in err.values():
                        yield from flatten(v)
                else:
                    yield str(err)

            return error_response(list(flatten(e.detail)), status.HTTP_422_UNPROCESSABLE_ENTITY)
        except IntegrityError:
            # username のユニーク制約などDBレベルの衝突
            return error_response("username is already taken", status.HTTP_422_UNPROCESSABLE_ENTITY)

        # JWT発行（SimpleJWT）
        access = RefreshToken.for_user(user).access_token
        token = str(access)

        # RealWorldの応答フォーマットに合わせて返す（bio/image は当面 null）
        resp = {
            "user": {
                "email": user.email,
                "token": token,
                "username": user.username,
                "bio": None,
                "image": None,
            }
        }
        # RealWorld実装は 200 を返すことが多いので 200 に合わせます（201でも可）
        return Response(resp, status=status.HTTP_200_OK)
