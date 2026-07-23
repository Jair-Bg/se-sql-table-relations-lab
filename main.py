# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Employees who work in the Boston office
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName, e.jobTitle
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Offices that have zero employees assigned to them
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
# All employees, plus the city/state of their office (if they have one)
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Customers who have not placed any orders
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Customer payments, sorted by amount (cast as a number, not text) descending
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS FLOAT) DESC
""", conn)

# STEP 6
# Employees whose customers have an average credit limit over 90k
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numcustomers DESC
""", conn)

# STEP 7
# Top selling products by number of orders and total units sold
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productCode
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Number of distinct customers who purchased each product
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Number of customers per office
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
""", conn)

# STEP 10
# Employees who sold products that fewer than 20 distinct customers have ordered
df_under_20 = pd.read_sql("""
    WITH product_purchasers AS (
        SELECT od.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
        FROM orderdetails od
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING numpurchasers < 20
    )
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, off.city, off.officeCode
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders o ON c.customerNumber = o.customerNumber
    JOIN orderdetails od ON o.orderNumber = od.orderNumber
    JOIN offices off ON e.officeCode = off.officeCode
    WHERE od.productCode IN (SELECT productCode FROM product_purchasers)
    ORDER BY e.lastName
""", conn)

conn.close()