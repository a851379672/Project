from datetime import date
import datetime
import time


class DateTime:

    def __init__(self):
        self.datetime_ = {
            'year': 0 and '',
            'month': 0 and '',
            'day': 0 and '',
            'hour': 0 and '',
            'min': 0 and '',
            'sec': 0 and ''
        }

    def date_today(self):
        """
        获取当前日期
        :return: "YYYY-MM-DD"
        """
        return date.today()

    def date_time(self):
        """
        获取当前时间
        :return: YYYY-MM-DD HH:MM:SS
        """
        return datetime.datetime.now().replace(microsecond=0)

    def msec_sec(self, time_):
        """
        毫秒转秒
        :return: int(sec)
        """
        return int(time_ / 60)

    def time_stamp(self, datetime_):
        """
        时间格式转时间戳 ：2013-10-10 23:40:00 转 1381419600000
        :param: datetime
        :return:
        """
        try:
            time_array = time.strptime(datetime_, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            time_array = time.strptime(datetime_, "%Y-%m-%d %H:%M")
        return round(time.mktime(time_array) * 1000)

    def stamp_time(self, timestamp):
        """
        时间戳转时间格式 ；1381419600 转 2013-10-10 23:40:00
        :param timestamp
        :return:
        """
        try:
            time_array = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
        except ValueError:
            time_array = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(timestamp)))
        return time_array

    def diy_time(self, args):
        """
        :param args: (YYYY, MM, DD, HH, MM, SS)
        :return: yyyy-mm-dd hh:mm:ss
        """
        args = [arg.strip() for arg in args.split(',')]
        if len(args) < 6:
            format_ = ['sec', 'min', 'hour', 'day', 'month', 'year']
            [self.datetime_.pop(format_[date_]) for date_ in range(len(format_)) if len(args) < len(self.datetime_)]
        date_ = {key: value for (key, value) in zip(self.datetime_.keys(), args) if key}
        objects = DateTime()
        datetime_ = objects.datetime_
        for func, value in date_.items():
            if set(r"([\+\-\])").intersection(value):
                # 是否交集
                getattr(objects, f'get_{func}')(value)
            elif value.startswith('*'):
                # 当前时间
                if func in 'year, hour, min, sec':
                    func = func.replace(func[0], func[0].upper())
                datetime_[func.lower()] = int(datetime.datetime.now().strftime(f'%{func[0]}'))
            else:
                # 指定时间
                datetime_[func] = value
            func_value = datetime_[func.lower()]
            if len(datetime_[func.lower()].__str__()) == 1:
                # 是否补0
                func_value = '%02d' % func_value
                datetime_[func.lower()] = func_value
        result_time = ''
        datetime_format = {'year': '-', 'month': '-', 'day': ' ', 'hour': ':', 'min': ':', 'sec': ''}
        for key in date_.keys():
            result_time += datetime_[key].__str__() + datetime_format[key]
        if len(args) < 6:
            result_time = result_time.replace(result_time[-1], '')
        return result_time

    def get_year(self, n):
        """
        :param n
        :return: year
        """
        if n:
            self.datetime_['year'] = int(datetime.datetime.now().strftime('%Y'))

    def get_month(self, n):
        """
        :param n
        :return: month
        """
        month_ = int(datetime.datetime.now().strftime('%m')) + int(n)
        if month_ > 12:
            self.datetime_['year'] += 1
            self.datetime_['month'] = month_ - 12
        else:
            self.datetime_['month'] = month_

    def get_day(self, n):
        """
        :param n
        :return: day
        """
        datetime_ = self.date_time() + datetime.timedelta(days=int(n))
        self.datetime_['day'] += datetime_.day
        if int(n) > 0 and datetime_.month - self.date_time().month:
            self.datetime_['month'] += 1
        elif int(n) < 0 and self.date_time().month - datetime_.month:
            self.datetime_['month'] -= 1

    def get_hour(self, n):
        """
        :param n
        :return: hour
        """
        datetime_ = self.date_time() + datetime.timedelta(hours=int(n))
        self.datetime_['hour'] = datetime_.hour
        if int(n) > 0 and datetime_.day - self.date_time().day:
            self.datetime_['day'] += 1
        elif int(n) < 0 and self.date_time().day - datetime_.day:
            self.datetime_['day'] -= 1

    def get_min(self, n):
        """
        :param n
        :return: min
        """
        datetime_ = self.date_time() + datetime.timedelta(minutes=int(n))
        self.datetime_['min'] = datetime_.minute
        if int(n) > 0 and datetime_.hour - self.date_time().hour:
            self.datetime_['hour'] += 1
        elif int(n) < 0 and self.date_time().hour - datetime_.hour:
            self.datetime_['hour'] -= 1

    def get_sec(self, n):
        """
        :param n
        :return: sec
        """
        datetime_ = self.date_time() + datetime.timedelta(seconds=int(n))
        self.datetime_['sec'] = datetime_.second
        if int(n) > 0 and datetime_.minute - self.date_time().minute:
            self.datetime_['min'] += 1
        elif int(n) < 0 and self.date_time().minute - datetime_.minute:
            self.datetime_['min'] -= 1


if __name__ == "__main__":
    object_ = DateTime()
    # diy时间 2021-9-19 18:3:30
    print(object_.time_stamp(object_.date_time().__str__()))  # 当前时间转时间戳 1643160050000
    print(object_.stamp_time('1381419600'))  # 2013-10-10 23:40:00
    print(object_.diy_time(('*, *, +02, +03')))  # 2022-01-28 11:40:30
    object_ = DateTime()
    print(object_.time_stamp(
        object_.diy_time(('*, +09, -02, +03, -40, 30'))))  # diy时间转时间戳 1661522790000
    print(object_.date_today())  # 获取当前日期, 2021-09-17
    print(object_.date_time())   # 2021-09-17 15:43:19.892563
    print(object_.msec_sec(3600))   # 60
