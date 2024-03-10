"""AutoGPT: A GPT-powered AI Assistant"""

import autogpt.app.cli

if __name__ == "__main__":
    print(f"Starting {__name__}...")
    autogpt.app.cli.cli()
    print(f"{__name__} finished.")
