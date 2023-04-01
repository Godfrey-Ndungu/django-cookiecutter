Change the database in `cookiecutter` settings and development files from PostgreSQL
======================================================================================

`cookiecutter` is a popular tool for creating templates for Python projects. By default, it comes with settings and development files that use PostgreSQL as the database. However, you may want to use a different database, such as MySQL or SQLite. In this guide, we'll show you how to change the database in the `cookiecutter` settings and development files.

Step 1: Open the `settings` file

The first step is to open the `settings` file in your `cookiecutter` project. This file is located in the `config` directory of your project. You can open it in your favorite text editor.

Step 2: Change the database settings

In the `settings` file, you'll find a section that specifies the database settings. By default, it looks like this:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cookiecutter',
            'USER': 'cookiecutter',
            'PASSWORD': 'cookiecutter',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

To change the database, you'll need to modify the `ENGINE`, `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` settings to match your desired database. For example, if you want to use MySQL, you would change the `ENGINE` setting to `'django.db.backends.mysql'` and modify the other settings accordingly.

Step 3: Open the `development` file

Next, open the `development` file in your `cookiecutter` project. This file is located in the root directory of your project.

Step 4: Change the database settings

In the `development` file, you'll find a section that specifies the database settings. By default, it looks like this:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cookiecutter',
            'USER': 'cookiecutter',
            'PASSWORD': 'cookiecutter',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

To change the database, you'll need to modify the `ENGINE`, `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` settings to match your desired database. For example, if you want to use MySQL, you would change the `ENGINE` setting to `'django.db.backends.mysql'` and modify the other settings accordingly.

Step 5: Save your changes

Once you've made your changes to the `settings` and `development` files, save your changes and exit your text editor.

Step 6: Test your changes

Finally, you'll want to test your changes to make sure everything is working as expected. You can run your `cookiecutter` project as you normally would and verify that your database is being used correctly.

