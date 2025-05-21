import os
import shutil
from pathlib import Path


def copy_allauth_templates():
    try:
        # Automatically find allauth installation path
        import allauth
        allauth_path = Path(allauth.__file__).parent
        src = allauth_path / "templates" / "account"

        # Verify source exists
        if not src.exists():
            print(f"Error: Source directory not found at {src}")
            print("Make sure django-allauth is installed in your virtual environment")
            return False

        # Set destination path
        dst = Path("templates") / "account"
        dst.mkdir(parents=True, exist_ok=True)

        # Copy files
        for item in src.iterdir():
            target = dst / item.name
            if item.is_file():
                shutil.copy2(item, target)
                print(f"Copied: {item.name}")
            elif item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
                print(f"Copied directory: {item.name}")

        print(f"\nSuccess! Templates copied to: {dst}")
        return True

    except ImportError:
        print("Error: django-allauth not installed. Run: pip install django-allauth")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return False


if __name__ == "__main__":
    copy_allauth_templates()
