# Agent Development Instructions

This study repository uses Docker Compose as the source of truth for its development environment.

## Commands

- `make build`: build the development image.
- `make up`: start the development container.
- `make shell`: open a shell inside the container.
- `make test`: compile-check the maintained chapter code inside the container.
- `make check`: run the standard project check.
- `make chapter6-deps`: install optional chapter 6 dependencies inside the container.
- `make down`: stop the Compose services.

## Rules

- Do not install project dependencies on the macOS host.
- Use the container for Python, pip, tests, and scripts.
- Keep `.env` local and never commit or print its values.
- After changing code, run `make check` before reporting completion.
- Install chapter-specific dependencies inside the container with their existing requirements files.
