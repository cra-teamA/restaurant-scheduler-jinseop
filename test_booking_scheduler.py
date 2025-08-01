from datetime import datetime

import pytest

from schedule import Customer, Schedule
from communication import SmsSender, MailSender
from booking_scheduler import BookingScheduler

def test_예약은_정시에만_가능하다_정시가_아닌경우_예약불가():
    #arrange
    not_on_the_hour = datetime.strptime("2021/03/26 09:05","%Y/%m/%d %H:%M")
    customer = Customer("Fake name","010-1234-5678")
    schedule = Schedule(not_on_the_hour,1,customer)
    booking_scheduler = BookingScheduler(3)

    #act and asser
    with pytest.raises(ValueError):
        booking_scheduler.add_schedule(schedule)


def test_예약은_정시에만_가능하다_정시인_경우_예약가능():



def test_시간대별_인원제한이_있다_같은_시간대에_Capacity_초과할_경우_예외발생():
    pass

def test_시간대별_인원제한이_있다_같은_시간대가_다르면_Capacity_차있어도_스케쥴_추가_성공():
    pass

def test_예약완료시_SMS는_무조건_발송():
    pass

def test_이메일이_없는_경우에는_이메일_미발송():
    pass

def test_이메일이_있는_경우에는_이메일_발송():
    pass

def test_현재날짜가_일요일인_경우_예약불가_예외처리():
    pass

def test_현재날짜가_일요일이_아닌경우_예약가능():
    pass