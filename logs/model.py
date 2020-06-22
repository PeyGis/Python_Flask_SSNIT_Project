from app.application import db

class ValidationLog(db.Model):
    __tablename__ = 'tbl_activity_log'
    id = db.Column(db.Integer(), primary_key=True)
    user_msisdn = db.Column(db.String(15), nullable=False)
    serial_no = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    status_details = db.Column(db.Text(), nullable=False)
    user_mno = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow) 

    def __init__(self):
        return "<{}:{}>".format(self.id, self.user_msisdn)