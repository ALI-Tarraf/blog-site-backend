from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    def resolve(self, next, root, info, **args):
        request = info.context
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                pass

        return next(root, info, **args)