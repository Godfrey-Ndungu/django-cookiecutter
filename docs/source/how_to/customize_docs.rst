Adding Items to the Docs/Source Folder
======================================

To add items to the `docs/source` folder, follow these steps:

1. Navigate to the `docs/source` folder in your project directory.

2. Create a new file for your item using a descriptive name, such as `my_item.rst`.

3. Open the file in a text editor and add your content. Use the reStructuredText syntax to format your content, and be sure to include a title for your item.

4. Save the file and commit it to your project's version control system.

5. If you want your item to appear in the table of contents, update the `index.rst` file in the `docs/source` folder. Add a new entry for your item using the following format:

   .. toctree::
      :maxdepth: 2
      :caption: My Item


   Replace `My Item` with the title of your item, and `my_item` with the name of the file you created in step 2.

6. Build the documentation using Sphinx. You can do this by running the following command from the root of your project directory:

