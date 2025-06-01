from model.Street import Street
from datetime import datetime

class CommercialInfo:
    def __init__(self, street: Street, qtyCommercialEstab: int, avgEarning: float, createDate: datetime=datetime.now()):
        self.street = street
        self.qtyCommercialEstab = qtyCommercialEstab
        self.avgEarning = avgEarning
        self.createDate = createDate

    def json(self):
        return {
            'streetId': self.street.id,
            'qtyCommercialEstab': self.qtyCommercialEstab,
            'avgEarning': self.avgEarning,
            'createDate': self.createDate
        }