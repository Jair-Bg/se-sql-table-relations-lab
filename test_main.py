import sqlite3
import pandas as pd
from main import *

def test_join_and_filter():
    assert(df_boston.shape == (2, 3))
    assert(list(df_boston['firstName']) == ['Julie', 'Steve'])
    assert(df_zero_emp.shape[0] == 0)

def test_type_of_join():
    assert(df_employee.shape == (23, 4))
    assert(df_employee.iloc[0]['firstName'] == 'Andy')
    assert(df_contacts.shape == (24, 4))
    assert(list(df_contacts['contactFirstName'])[0:3] == ['Raanan', 'Mel', 'Carmen'])

def test_builtin_function():
    assert(df_payment.shape == (273, 4))
    assert(df_payment.iloc[0]['contactFirstName'] == 'Diego ')

def test_joining_and_grouping():
    assert(df_credit.shape == (4, 4))
    assert(df_credit.iloc[0]['firstName'] == 'Larry')
    assert(df_product_sold.shape == (109, 3))
    assert(df_product_sold.iloc[0]['totalunits'] == 1808)

def test_multiple_joins():
    assert(df_total_customers.shape == (109, 3))
    assert(df_total_customers.iloc[0]['numpurchasers'] == 40)
    assert(df_customers.iloc[0]['n_customers'] == 12)
    assert('n_customers' in list(df_customers.columns))

def test_subquery():
    assert(df_under_20.shape == (15, 5))
    assert(df_under_20.iloc[0]['firstName'] == 'Loui')