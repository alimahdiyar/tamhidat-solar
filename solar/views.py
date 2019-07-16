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
        for level_type in SolarLevelType.objects.all():
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
                wallet[i] = slice_price(wallet[i] // (level_type.people_in_a_level ** i))


            total = total * tamhidat_card_price
            context['level_types'].append({
                'first_level_share': level_type.first_level_share,
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
        pass
        # the_form = get_object_or_404(QualificationForm, slug=slug)
        # if request.user.is_authenticated:
        #     context = {}
        #
        #     the_student = request.user.profile.first()
        #     the_campaign = get_object_or_404(Campaign, id=int(request.POST['course_id']))
        #     the_grader = get_object_or_404(Profile, id=int(request.POST['grader_id']))
        #     the_grader_cpr = CampaignPartyRelation.objects.get(
        #         type=CampaignPartyRelationType.GRADER,
        #         content_type=ContentType.objects.get_for_model(the_grader),
        #         object_id=the_grader.id,
        #         campaign=the_campaign
        #     )
        #     the_student_cpr = CampaignPartyRelation.objects.get(
        #         type=CampaignPartyRelationType.STUDENT,
        #         content_type=ContentType.objects.get_for_model(the_student),
        #         object_id=the_student.id,
        #         campaign=the_campaign
        #     )
        #     try:
        #         the_qualification = Qualification.objects.get(
        #             src=the_student_cpr,
        #             dst=the_grader_cpr
        #         )
        #         edit = True
        #     except:
        #         the_qualification = Qualification.objects.create(
        #             src=the_student_cpr,
        #             dst=the_grader_cpr
        #         )
        #         edit = False
        #     for qr in the_form.questions.all():
        #         if 'ans_' + str(qr.id) in request.POST and qr.question.is_valid_ans(request.POST['ans_' + str(qr.id)]):
        #
        #             the_qa_qs = QA.objects.filter(
        #                     qualification=the_qualification,
        #                     question=qr
        #                 )
        #
        #             if the_qa_qs.exists():
        #                 the_qa = the_qa_qs.first()
        #                 if request.POST['ans_' + str(qr.id)] != '-1':
        #                     the_qa.answer = request.POST['ans_' + str(qr.id)]
        #                     the_qa.save()
        #                 else:
        #                     the_qa.delete()
        #
        #             else:
        #                 if request.POST['ans_' + str(qr.id)] != '-1':
        #                     QA.objects.create(
        #                         qualification=the_qualification,
        #                         question=qr,
        #                         answer=request.POST['ans_' + str(qr.id)],
        #                     )
        #         else:
        #             context['status'] = 'error'
        #             if not edit:
        #                 the_qualification.delete()
        #                 break
        #
        #     if 'status' not in context:
        #         if edit:
        #             context['status'] = 'modified'
        #         else:
        #             context['status'] = 'new'
        #
        #     context.update(self.the_context(request, the_form))
        #     return render(request, self.template_name, context)
        # else:
        #     return redirect(reverse('users:login') + "?next=" + request.path_info)
