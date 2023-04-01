Customize Ansible Variables
=============================

Ansible is an open-source automation tool that can be used for a wide range of tasks, including configuration management, deployment, and orchestration. The `django-minimal-cookiecutter` project includes an Ansible playbook that can be used to set up your development environment. In this guide, you'll learn how to customize the Ansible variables in this playbook to suit your needs.

Step 1: Modify the PostgreSQL variables

The Ansible playbook includes variables for setting up a PostgreSQL database and user. You can modify these variables to use your own PostgreSQL database and user. Open the `ansible/vars/main.yml` file and modify the following variables:

- `postgres_database`: Change this variable to the name of your desired PostgreSQL database.
- `postgres_user`: Change this variable to the name of your desired PostgreSQL user.
- `postgres_password`: Change this variable to the password for your PostgreSQL user.

For example, to use a PostgreSQL database named `mydb` and a user named `myuser` with the password `mypassword`, you would modify the variables as follows:

.. code-block:: yaml

    postgres_database: mydb
    postgres_user: myuser
    postgres_password: mypassword

Step 2: Modify the project name

The `project_name` variable in the `ansible/vars/main.yml` file specifies the name of your project. You can modify this variable to use your own project name:

.. code-block:: yaml

    project_name: myproject

Step 3: Modify the Docker Compose version

The `docker_compose_version` variable in the `ansible/vars/main.yml` file specifies the version of Docker Compose that will be installed. You can modify this variable to use a different version of Docker Compose:

.. code-block:: yaml

    docker_compose_version: 1.29.2

Step 4: Modify the Nginx template file

The `ansible/roles/nginx/tasks/main.yml` file includes a task for configuring Nginx. This task uses a Jinja2 template to generate the Nginx configuration file. You can modify the `src` variable in this task to point to the template file for your own Nginx configuration. 

For example, if you've created a custom Nginx configuration file called `myproject.conf.j2`, you would modify the task as follows:

.. code-block:: yaml

    - name: Generate Nginx configuration file
      template:
        src: "path/to/myproject.conf.j2"
        dest: "/etc/nginx/sites-available/{{ project_name }}"

Conclusion
----------

In this guide, you learned how to customize the Ansible variables in the `django-minimal-cookiecutter` project to suit your needs. By modifying these variables, you can set up your development environment with your own PostgreSQL database and user, project name, Docker Compose version, and Nginx configuration file.
