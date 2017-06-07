from django.http import HttpResponse,HttpRequest
from django.middleware.csrf import CsrfViewMiddleware

# 在没登录的情况下，转向登录界面后，输入账户后，点击登录就再返回开始进入的界面
class url():
    def process_response(self,response,request):
        url_list=[
            '/users/register/',
            '/users/register_handle/',
            '/users/register_exist/',
            '/users/login/',
            '/users/login_handle/',
            '/users/logout/'
        ]
        if not request.is_ajax and request.path not in url_list:
            response.set_cookie('red_url',request.get_full_path())
        return response