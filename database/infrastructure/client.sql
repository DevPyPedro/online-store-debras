-- public.client_stores definição

-- Drop table

-- DROP TABLE public.client_stores;

CREATE TABLE public.client_users (
	user_id serial NOT NULL,
	user_name text NOT NULL,
	user_cpf text NOT NULL,
	user_cnpj text NULL,
	user_email text NULL,
	user_phone text NULL,
	user_password text NULL,
	user_date text NOT NULL,
	user_register_date text NULL,
	user_status text NOT NULL,
	CONSTRAINT client_users_pkey PRIMARY KEY (user_id)
);

CREATE TABLE public.client_users_resellers (
	user_resellers_id serial NOT NULL,
	user_resellers_name text NOT NULL,
	user_resellers_cpf text NOT NULL,
	user_resellers_cnpj text NULL,
	user_resellers_email text NULL,
	user_resellers_phone text NULL,
	user_resellers_password text NULL,
	user_resellers_date text NOT NULL,
	user_resellers_register_date text NULL,
	user_resellers_status text NOT NULL,
	CONSTRAINT client_users_resellers_pkey PRIMARY KEY (user_resellers_id)
);

CREATE TABLE public.client_users_sellers (
	user_seller_id serial NOT NULL,
	user_seller_name text NOT NULL,
	user_seller_email text NULL,
	user_seller_cpf text NOT NULL,
	user_seller_cnpj text NULL,
	user_seller_phone text NOT NULL,
	user_seller_password text NOT NULL,
	user_seller_date text NOT NULL,
	user_seller_register_date text NOT NULL,
	user_seller_status text NULL,
	CONSTRAINT client_users_sellers_pkey PRIMARY KEY (user_seller_id)
);

CREATE TABLE public.client_stores (
	store_id serial NOT NULL,
	store_name text NOT NULL,
	store_user_associated text NOT NULL,
	store_cnpj text NOT NULL,
	store_email text NULL,
	store_phone text NULL,
	store_address text NULL,
	store_city text NULL,
	store_state text NULL,
	store_cep text NULL,
	store_register_date timestamp NOT NULL,
	store_description text NULL,
	store_status text NULL,
	CONSTRAINT client_stores_pkey PRIMARY KEY (store_id),
	CONSTRAINT client_stores_store_cnpj_key UNIQUE (store_cnpj)
);


