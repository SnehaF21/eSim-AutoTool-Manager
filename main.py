
from core.tool_detector import detect_tools, TOOL_CATALOG
from core.installer import install_tool
from core.updater import check_updates, update_tool
from core.config_manager import (
    load_settings,
    save_settings,
    show_settings,
    set_tool_path
)
from core.dependency_checker import run_dependency_check
from core.logger import get_logger

logger = get_logger()


def pause():
    input("\nPress Enter to continue...")


def show_tools():
    print("\n--- Installed tool status ---")

    results = detect_tools()

    for key, item in results.items():
        status = "FOUND" if item["installed"] else "NOT FOUND"
        print(f"\n{item['name']}: {status}")
        print(f"Version: {item['version']}")
        print(f"Path: {item['path']}")

    logger.info("Displayed installed tool status")
    pause()


def install_menu():
    print("\n--- Install tools ---")

    for key, item in TOOL_CATALOG.items():
        print(f"{key}. {item['name']} ({item['description']})")

    choice = input("Enter tool number (or B to go back): ").strip().lower()

    if choice in TOOL_CATALOG:
        install_tool(choice)
    elif choice != "b":
        print("Invalid selection.")

    pause()


def update_menu():
    print("\n--- Update tools ---")

    updates = check_updates()

    if not updates:
        print("No update information available.")
    else:
        for key, item in updates.items():
            print(f"{key}. {item['name']}: {item['message']}")

        choice = input(
            "\nEnter tool number to update (or B to go back): "
        ).strip().lower()

        if choice in updates and updates[choice]["available"]:
            confirm = input(
                f"Update {updates[choice]['name']}? Type YES: "
            ).strip()

            if confirm == "YES":
                update_tool(choice)
            else:
                print("Update cancelled.")

        elif choice != "b":
            print("No available update selected.")

    pause()


def config_menu():
    while True:
        print("\n--- Configuration ---")
        print("1. View current settings")
        print("2. Set path for a tool")
        print("3. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            show_settings()

        elif choice == "2":
            for key, item in TOOL_CATALOG.items():
                print(f"{key}. {item['name']}")

            key = input("Tool number: ").strip()

            if key in TOOL_CATALOG:
                path = input(
                    "Enter full executable path: "
                ).strip().strip('"')

                set_tool_path(key, path)
            else:
                print("Invalid tool number.")

        elif choice == "3":
            break

        else:
            print("Invalid selection.")

        pause()


def main():
    while True:
        print("\n======================================")
        print("       eSim AUTOMATED TOOL MANAGER")
        print("======================================")
        print("1. View installed tools and versions")
        print("2. Install a tool")
        print("3. Check for updates / update a tool")
        print("4. Configure tool paths")
        print("5. Check dependencies")
        print("6. View saved configuration")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            show_tools()

        elif choice == "2":
            install_menu()

        elif choice == "3":
            update_menu()

        elif choice == "4":
            config_menu()

        elif choice == "5":
            run_dependency_check()
            pause()

        elif choice == "6":
            show_settings()
            pause()

        elif choice == "0":
            print("Thank you for using eSim AutoTool Manager.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()