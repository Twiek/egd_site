# EGD Site based on Frappe

Effective Altruism Day Website based on Frappe Framework.


# Setup

## Install Frappe
Please follow instructions from: (https://frappeframework.com/docs/user/en/installation)[https://frappeframework.com/docs/user/en/installation].


## Create a new site

```
bench new-site --db-name db_egd --mariadb-root-password ******* --force egd.local
```

## Install app on created site

```
bench get-app git@github.com:Ayuda-Efectiva/egd_site.git
bench update --requirements
bench --site egd.local install-app egd_site
```

## Load your local site

```
bench start
```

Add **egd.local** to your hosts file pointing to **localhost** and load **egd.local:8000** in your browser.


# Multilanguage

There are two folders with translatable or localizable text.


## Markdown/HTML pages inside /egd_site/www/xx

Whole site navigation structure with code and translatable text. There is one folder **xx** per language.

At the top of the markdown pages there are some variables. Two of them needs translation too:

  * **title**: html page title
  * **meta_description**: Meta tag description


## xx.csv files inside /egd_site/translations/

Contains one file per language named as **xx.csv** where **xx** is the language.

Each CSV file is formed by three columns:

  * **Column 1 (do not modify)**: File where the translation key is located (it could be in different locations too)
  * **Column 2 (do not modify)**: Translation key
  * **Column 1**: Translation for CSV language. You can use **,** (comma) but you need to wrap whole translation with **"**.


# License

MIT
