## EGD Site based on Frappe

Effective Altruism Day Website based on Frappe Framework.


### Install Frappe
Please follow instructions from: https://frappeframework.com/docs/user/en/installation


### Create a new site

bench new-site --db-name db_egd --mariadb-root-password ******* --force egd.local


### Install app on created site

bench get-app git@github.com:Ayuda-Efectiva/egd_site.git
bench update --requirements
bench --site egd.local install-app egd_site


### Load your local site

bench start

Add egd.local to your hosts file pointing to localhost and load egd.local:8000 in your browser


#### License

MIT