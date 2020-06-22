from app.libs.mysqllib import MysqlLib

class Dashboard(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(Dashboard, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user


    def getAdminAnalysis(self, request_params):
        data = {"total_trans":{"num":0}, "successful":{"num":0}, "fails":{"num":0}, "initiated":{"num":0}, "sdata":[],"pie_data":[], "bar_data":[]}

        cursor = self.dbconn.getInstanceCursor()

        query = "SELECT status, COUNT(id) as num FROM `tbl_activity_log` WHERE date_created BETWEEN '{0}' and '{1}' GROUP BY status".format(request_params['start_date'], request_params['end_date'])
        # query = "SELECT status, COUNT(id) as num, SUM(amount) as amount FROM `tbl_activity_log` WHERE date_created BETWEEN '{0}' and '{1}' GROUP BY status".format("2017-01-01 00:00:00", "2017-07-01 23:59:59")

        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)
        for result in res:
            data["total_trans"]["num"] = round(data["total_trans"]["num"] + result['num'])
            if result['status'] == 'PENDING':
                data["initiated"]["num"] = result['num']

            if result['status'] == 'FAILED':
                data["fails"]["num"] = result['num']

            if result['status'] == 'SUCCESSFUL':
                data["successful"]["num"] = result['num']

        data['sdata'] = res
        return data


    def getBranchAnalysis(self, request_params):

        data = {"successful":{"num":0}, "fails":{"num":0}, "initiated":{"num":0}, "pie_data":[], "bar_data":[]}

        cursor = self.dbconn.getInstanceCursor()

        query = "SELECT status, COUNT(tbl_transaction.id) as num FROM `tbl_transaction` INNER JOIN tbl_file_upload ON tbl_transaction.bulk_id=tbl_file_upload.bulk_id AND tbl_file_upload.merchant_id='{0}' WHERE transaction_date BETWEEN '{1}' and '{2}' GROUP BY status".format(self.user['institution_data']['id'],request_params['fromdate'], request_params['todate'])
        
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)
        for result in res:
            if result['status'] == 1:
                data["initiated"]["num"] = result['num']
                data["initiated"]["amount"] = result['amount']

            if result['status'] == 2:
                data["fails"]["num"] = result['num']
                data["fails"]["amount"] = result['amount']

            if result['status'] == 3:
                data["successful"]["num"] = result['num']
                data["successful"]["amount"] = result['amount']


        query = "SELECT receivingHouse, COUNT(tbl_transaction.id) as num, SUM(tbl_transaction.amount) as amount FROM `tbl_transaction` INNER JOIN tbl_file_upload ON tbl_transaction.bulk_id=tbl_file_upload.bulk_id AND tbl_file_upload.merchant_id='{0}' WHERE transaction_date BETWEEN '{1}' and '{2}' GROUP BY status".format(self.user['institution_data']['id'],request_params['fromdate'], request_params['todate'])
        
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)

        for result in res:
            data["pie_data"].append({"institution":result['receivingHouse'], "number":result['num']})
            data["bar_data"].append({"institution":result['receivingHouse'], "number":result['amount']})

        print(data)
        return data