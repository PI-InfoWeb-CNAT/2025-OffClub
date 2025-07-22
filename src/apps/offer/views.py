from django.shortcuts import render, redirect, get_object_or_404
from ..offer.models import *
from .services.discount import Discount

def offer_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
        # busca no model, na classe 'Offer', uma oferta que tenha o id igual a pk
        # se achar, vai guardar na variável 'offer', e se não encontrar, mostra a pág de erro
    
    enterprise = offer.enterprise
    picture_enterprise = offer.enterprise.user.profile_picture
    title = offer.title
    description = offer.description
    category = offer.category
    image = offer.image
    price = offer.price
    discount = offer.discount
    start_date = offer.start_date
    end_date = offer.end_date
    redemption_period = offer.redemption_period
    max_coupons = offer.max_coupons
    generated_coupons = offer.generated_coupons


    context = {
        'enterprise': enterprise,
        'picture_enterprise': picture_enterprise,
        'title': title,
        'description': description,
        'category': category,
        'image': image,
        'price': price,
        'discount': discount,
        'start_date': start_date,
        'end_date': end_date,
        'redemption_perio': redemption_period,
        'max_coupons': max_coupons,
        'generated_coupons': generated_coupons
    }



    return render(request, 'offer_detail.html', context)

