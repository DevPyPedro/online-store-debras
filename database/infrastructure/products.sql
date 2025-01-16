CREATE TABLE public.products (
	product_id serial4 NOT NULL,
	store_id int8 NOT NULL,
	product_name text NOT NULL,
	product_description text NULL,
	product_price text NOT NULL,
	product_status text NOT NULL,
	product_image text NULL,
	product_created timestamp NOT NULL,
	product_updated timestamp NOT NULL,
	CONSTRAINT products_pkey PRIMARY KEY (product_id)
);


-- public.products chaves estrangeiras

ALTER TABLE public.products ADD CONSTRAINT products_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.client_stores(store_id);


CREATE TABLE public.products_sales_history (
	sale_id serial4 NOT NULL,
	store_id int8 NOT NULL,
	sale_product_id int8 NOT NULL,
	sale_quantity_sold int4 NOT NULL,
	sale_price numeric(10, 2) NOT NULL,
	sale_total_price numeric(15, 2) NULL,
	sale_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	sale_period text NOT NULL,
	CONSTRAINT products_sales_history_pkey PRIMARY KEY (sale_id)
);

-- Table Triggers

create trigger trg_calculate_sale_total_price before
insert
    or
update
    on
    public.products_sales_history for each row execute function calculate_sale_total_price();


-- public.products_sales_history chaves estrangeiras

ALTER TABLE public.products_sales_history ADD CONSTRAINT products_sales_history_sale_product_id_fkey FOREIGN KEY (sale_product_id) REFERENCES public.products(product_id);
ALTER TABLE public.products_sales_history ADD CONSTRAINT products_sales_history_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.client_stores(store_id);


CREATE TABLE public.products_stock (
	stock_id serial4 NOT NULL,
	product_id int8 NOT NULL,
	store_id int8 NOT NULL,
	stock_quantity int4 DEFAULT 0 NOT NULL,
	stock_total_price numeric(15, 2) NULL,
	stock_updated timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT products_stock_pkey PRIMARY KEY (stock_id)
);

-- Table Triggers

create trigger trg_calculate_stock_total_price before
insert
    or
update
    on
    public.products_stock for each row execute function calculate_stock_total_price();


-- public.products_stock chaves estrangeiras

ALTER TABLE public.products_stock ADD CONSTRAINT products_stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
ALTER TABLE public.products_stock ADD CONSTRAINT products_stock_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.client_stores(store_id);