
import datetime

from app import config
from app import language
from app.home.models import Dashboard
from app.libs.logger import Logger
from app.libs.utils import Utilites

class DashboardServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Dashboard(user)
        self.logger = Logger()

    def getValidationInfo(self):
        self.logger.write_to_console("EVENT", "{0} Getting Statistics {1}".format(self.user['username'], str(self.user['username'])))

        filter_data={}
        validation_query = "SELECT COUNT(*) AS total, SUM(serial_status = 'VALIDATED') AS validated, SUM(serial_status = 'NOT VALIDATED') AS non_validated FROM tbl_serials"
        uploads_query = "SELECT COUNT(*) AS total, SUM(approval_status = 'Approved') AS approved, SUM(approval_status = 'Not Approved') AS pending, SUM(approval_status = 'Declined') AS declined FROM tbl_uploads"
        verification_query = "SELECT COUNT(*) AS total, SUM(status = 'VALIDATED') AS validated, SUM(status = 'NOT VALIDATED' OR status = 'NON EXISTENT') AS failed FROM tbl_activity_log WHERE user_type = 'gen_public'"
        filter_data['validation'] = self.model.getSerialsValidationInfo(validation_query)
        filter_data['uploads'] = self.model.getSerialsValidationInfo(uploads_query)
        filter_data['verification'] = self.model.getSerialsValidationInfo(verification_query)

        print(filter_data)
        return filter_data
    
    def generateSerialsReport(self, request_data):
        """
            This function generates report to be used in the chart
            @Params : void
        """
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        #if no data is supplied, return weekly report
        if 'get_chart' in request_data:
            end_date = self.addDaysToDate(addDays = 6)
            request_data = {'filter_type': 'weekly', 'from_date': end_date, 'end_date':start_date, 'user_type': request_data['get_chart']}
        else:
            #check filter and apply necessary date range
            if request_data['filter_type'] == "daily":
                request_data['from_date'] = start_date
                request_data['end_date'] = start_date
            elif request_data['filter_type'] == "weekly":
                request_data['from_date'] = self.addDaysToDate(addDays = 6)
                request_data['end_date'] = start_date
            elif request_data['filter_type'] == "monthly":
                request_data['from_date'] = self.addDaysToDate(addDays = 30)
                request_data['end_date'] = start_date
            else:
                return []

        report_data = self.model.generateSerialsReport(request_data)

        #process weekly days in order
        if request_data['filter_type'] == "weekly":
            week_days = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]
            i = 0
            for days in report_data:
                days["days"] = week_days[i]
                i+=1

        #process monthly days in order
        elif request_data['filter_type'] == "monthly":
            days_list = self.getDaysList()
            #length = len(days_list)
            formatted_date = [
            "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", 
            "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th",
            "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"
            ]


            for days in report_data:
                day = days["days"]
                total = days["total"]

                #if day is in list
                if day in days_list:
                    index = days_list.index(day)
                    tempDict = {"days": formatted_date[day-1], "total": total}
                    days_list[index] = tempDict
            return days_list

        return report_data


    def addDaysToDate(self, dateFormat="%Y-%m-%d", addDays=0):
        timeNow = datetime.datetime.now()
        anotherTime = timeNow - datetime.timedelta(days=addDays)
        return anotherTime.strftime(dateFormat)

    def getDaysList(self):
        cur_date = datetime.date.today()
        days_ago = cur_date - datetime.timedelta(31) #get 30days ago
        date_difference = cur_date - days_ago
        daysList = []
        for i in range(date_difference.days + 1):
           tempDate = cur_date - datetime.timedelta(i)
           daysList.append(tempDate.day)
        return daysList


