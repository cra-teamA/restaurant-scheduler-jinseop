from datetime import datetime , timedelta

import pytest

from schedule import Customer, Schedule
from communication import SmsSender, MailSender
from booking_scheduler import BookingScheduler
from test_communication import TestableSmsSender

NOT_ON_THE_HOUR = datetime.strptime("2021/03/26 09:05", "%Y/%m/%d %H:%M")
ON_THE_HOUR = datetime.strptime("2021/03/26 09:00", "%Y/%m/%d %H:%M")
CUSTOMER = Customer("Fake name", "010-1234-5678")
UNDER_CAPACITY = 1
CAPACITY_PER_HOUR = 3

@pytest.fixture
def booking_scheduler():
    return BookingScheduler(CAPACITY_PER_HOUR)

@pytest.fixture
def booking_scheduler_with_sms_mock():
    booking_scheduler = BookingScheduler(CAPACITY_PER_HOUR)
    testable_sms_sender = TestableSmsSender()
    booking_scheduler.set_sms_sender(testable_sms_sender)

    return booking_scheduler , testable_sms_sender



def test_예약은_정시에만_가능하다_정시가_아닌경우_예약불가(booking_scheduler):
    #arrange
    schedule = Schedule(NOT_ON_THE_HOUR,UNDER_CAPACITY,CUSTOMER)

    #act and asser
    with pytest.raises(ValueError):
        booking_scheduler.add_schedule(schedule)


def test_예약은_정시에만_가능하다_정시인_경우_예약가능(booking_scheduler):
    #arrange
    schedule = Schedule(ON_THE_HOUR,UNDER_CAPACITY,CUSTOMER)

    #act
    booking_scheduler.add_schedule(schedule)

    #assert
    assert booking_scheduler.has_schedule(schedule)


def test_시간대별_인원제한이_있다_같은_시간대에_Capacity_초과할_경우_예외발생(booking_scheduler):
    #arrange
    schedule=Schedule(ON_THE_HOUR,CAPACITY_PER_HOUR,CUSTOMER)
    booking_scheduler.add_schedule(schedule)

    #act and assert
    with pytest.raises(ValueError , match="Number of people is over restaurant capacity per hour"):
        new_schedule = Schedule(ON_THE_HOUR,UNDER_CAPACITY,CUSTOMER)
        booking_scheduler.add_schedule(new_schedule)


def test_시간대별_인원제한이_있다_같은_시간대가_다르면_Capacity_차있어도_스케쥴_추가_성공(booking_scheduler):
    #arrange
    schedule = Schedule(ON_THE_HOUR, CAPACITY_PER_HOUR, CUSTOMER)
    booking_scheduler.add_schedule(schedule)

    #act
    different_hour = ON_THE_HOUR + timedelta(hours=1)
    new_schedule = Schedule(different_hour , UNDER_CAPACITY , CUSTOMER)
    booking_scheduler.add_schedule(new_schedule)

    #assert
    assert booking_scheduler.has_schedule(schedule)
    assert booking_scheduler.has_schedule(new_schedule)

def test_예약완료시_SMS는_무조건_발송(booking_scheduler_with_sms_mock):
    #arrange
    booking_scheduler , sms_mock = booking_scheduler_with_sms_mock
    schedule = Schedule(ON_THE_HOUR , UNDER_CAPACITY , CUSTOMER)

    #act
    booking_scheduler.add_schedule(schedule)

    #assert
    assert sms_mock.send_called

def test_이메일이_없는_경우에는_이메일_미발송():
    pass

def test_이메일이_있는_경우에는_이메일_발송():
    pass

def test_현재날짜가_일요일인_경우_예약불가_예외처리():
    pass

def test_현재날짜가_일요일이_아닌경우_예약가능():
    pass