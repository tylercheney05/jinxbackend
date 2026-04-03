# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test menuitems

# Run a specific test file
python manage.py test menuitems.tests.serializers.test_menu_item.test_write_only_serializer

# Run a specific test class or method
python manage.py test menuitems.tests.serializers.test_menu_item.test_write_only_serializer.TestMenuItemSerializer.test_fields

# Apply migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Environment requires a `.env` file with `SECRET_KEY`, `NODE_ENV`, `HOST`, `REDIS_PORT`, and optionally `REDIS_URL`.

## Architecture

Django REST Framework API backend for a soda shop ordering system. Uses JWT auth (`djangorestframework-simplejwt`), `django-filter` for queryset filtering, `channels`/`daphne` for WebSocket support via Redis, and `pandas`/`openpyxl` for data processing. Deployed to Heroku (`django-heroku`).

### App Structure

Each app follows a consistent structure. Larger apps (e.g. `menuitems`) split their `serializers/`, `tests/`, `filters/`, etc. into sub-packages (directories with `__init__.py`). Smaller apps use flat files.

Key apps:
- **`core`** — Shared base classes: `ReadOnlyModelSerializer` (blocks writes), `AutocompleteViewSetMixin` (adds `/autocomplete` endpoint using pandas), `IsSystemAdminUserOrIsStaffUserReadOnly` permission
- **`users`** — Custom user model (`users.User`) set as `AUTH_USER_MODEL`
- **`menuitems`** — Central domain model; `MenuItem` links to `Soda` and has nested `MenuItemFlavor`, `MenuItemPrice`, `LimitedTimeMenuItem`
- **`orders`** — Complex ordering logic with `OrderItem` supporting three types: `OrderItemMenuItem`, `OrderItemCustomOrder`, `OrderItemMenuItemCustomOrder`
- **`inventory`** — `InventoryItem` uses Django's `GenericForeignKey` (via `ContentType`) to link to arbitrary product models

### Serializer Conventions

- Write serializers use `serializers.ModelSerializer` directly
- Read-only serializers extend `core.serializers.ReadOnlyModelSerializer`
- Nested writes: pop nested data in `create()`, validate and save via nested serializers explicitly (see `MenuItemSerializer.create()`)
- Field naming convention for related fields: `related_model__field_name` (e.g. `order__collected_by`, `cup__size__display`)
- `read_only_fields = ["id"]` on writable serializers
- `extra_kwargs` used for optional fields (e.g. `{"is_archived": {"required": False}}`)
- Complex creates use `@transaction.atomic` on the view, not the serializer

### Testing Conventions

Tests use `django.test.TestCase` and `model_bakery` for fixtures. Test files mirror the source structure — a serializer at `menuitems/serializers/menu_item.py` has tests at `menuitems/tests/serializers/test_menu_item/`. Test classes verify: subclass type, `Meta.model`, `Meta.fields`, field instances, `extra_kwargs`, and `create()` behavior.
