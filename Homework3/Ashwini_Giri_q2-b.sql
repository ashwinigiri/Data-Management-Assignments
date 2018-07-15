Drop view horror_view;
create view horror_view as select distinct cu.customer_id from customer cu where cu.customer_id in (select r.customer_id from rental r where r.inventory_id in (select i.inventory_id from inventory i where i.film_id in (select fm.film_id from film_category fm,category c where fm.category_id = c.category_id and c.name = 'Horror')));
