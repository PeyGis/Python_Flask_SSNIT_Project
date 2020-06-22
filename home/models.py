from app.libs.mysqllib import MysqlLib

class Dashboard(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(Dashboard, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getSerialsValidationInfo(self, query):
        result = self.dbconn.custom_query(query)
        return result

    def generateSerialsReport(self, request_params):
        if request_params['filter_type'] == "daily":
            data = self.dbconn.custom_query("SELECT days_of_week.day AS days, COALESCE(COUNT(id), 0) AS total FROM ( SELECT 0 as day UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23) days_of_week LEFT JOIN tbl_activity_log c ON HOUR(c.date_created) = days_of_week.day AND DATE(c.date_created) BETWEEN '{0}' AND '{1}' AND c.user_type = '{2}' GROUP BY days".format(request_params['from_date'], request_params['end_date'], request_params['user_type']))
        elif request_params['filter_type'] == "weekly":
            data = self.dbconn.custom_query("SELECT days_of_week.day AS days, COALESCE(COUNT(id), 0) AS total FROM ( SELECT 0 as day UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 ) days_of_week LEFT JOIN tbl_activity_log c ON WEEKDAY(c.date_created) = days_of_week.day AND DATE(c.date_created) BETWEEN '{0}' AND '{1}' AND c.user_type = '{2}' GROUP BY days".format(request_params['from_date'], request_params['end_date'], request_params['user_type']))
        elif request_params['filter_type'] == "monthly":
            data = self.dbconn.custom_query("SELECT days_of_week.day AS days, COALESCE(COUNT(id), 0) AS total FROM (SELECT 1 AS day UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 UNION ALL SELECT 31) days_of_week LEFT JOIN tbl_activity_log c ON DAY(c.date_created) = days_of_week.day AND DATE(c.date_created) BETWEEN '{0}' AND '{1}' AND c.user_type = '{2}' GROUP BY days".format(request_params['from_date'], request_params['end_date'], request_params['user_type']))
        else:
            data = []

        return data 
