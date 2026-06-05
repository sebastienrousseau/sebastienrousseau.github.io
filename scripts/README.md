# Site build tools

> Last Updated: June 5, 2026

This folder holds the build and helper scripts that manage compiling and staging for the Sebastien Rousseau website, and all steps stay clean.

## Folder structure

We group the repository tools into domain folders to keep the build system clean and simple.

- **cron:** This folder has the daily release schedule routines and installer files for task tools.
- **dev:** This folder has the local test files and coding helpers used to check the site.
- **editorial:** This folder has the automated translation tools and page metadata setup.
- **generators:** This folder houses the site builders that render templates and blog posts.
- **lib:** This folder holds common Python helper code that runs project activities.
- **postbuild:** This folder handles HTML tweaks, search tags, and sitemap updates.
- **security:** This folder holds key setup files and cryptographic signing scripts.
- **seo_and_audit:** This folder handles link checks, data validation, and text reading ease tools.
