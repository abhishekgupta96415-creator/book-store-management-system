
create  database  bookstore_db;

use bookstore_db; 

create  table  stock(book_no  int  primary  key, 
		title  varchar(20) ,
		author  varchar(10),
 		publisher   varchar(30),
		price  int, qty  int);

create  table  customer(cust_no  int  primary  key,
		name  varchar(20), 
		address  varchar(40)); 

create  table  billing(bill_no  int  primary  key,
		  cust_no  int  references  customer.cust_no);

create  table  billing_details(sale_id int primary key, 
		book_no  int  references  stock.book_no, 
		bill_no  int  references  billing.bill_no,
		price  int, 
		qty  int);

create  table  staff(id  int  primary  key,
		name  varchar(20) not null, 	
		age  int, 
		gender varchar(1),
		contact  int(10), 
		address  varchar(30));
