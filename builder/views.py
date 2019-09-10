import datetime
from django.templatetags.static import static
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MenuSerializer
from .models import Info, CentralDorm, Yangsung, Yangjin

dorm_list = ['중문기숙사', '양성재', '양진재']
day_list = ['월요일', '화요일', '수요일' ,'목요일' ,'금요일', '토요일' ,'일요일']
quick_dorms = [{
                "action": "message",
                "label": dorm,
                "messageText": dorm
                } for dorm in dorm_list]
quick_days = [{
                "action": "message",
                "label": day,
                "messageText": day,
                } for day in day_list]

def set_info(input_request):
    user_key = input_request.data["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    try:
        dorm = input_request.data['userRequest']['utterance']
    except:
        dorm = ''
    try:
        user = Info.objects.get(user_key=user_key)
        user.dorm = dorm
        user.save()
    except Info.DoesNotExist:
        Info.objects.create(user_key=user_key, dorm=dorm)
    return

def today_date():
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        date = datetime.datetime.now().weekday()
        date_list = ('월', '화', '수', '목', '금', '토', '일')
        today_str = "오늘은 {}년 {}월 {}일\n{}요일 입니다.".format(year, month, day, date_list[date])
        return today_str

@api_view(['POST'])
def set_dorm(request):
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "description": "💁‍♀️기숙사를 선택해주세요",
                        "thumbnail": {
                            "imageUrl": static('/builder/timetable.png')
                        },
                    }
                }
            ],
            "quickReplies": quick_dorms
        },
    }
    return Response(data=response, status=status.HTTP_200_OK)

def get_menu(user_key, day):
    weekday = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"]
    dorm = Info.objects.get(user_key=user_key).dorm
    week = {key: idx for idx, key in enumerate(weekday)}

    if dorm == "중문기숙사":
        return CentralDorm.objects.get(day=week[day])
    elif dorm == "양성재":
        return Yangsung.objects.get(day=week[day])
    elif dorm == "양진재":
        return Yangjin.objects.get(day=week[day])

@api_view(['POST'])
def show_days(request):
    set_info(request)
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "💁‍♀️요일을 선택해주세요\n\n" + today_date()
                    }
                }
            ],
            "quickReplies": quick_days
        },
    }
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(['POST'])
def show_menus(request):
    user_key = request.data["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    day = request.data['userRequest']['utterance']
    serializer = MenuSerializer(get_menu(user_key, day))
    menu = serializer.data['menu']
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": menu
                    }
                }
            ],
            "quickReplies": quick_days
        },
    }
    return Response(data=response, status=status.HTTP_200_OK)