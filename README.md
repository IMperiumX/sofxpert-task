# ticket-system

This project implements a Django-based REST API for assigning support tickets to agents, focusing on concurrency, scalability, and data integrity. It ensures that no two agents receive the same ticket and that tickets are assigned in the order they were created.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## API Endpoints

The API is built using Django REST Framework's `ViewSet`s for efficient endpoint management.

| Method | Endpoint                       | Description                                                                          | Permissions          |
| ------ | ------------------------------- | ------------------------------------------------------------------------------------ | -------------------- |
| POST   | `/api/users/`                  | Create a new user.                                                                  | Admin only            |
| GET    | `/api/users/`                 | Get a list of all users                                      | Admin or agent        |
| GET    | `/api/users/{id}/`             | Retrieve, update, or delete a specific user.                                       | Admin (or own user) |
| POST   | `/api/agents/`                 | Create a new agent (linked to a user).                                               | Admin only            |
| GET    | `/api/agents/`                | List all agents.                                                                     | Admin or agent        |
| GET    | `/api/agents/{id}/`            | Retrieve, update, or delete a specific agent.                                       | Admin (or own agent) |
| POST   | `/api/tickets/`                | Create a new ticket.                                                                  | Admin only           |
| GET    | `/api/tickets/`                | List tickets. Admins see all; agents see only their assigned tickets.             | Authenticated        |
| GET    | `/api/tickets/{id}/`            | Retrieve, update, or delete a specific ticket.                                       | Admin (or assigned agent)|
| POST   | `/api/tickets/fetch_tickets/` | Fetch and assign up to 15 unassigned tickets to the requesting agent.               | Authenticated Agent |
| POST   | `/api/tickets/sell_tickets/`  | Mark the specified tickets as 'sold' (if assigned to the requesting agent).         | Authenticated Agent |

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    mypy ticket_system

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    coverage run -m pytest
    coverage html
    open htmlcov/index.html

#### Running tests with pytest

    pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd ticket_system
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd ticket_system
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd ticket_system
celery -A config.celery_app worker -B -l info
```

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
