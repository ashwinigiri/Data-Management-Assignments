import mysql.connector
import sys
cnx = mysql.connector.connect(user='inf551',password='inf551',host='127.0.0.1',database='sakila')
cursor=cnx.cursor()
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg1 = arg1.strip().lower()
arg2 = arg2.strip().lower()
query = "select count(*) from customer cu where cu.customer_id in (select r.customer_id from rental r where r.inventory_id in (select i.inventory_id from inventory i where i.film_id in (select fm.film_id from film_category fm,category c where fm.category_id = c.category_id and c.name = \""+arg1+"\"))) and cu.customer_id not in (select r.customer_id from rental r where r.inventory_id in (select i.inventory_id from inventory i where i.film_id in (select fm.film_id from film_category fm,category c where fm.category_id = c.category_id and c.name = \""+arg2+"\")));"
cursor.execute(query)
for count in cursor:
    print(count[0])
cursor.close()
cnx.close()
