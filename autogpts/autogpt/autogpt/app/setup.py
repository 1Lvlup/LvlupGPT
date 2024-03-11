"""Set up the AI and its goals"""
import logging
from typing import Optional

from autogpt.app.utils import clean_input
from autogpt.config import AIDirectives, AIProfile, Config
from autogpt.logs.helpers import print_attribute

# Initialize the logger for this module
logger = logging.getLogger(__name__)


def apply_overrides_to_ai_settings(
    ai_profile: AIProfile,  # The AI profile to apply overrides to
    directives: AIDirectives,  # The AI directives to apply overrides to
    override_name: Optional[str] = "",  # Optional override for AI name
    override_role: Optional[str] = "",  # Optional override for AI role
    replace_directives: bool = False,  # Replace existing directives or add to them
    resources: Optional[list[str]] = None,  # Optional list of resource overrides
    constraints: Optional[list[str]] = None,  # Optional list of constraint overrides
    best_practices: Optional[list[str]] = None,  # Optional list of best practice overrides
):
    """
    Apply overrides to AI settings.

    This function allows you to override various attributes of the AI profile and
    directives. You can override the AI name and role, as well as add, remove, or
    replace resources, constraints, and best practices.

    Args:
        ai_profile (AIProfile): The AI profile to apply overrides to.
        directives (AIDirectives): The AI directives to apply overrides to.
        override_name (Optional[str], optional): Optional override for AI name.
            Defaults to "".
        override_role (Optional[str], optional): Optional override for AI role.
            Defaults to "".
        replace_directives (bool, optional): Replace existing directives or add to them.
            Defaults to False.
        resources (Optional[list[str]], optional): Optional list of resource overrides.
            Defaults to None.
        constraints (Optional[list[str]], optional): Optional list of constraint overrides.
            Defaults to None.
        best_practices (Optional[list[str]], optional): Optional list of best practice overrides.
            Defaults to None.
    """
    if override_name:
        ai_profile.ai_name = override_name
    if override_role:
        ai_profile.ai_role = override_role

    if replace_directives:
        if resources:
            directives.resources = resources
        if constraints:
            directives.constraints = constraints
        if best_practices:
            directives.best_practices = best_practices
    else:
        if resources:
            directives.resources += resources
        if constraints:
            directives.constraints += constraints
        if best_practices:
            directives.best_practices += best_practices


async def interactively_revise_ai_settings(
    ai_profile: AIProfile,
    directives: AIDirectives,
    app_config: Config,
):
    """
    Interactively revise the AI settings.

    This function allows you to revise the AI profile and directives through an
    interactive prompt. You can change the AI name and role, add, remove, or
    modify constraints, resources, and best practices.

    Args:
        ai_profile (AIProfile): The current AI profile.
        ai_directives (AIDirectives): The current AI directives.
        app_config (Config): The application configuration.

    Returns:
        AIProfile: The revised AI settings.
    """
    logger = logging.getLogger("revise_ai_profile")

    revised = False

    while True:
        # Print the current AI configuration
        print_ai_settings(
            title="Current AI Settings" if not revised else "Revised AI Settings",
            ai_profile=ai_profile,
            directives=directives,
            logger=logger,
        )

        # Ask the user if they want to continue with the current settings
        if (
            await clean_input(app_config, "Continue with these settings? [Y/n]")
            or app_config.authorise_key
        ) == app_config.authorise_key:
            break

        # Revise the AI profile
        ai_profile.ai_name = (
            await clean_input(
                app_config, "Enter AI name (or press enter to keep current):"
            )
            or ai_profile.ai_name
        )
        ai_profile.ai_role = (
            await clean_input(
                app_config, "Enter new AI role (or press enter to keep current):"
            )
            or ai_profile.ai_role
        )

        # Revise constraints
        i = 0
        while i < len(directives.constraints):
            constraint = directives.constraints[i]
            print_attribute(f"Constraint {i+1}:", f'"{constraint}"')
            new_constraint = (
                await clean_input(
                    app_config,
                    f"Enter new constraint {i+1}"
                    " (press enter to keep current, or '-' to remove):",
                )
                or constraint
            )

            if new_constraint == "-":
                directives.constraints.remove(constraint)
                continue
            elif new_constraint:
                directives.constraints[i] = new_constraint

            i += 1

        # Add new constraints
        while True:
            new_constraint = await clean_input(
                app_config,
                "Press enter to finish, or enter a constraint to add:",
            )
            if not new_constraint:
                break
            directives.constraints.append(new_constraint)

        # Revise resources
        i = 0
        while i < len(directives.resources):
            resource = directives.resources[i]
            print_attribute(f"Resource {i+1}:", f'"{resource}"')
            new_resource = (
                await clean_input(
                    app_config,
                    f"
