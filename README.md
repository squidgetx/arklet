# squidgetx/arklet: A basic ARK resolver

Fork of the [Internet Archive Arklet](https://github.com/internetarchive/arklet/)
Python Django application for minting, binding, and resolving ARKs
with additional features, improved security and bugfixes.

In use by the Frick Museum in New York ([Fork Link](https://github.com/frickdahl/arklet-frick))


It is intended to follow best practices set out by https://arks.org/.
| |squidgetx/arklet| internetarchive/arklet |
|-|------------- | ------------- |
|ARK resolution|x|x|
|ARK minting and editing|x|x|
|Bulk minting and editing|x||
|Suffix passthrough|x||
|Separate minter and resolver|x||
|API access key hashing|x||
|Shoulder rules|x||
|Extensive metadata|x||
|?info and ?json endpoints|x||

This code is licensed with the MIT open source license.

# Overview

The Arklet service consists of four major components.

1. SQL Database which stores ARK identifiers and related metadata
2. Python Django web application (resolver) which allows users to input URLs containing ARK identifiers and be automatically redirected to the associated resource URL (or alternatively, to receive information about the resource using the `?info` or `?json` suffixes)
3. Python Django web application (minter) which allows administrators to manage the ARK system through both a web API (to mint and edit ARKs) and a graphical web user interface (to manage access tokens and shoulders). The minter can also function as a resolver.
4. Python command line tool (ui/api.py) which allows users to mint and edit ARKs using a command line interface.

The repository comes pre-configured with Docker development and production settings to manage all three components. See the Setup section for more details.

# Usage

## ARK resolution API (resolver and minter)

`GET /ark://1234/a0test` redirects to the URL associated with the given ARK ID, a 404 if the given ARK is in the system but no URL is associated with it, and forwards the request to n2t.net if no ARK record matching the given ID is found at all.

`GET /ark://1234/a0test?info` returns a human readable HTML response with all extra metadata stored in the database and 404 if no matching record is found.

`GET /ark://1234/a0test?json` returns a pure JSON response of all extra metadata stored in the database and 404 if no matching record is found.

`GET /ark://1234/a0test/<suffix>` and `GET /ark://1234/a0test?<suffix>` redirect to the URL associated with the given ARK ID and 'pass through' the suffix to the final destination URL.

## ARK management API (minter only)

ARK management endpoints additionally require an `Authorization` header with a valid API key. API keys can be provisioned by the administrator in the arklet admin user interface and are tied to NAANs.

`POST /mint` mints an ARK described by JSON in the request body. Request parameters:

```
naan
shoulder
url (optional)
metadata (optional)
title (optional)
type (optional)
commitment (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

Returns a JSON response with the minted ark identifier (string). ARKs cannot be minted if the provided shoulder does not exist. The administrator must manage shoulders using the arklet admin user interface.

`PUT /update` updates an ARK described by JSON in the request body. Request parameters:

```
ark
url (optional)
metadata (optional)
title (optional)
type (optional)
commitment (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

Returns an empty 200 response if update is successful.

`POST /bulk_update` update several ARK at once described by JSON in the request body. The request body should be a JSON object with one key (`data`) whose value is an array of objects containing the fields to be updated:

```
ark
url (optional)
metadata (optional)
title (optional)
type (optional)
commitment (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

The maximum number of records that can be updated at once is 100.

`POST /bulk_mint` mints several ARK at once described by JSON in the request body. The request body should be a JSON object with one key (`naan`) which is the NAAN under which the ARKs should be created, and one key (`data`) whose value is an array of objects containing the fields to be updated:

```
shoulder (required)
url (optional)
metadata (optional)
title (optional)
type (optional)
commitment (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

The maximum number of records that can be minted at once is 100.

`POST /bulk_query` queries several ARK at once described by JSON in the request body. The request body should be a JSON object with one key (`data`) which is an array of objects each with one key (`ark`).

The maximum number of records that can be queried at once is 100.

Python command line tools are available in the `/ui` subdirectory for interacting with the API.

## Admin User Interface

Administrators can access the `/admin` user interface of the minter to manage API access keys, shoulders, NAANs, and other administrators. Administrator access is protected using standard username and password authentication. The first administrator account must be set up when initially deploying the application.

# Setup

## Local

Use `docker-compose up` to automatically launch the `postgres` database, the `arklet-minter` component, and the `arklet-resolver` component. By default, the minter runs on 127.0.0.1:8001 and the resolver runs on 127.0.0.1:8000.

Configuration for the local environment can be found in the `docker/env.local` envfile. Note that if you wish to change the ports you also need to update the port forwarding configuration in `docker-compose.yml`.

### Creating a Superuser

You need to create the first user with admin privileges from the command line in order to properly set up the application.

```
make dev-cmd
```

launches a bash shell in the minter container.

```
./manage.py createsuperuser
```

creates the superuser

### Admin Panel Setup

To continue the setup, you can access the Admin panel via web browser at `127.0.0.1:8000/admin`.

Create a NAAN and an associated API key.

## Production

This repo is pre-configured for production deployment using nginx, gunicorn, and assuming a managed database instance + general webserver compute instance (eg, Digital Ocean droplet + managed postgres). Nginx and gunicorn replace the development Django server offering improved performance and security.

Fill in the relevant postgres credentials and a secure Django secret key in `env.prod.example` and rename the file to `env.prod`.

To launch the minter, resolver, and nginx server run `docker-compose -f docker-compose.nginx.yml --profile nginx up`, or simply `make prod`. By default, the resolver runs on port 80 (eg, no need to specify a port number when using the resolver service) and the minter runs on port 8080. If you wish to change the port that the minter is accessed on you must alter the port numbers in both `docker-compose.nginx.yml` as well as `nginx.conf`
