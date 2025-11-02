#!/usr/bin/env python3
"""
API Key Setup Helper for ScholaRAG

This script helps users set up API keys for academic databases.
It creates/updates the .env file in your project directory.

Usage:
    python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject
    python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject --key SEMANTIC_SCHOLAR_API_KEY

Author: ScholaRAG Team
Version: 1.2.4
"""

import argparse
import sys
from pathlib import Path
import re


class APIKeySetup:
    """Helper class for setting up API keys in .env files"""

    SUPPORTED_KEYS = {
        'SEMANTIC_SCHOLAR_API_KEY': {
            'name': 'Semantic Scholar',
            'url': 'https://www.semanticscholar.org/product/api#api-key',
            'description': 'FREE API key for Semantic Scholar (1000 requests/5min)',
            'required': True,
            'validation': lambda k: len(k) >= 20,
            'error_msg': 'API key should be at least 20 characters'
        },
        'OPENAI_API_KEY': {
            'name': 'OpenAI',
            'url': 'https://platform.openai.com/api-keys',
            'description': 'API key for OpenAI (for AI-PRISMA screening)',
            'required': False,
            'validation': lambda k: k.startswith('sk-'),
            'error_msg': 'OpenAI API key should start with "sk-"'
        },
        'ANTHROPIC_API_KEY': {
            'name': 'Anthropic Claude',
            'url': 'https://console.anthropic.com/settings/keys',
            'description': 'API key for Claude AI (for AI-PRISMA screening)',
            'required': False,
            'validation': lambda k: len(k) >= 20,
            'error_msg': 'API key should be at least 20 characters'
        }
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.env_path = self.project_path / ".env"

        # Validate project path
        if not self.project_path.exists():
            print(f"❌ Error: Project path does not exist: {self.project_path}")
            sys.exit(1)

    def show_welcome(self):
        """Show welcome message"""
        print("\n" + "="*80)
        print("🔑 ScholaRAG API Key Setup")
        print("="*80)
        print(f"\nProject: {self.project_path}")
        print(f".env file: {self.env_path}")
        print()

    def setup_key(self, key_name: str, interactive: bool = True) -> bool:
        """
        Set up a specific API key.

        Args:
            key_name: Name of the API key (e.g., 'SEMANTIC_SCHOLAR_API_KEY')
            interactive: If True, prompt user for input. If False, show instructions only.

        Returns:
            True if key was set up successfully
        """
        if key_name not in self.SUPPORTED_KEYS:
            print(f"❌ Unknown API key: {key_name}")
            print(f"   Supported keys: {', '.join(self.SUPPORTED_KEYS.keys())}")
            return False

        config = self.SUPPORTED_KEYS[key_name]

        print("\n" + "-"*80)
        print(f"🔑 Setting up: {config['name']}")
        print("-"*80)
        print(f"Description: {config['description']}")
        print(f"Get API key: {config['url']}")
        if config['required']:
            print("Status: ⚠️  REQUIRED for this database")
        else:
            print("Status: ℹ️  Optional (but recommended)")
        print()

        if not interactive:
            print("ℹ️  Non-interactive mode. Showing instructions only.")
            print(f"\nTo add manually:")
            print(f"  1. Get API key from: {config['url']}")
            print(f"  2. Add to {self.env_path}:")
            print(f"     {key_name}=your_key_here")
            return False

        # Prompt for API key
        api_key = input(f"Enter your {config['name']} API key (or press Enter to skip): ").strip()

        if not api_key:
            if config['required']:
                print(f"⚠️  Warning: This API key is REQUIRED for {config['name']}")
                print(f"   You can add it later to: {self.env_path}")
            else:
                print(f"⏩ Skipped {config['name']} API key")
            return False

        # Validate API key
        if not config['validation'](api_key):
            print(f"❌ Invalid API key: {config['error_msg']}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry == 'y':
                return self.setup_key(key_name, interactive)
            return False

        # Save to .env file
        self.save_key(key_name, api_key)
        print(f"✅ {config['name']} API key saved successfully!")
        return True

    def save_key(self, key_name: str, api_key: str):
        """
        Save API key to .env file.

        Args:
            key_name: Name of the environment variable
            api_key: API key value
        """
        # Read existing .env content
        if self.env_path.exists():
            with open(self.env_path, 'r') as f:
                env_content = f.read()
        else:
            env_content = "# ScholaRAG Project Environment\n# API Keys\n\n"

        # Check if key already exists
        pattern = f"{key_name}=.*"
        if re.search(pattern, env_content):
            # Replace existing key
            env_content = re.sub(pattern, f"{key_name}={api_key}", env_content)
            print(f"   Updated existing {key_name}")
        else:
            # Append new key
            env_content += f"\n# {self.SUPPORTED_KEYS[key_name]['name']} API\n"
            env_content += f"{key_name}={api_key}\n"
            print(f"   Added {key_name}")

        # Write to .env file
        with open(self.env_path, 'w') as f:
            f.write(env_content)

    def show_status(self):
        """Show current status of API keys"""
        print("\n" + "="*80)
        print("📊 API Key Status")
        print("="*80)

        if not self.env_path.exists():
            print("⚠️  No .env file found")
            print(f"   Will be created at: {self.env_path}")
            return

        # Read .env file
        with open(self.env_path, 'r') as f:
            env_content = f.read()

        # Check each key
        for key_name, config in self.SUPPORTED_KEYS.items():
            pattern = f"{key_name}=(.+)"
            match = re.search(pattern, env_content)

            if match:
                api_key = match.group(1).strip()
                masked = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
                status = "✅ SET"
                print(f"{status} {config['name']}: {masked}")
            else:
                status = "❌ MISSING" if config['required'] else "⚠️  NOT SET"
                print(f"{status} {config['name']}")

        print()

    def setup_all_keys(self, interactive: bool = True):
        """Set up all API keys"""
        print("\n📋 Setting up all API keys...\n")

        # Set up required keys first
        for key_name, config in self.SUPPORTED_KEYS.items():
            if config['required']:
                self.setup_key(key_name, interactive)

        # Ask about optional keys
        print("\n" + "-"*80)
        print("ℹ️  Optional API Keys")
        print("-"*80)
        print("The following keys are optional but recommended for AI-PRISMA screening:")

        for key_name, config in self.SUPPORTED_KEYS.items():
            if not config['required']:
                print(f"\n   • {config['name']}: {config['description']}")

        if interactive:
            setup_optional = input("\nSet up optional keys now? (y/n): ").strip().lower()
            if setup_optional == 'y':
                for key_name, config in self.SUPPORTED_KEYS.items():
                    if not config['required']:
                        self.setup_key(key_name, interactive)

    def show_completion(self):
        """Show completion message"""
        print("\n" + "="*80)
        print("✅ API Key Setup Complete!")
        print("="*80)
        print(f"\n.env file location: {self.env_path}")
        print("\n🚀 Next steps:")
        print("   1. Start fetching papers:")
        print(f"      python scripts/01_fetch_papers.py --project {self.project_path} --query \"your query\"")
        print("\n   2. View your API key status:")
        print(f"      python scripts/setup_api_keys.py --project {self.project_path} --status")
        print("\n📚 Documentation: https://github.com/HosungYou/ScholaRAG")
        print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Set up API keys for ScholaRAG project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup for all keys
  python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject

  # Set up specific key only
  python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject --key SEMANTIC_SCHOLAR_API_KEY

  # Check API key status
  python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject --status

  # Non-interactive mode (show instructions only)
  python scripts/setup_api_keys.py --project projects/2025-01-01_MyProject --no-interactive
        """
    )

    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory (e.g., projects/2025-01-01_MyProject)'
    )
    parser.add_argument(
        '--key',
        choices=list(APIKeySetup.SUPPORTED_KEYS.keys()),
        help='Set up specific API key only (default: all required keys)'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current API key status and exit'
    )
    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Non-interactive mode (show instructions only)'
    )

    args = parser.parse_args()

    # Create setup instance
    setup = APIKeySetup(args.project)

    # Show welcome
    setup.show_welcome()

    # Handle status check
    if args.status:
        setup.show_status()
        return

    # Show current status first
    setup.show_status()

    # Set up keys
    interactive = not args.no_interactive

    if args.key:
        # Set up specific key
        setup.setup_key(args.key, interactive)
    else:
        # Set up all keys
        setup.setup_all_keys(interactive)

    # Show completion
    if interactive:
        setup.show_completion()
    else:
        print("\nℹ️  To complete setup, add API keys to:")
        print(f"   {setup.env_path}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏩ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
