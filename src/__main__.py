import argparse
import logging
import sys

import pyuac
import yaml

import tasks
from spreadsheet import Spreadsheet


def main() -> None:
    try:
        # Logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("TaskRunner")

        # Arguments
        parser = argparse.ArgumentParser(
            description="",
            epilog="© 2024 Mariusz Kubisz (contact@maniu.dev)",
        )

        parser.add_argument("config", help="Path to config file")

        args = parser.parse_args()

        # Load config
        logger.info(f"Loading config from: {args.config}")

        config = load_config(args.config)

        # Validate config
        if not config:
            raise ValueError("Config is empty")

        if not config.get("output") or not isinstance(config["output"], str):
            raise ValueError("Output is missing or not a string")

        if not config.get("tasks") or not isinstance(config["tasks"], list):
            raise ValueError("Tasks are missing or not a list")

        if not config.get("items") or not isinstance(config["items"], list):
            raise ValueError("Items are missing or not a list")

        # Elevate privileges
        if config.get("admin_required", False) and not pyuac.isUserAdmin():
            logger.info("Elevating privileges")

            execute = [sys.executable, __file__, *sys.argv[1:]]

            # Remove the first argument if running as a PyInstaller bundle
            if getattr(sys, "frozen", False):
                execute.pop(1)

            return pyuac.runAsAdmin(execute, wait=False)

        # Code
        logger.info("Running code")

        with Spreadsheet(config["output"]) as spreadsheet:
            # Write headers
            spreadsheet.append([task["name"] for task in config["tasks"]])

            # Process items
            for item in config["items"]:
                logger.info(f"Processing item: {item}")
                row = []

                # Process tasks
                for task in config["tasks"]:
                    logger.info(f"└── Processing task: {task['name']}")

                    # Execute task
                    match task["type"]:
                        case "format":
                            output, error = tasks.format(item, task["template"])

                        case "ping":
                            output, error = tasks.ping(item)

                        case "command":
                            output, error = tasks.command(item, task["command"])

                    # Append output to row
                    row.append(output)

                    # Abort on error
                    if task.get("abort_on_error", False) and error is not None:
                        logger.info(f"└── Aborting due to error: {error}")
                        break

                # Append row to spreadsheet
                spreadsheet.append(row)
    except Exception as e:
        logger.error(e)
    finally:
        input("Press Enter to exit")


def load_config(path: str) -> dict:
    with open(path, "r") as config_file:
        config_parsed = yaml.safe_load(config_file)

    return config_parsed


if __name__ == "__main__":
    main()
