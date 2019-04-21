import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from users.models import User


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登陆验证中间件
        # 不需要登陆验证的url
        not_need_check = ['/home/index/', '/users/login/',
                          '/users/regist/', '/cart/cart/',
                          '/cart/f_price/', '/cart/add_cart/',
                          '/media/(.*)', '/static/(.*)',
                          '/goods/detail/(\d+)/','/cart/change_select/(\d+)/',
                          '/cart/make_num/(\d+)/(\d+)/', '/home/search/',
                          '/cart/delete/(\d+)/'
                          ]
        path = request.path
        for not_path in not_need_check:
            # 匹配当前url地址是不是需要登陆验证
            if re.match(not_path, path):
                return None

        # 登陆验证开始
        user_id = request.session.get('user_id')
        # 没有登陆, 获取不到user_id
        if not user_id:
            return HttpResponseRedirect(reverse('users:login'))

        user = User.objects.get(pk=user_id)
        request.user = user

        return None

class UserSessionMiddleware(MiddlewareMixin):
    # 同步session数据到shopping_cart表

    def process_request(self, request):
        # 判断用户是否登录
        user_id = request.session.get('user_id')
        if user_id:
            # 获取到session中的商品数据
            session_goods = request.session.get('goods')
            if session_goods:
                # 1. 如果购物车中没有session中的商品数据, 则创建
                # 2. 如果购物车中有session中的商品数据, 则更新
                # session中商品信息的结构:
                for good in session_goods:
                    if int(good[1]):
                        cart = ShoppingCart.objects.filter(goods_id=good[0], user_id=user_id).first()
                        if cart:
                            cart.nums += int(good[1])
                            cart.is_select = int(good[2])
                            cart.save()
                        else:
                            ShoppingCart.objects.create(user_id=user_id,
                                                        goods_id=good[0],
                                                        nums=int(good[1]),
                                                        is_select=int(good[2]))
                # 删除session中的商品信息
                request.session.pop('goods')
                return None