# Local daily-publish automation

> Last Updated: June 4, 2026

The automation scripts in this folder handle daily article publication tasks from your local computer, which Sebastien runs manually each evening to check the pages before pushing.

## Why local, not cloud

We run the publishing tasks locally to keep the API secrets safe on your own machine. The local script uses your GPG keys to sign commits and push changes to the repository.

## What it does

The script pulls the latest code and calls the translation tool to generate the new pages, and it also checks for drafts, runs the tests, and opens a pull request automatically.

## Install

Run the install script to setup the task scheduler and register the plist service on your operating system. The script creates the log path and registers the daily schedule.

## Schedule

The scheduler runs the task in the morning to align the release of new content with active publishing times, and running it twice ensures that the posts land at the right time.

## Alternative: cron with strict UTC

You can edit your user crontab if you want to run the job at a fixed time. This needs disk access on macOS, so the plist is the best choice.

## Test / verify

You can test the tool by running the script and reading the files in the log folder, and if there is no draft, the runner exits with no changes.

## Uninstall

To remove the job, run the uninstall script to stop the service and delete the plist settings from your system folder. You must delete the log files by hand if needed.

## What can break (and how to debug)

The debug table lists common issues like bad paths, git blocks, budget caps, or push errors. Check the logs to see which step failed during the run.

## Files in this folder

This folder holds the plist file, the install scripts, the main runner, and this guide.
