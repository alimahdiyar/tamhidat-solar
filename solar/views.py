from django.shortcuts import render
from django.views import View

from solar.models import SolarLevelType

def slice_price (price):
    price_str = str(price)[::-1]
    price_sliced_lst = [price_str[i: i + 3] for i in range(0, len(price_str), 3)]
    return ','.join(price_sliced_lst)[::-1]

class solar_level_view(View):
    template_name = 'solar-level.html'

    @staticmethod
    def the_context(request):
        context = {
            'level_types': []
        }
        tamhidat_card_price = 100000
        for level_type in SolarLevelType.objects.all().order_by('-id'):
            wallet = [0]

            for i in range(1, level_type.levels):
                wallet.append(0)
                wallet[i - 1] += (level_type.people_in_a_level ** i) * level_type.first_level_share * tamhidat_card_price // 100
                for j in range(0, i - 1):
                    wallet[j] += (level_type.people_in_a_level ** i) * level_type.other_levels_share * tamhidat_card_price // 100

            total = 0
            shares_total = sum(wallet)
            for i in range(len(wallet)):
                total += level_type.people_in_a_level ** i
                wallet[i] = str(level_type.people_in_a_level ** i) + ' - ' + slice_price(wallet[i] // (level_type.people_in_a_level ** i)) + ' - ' + slice_price(wallet[i])


            total = total * tamhidat_card_price
            context['level_types'].append({
                'first_level_share': level_type.first_level_share,
                'tamhidat_card_price': level_type.tamhidat_card_price,
                'other_levels_share': level_type.other_levels_share,
                'people_in_a_level': level_type.people_in_a_level,
                'levels': level_type.levels,
                'shares': wallet,
                'shares_total': slice_price(shares_total),
                'avizhe_share': slice_price(total - shares_total),
                'total': slice_price(total),
            })

        return context

    def get(self, request, slug=None, *args, **kwargs):
        context = self.the_context(request)
        return render(request, self.template_name, context)

    def post(self, request, slug=None, *args, **kwargs):
        try:
            SolarLevelType.objects.create(
                    first_level_share = int(request.POST['first_level_share']),
                    other_levels_share = int(request.POST['other_levels_share']),
                    people_in_a_level = int(request.POST['people_in_a_level']),
                    levels = int(request.POST['levels']),
                    tamhidat_card_price = int(request.POST['tamhidat_card_price']),
            )
        except:
            pass
        context = self.the_context(request)
        return render(request, self.template_name, context)
