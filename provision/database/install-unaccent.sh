cat << EOF | sudo su - postgres -c psql
-- Create the database user:
CREATE USER supervagrant SUPERUSER INHERIT CREATEDB CREATEROLE;
ALTER ROLE vagrant SUPERUSER;
EOF