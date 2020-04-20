from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class TokenAuth():
    def authenticate(self, request):
        token={"token":None}
        # print(request.META.get("HTTP_TOKEN"))
        token["token"] = request.META.get('HTTP_TOKEN')
        print('token',token)
        valid_data = VerifyJSONWebTokenSerializer().validate(token)
        print(valid_data)
        user = valid_data['user']
        print(user)
        if user:
            return
        else:
            raise AuthenticationFailed('认证失败')