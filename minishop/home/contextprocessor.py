from . views import *
from cart.views import *



def cat(request):
    cata = cate.objects.all()
    return {'c': cata}

def count(request, count=0):
    user = request.user
    if user.is_authenticated:
        ct = cartlist.objects.filter(user=user)
    else:
        cart_id = request.session.get('cart_id')
        ct = cartlist.objects.filter(cart_id=cart_id)  # we already uses decorator ghen here this else is not working
    # -------------------------------------------------------------------------
    ct_items = items.objects.filter(cart__in=ct, active=True)
    for i in ct_items:
        #tot += (i.prod.price * i.quan)
        count += i.quan
    return {'cn': count}
