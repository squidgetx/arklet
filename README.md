# Arklet-Frick: A basic ARK resolver

Arklet-Frick is a fork of the [arklet](https://github.com/internetarchive/arklet/) project
with additional features, improved security and several bugfixes. This work was largely developed in support of the Frick Art Reference Library's use case.

Arklet-Frick is a Python Django application for minting, binding, and resolving ARKs.
It is intended to follow best practices set out by https://arks.org/.

This code is licensed with the MIT open source license.

# Usage / API

The django application can be run either in minter mode, or in resolver mode. Resolver mode is limited to read requests, while the minter can be used for editing and updating ARKs.

## ARK resolution (minter or resolver modes)

`GET /ark://1234/a0test` redirects to the URL associated with the given ARK ID, a 404 if the given ARK is in the system but no URL is associated with it, and forwards the request to n2t.net if no ARK record matching the given ID is found at all.

`GET /ark://1234/a0test?info` returns a human readable HTML response with all extra metadata stored in the database and 404 if no matching record is found.

`GET /ark://1234/a0test?json` returns a pure JSON response of all extra metadata stored in the database and 404 if no matching record is found.

## ARK management (minter mode only)

ARK management endpoints additionally require an authorization header with a valid API key.

`POST /mint` mints an ARK described by JSON in the request body. Request parameters:

```
naan
shoulder
url (optional)
metadata (optional)
title (optional)
type (optional)
rights (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

Returns a JSON response with the minted ark identifier (string).

`PUT /update` updates an ARK described by JSON in the request body. Request parameters:

```
ark
url (optional)
metadata (optional)
title (optional)
type (optional)
rights (optional)
identifier (optional)
format (optional)
relation (optional)
source (optional)
```

Returns an empty 200 response if update is successful.

Python command line tools are available in the `/ui` subdirectory for interacting with the API.

# Deployment

## Local deployment

Use `docker-compose up` to automatically launch the `postgres` database, the `arklet-minter` component, and the `arklet-resolver` component. By default, the minter runs on 127.0.0.1:8000 and the resolver runs on 127.0.0.1:8001.

Configuration for the local environment can be found in `docker/env.[minter|postgres|resolver].local` envfiles. Note that if you wish to change the ports you also need to update the port forwarding configuration in `docker-compose.yml`.

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

## Production Deployment

This repo is pre-configured for production deployment assuming a managed database instance + general webserver compute instance (eg, Digital Ocean droplet + managed postgres).

Create corresponding env files with the `prod` suffix in the `docker` directory (eg, `env.postgres.prod`), filling in the relevant postgres credentials and an actually secure Django secret key.

To launch both the minter and the resolver, run `docker-compose -f docker-compose.prod.yml up`, or simply `make prod`.

To launch just the minter or just the resolver (eg, if you want to run the resolver/minter on separate machines), specify the container name at the end of the command:

```
docker-compose -f docker-compose.prod.yml up arklet-minter
```

You will need to complete the same setup steps as above.
