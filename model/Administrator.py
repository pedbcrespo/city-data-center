from configuration.config import ormDatabase as orm
from datetime import datetime
from typing import List

class Administrator(orm.Model):
    __tablename__ = 'administrator'
    id = orm.Column(orm.BigInteger, primary_key=True)
    name = orm.Column(orm.String(200))
    city_id = orm.Column(orm.BigInteger, orm.ForeignKey('city.id'))
    isMainAdm = orm.Column(orm.Boolean, nullable=False, default=True)

    def json(self):
        return {
            'name': self.name,
            'cityId': self.city_id,
            'isMainAdm': self.isMainAdm,
        }

class Expense:
    def __init__(self, name:str, value:float):
        self.name = name
        self.value = value

class Administrate(orm.Model):
    __tablename__ = 'administrate'
    id = orm.Column(orm.BigInteger, primary_key=True)
    adm_id = orm.Column(orm.BigInteger, orm.ForeignKey('administrator.id'))
    street_id = orm.Column(orm.BigInteger, orm.ForeignKey('street.id'))

class AdministratorInfo:
    def __init__(self, name:str, currentInCharge:str, currentStoredValue:float, expenseList:List[Expense]=[], createDate:datetime = datetime.now()):
        self.name = name
        self.currentInCharge = currentInCharge
        self.currentStoredValue = currentStoredValue
        self.expenseList = expenseList
        self.createDate = createDate

    def addExpenseList(self, expenseList: List[Expense]) -> None:
        self.expenseList += expenseList

    def json(self):
        return {
            'name': self.name,
            'currentInCharge': self.currentInCharge,
            'currentStoredValue': self.currentStoredValue,
            'expenseList': self.expenseList,
            'totalExpense': self.__totalExpense__(),
            'createDate': self.createDate
        }
    
    def __totalExpense__(self):
        total = 0.0
        for expense in self.expenseList:
            total += expense.value
        return total

