# Makefile to clean up files for release

# Define the files and folders to be removed
FILES := .coveragerc .dockerignore Makefile README.md tox.ini CONTRIBUTING.rst SECURITY.md
FOLDERS := tests/ .circleci/ docs/

# Define the targets to remove files and folders
clean:
    @echo "Removing files and folders for release..."
    @for file in $(FILES); do \
        rm -rf $$file; \
        echo "Removed $$file"; \
    done
    @for folder in $(FOLDERS); do \
        rm -rf $$folder; \
        echo "Removed $$folder"; \
    done
    @echo "Cleanup complete."
