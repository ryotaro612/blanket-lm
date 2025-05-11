


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Get the path to the current script
    script_path = Path(__file__).resolve()

    # Get the parent directory of the script
    parent_dir = script_path.parent

    # Add the parent directory to sys.path
    sys.path.append(str(parent_dir))