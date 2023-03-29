<<<<<<< HEAD
# This file must be used with "source <venv>/bin/activate.fish" *from fish*
# (https://fishshell.com/); you cannot run it directly.

function deactivate  -d "Exit virtual environment and return to normal shell environment"
=======
# This file must be used with ". bin/activate.fish" *from fish* (http://fishshell.org)
# you cannot run it directly

function deactivate  -d "Exit virtualenv and return to normal shell environment"
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME $_OLD_VIRTUAL_PYTHONHOME
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
        functions -e fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
    end

    set -e VIRTUAL_ENV
<<<<<<< HEAD
    set -e VIRTUAL_ENV_PROMPT
    if test "$argv[1]" != "nondestructive"
        # Self-destruct!
=======
    if test "$argv[1]" != "nondestructive"
        # Self destruct!
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
        functions -e deactivate
    end
end

<<<<<<< HEAD
# Unset irrelevant variables.
deactivate nondestructive

set -gx VIRTUAL_ENV "/Users/potato_cat/Desktop/onboarding_team_7/venv"
=======
# unset irrelevant variables
deactivate nondestructive

set -gx VIRTUAL_ENV "/Users/choyumin/Desktop/sparta/onboarding/onboarding_team_7/venv"
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH

<<<<<<< HEAD
# Unset PYTHONHOME if set.
=======
# unset PYTHONHOME if set
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # fish uses a function instead of an env var to generate the prompt.

<<<<<<< HEAD
    # Save the current fish_prompt function as the function _old_fish_prompt.
    functions -c fish_prompt _old_fish_prompt

    # With the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command.
        set -l old_status $status

        # Output the venv prompt; color taken from the blue of the Python logo.
        printf "%s%s%s" (set_color 4B8BBE) "(venv) " (set_color normal)

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        # Output the original/"old" prompt.
=======
    # save the current fish_prompt function as the function _old_fish_prompt
    functions -c fish_prompt _old_fish_prompt

    # with the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command
        set -l old_status $status

        # Prompt override?
        if test -n "(venv) "
            printf "%s%s" "(venv) " (set_color normal)
        else
            # ...Otherwise, prepend env
            set -l _checkbase (basename "$VIRTUAL_ENV")
            if test $_checkbase = "__"
                # special case for Aspen magic directories
                # see http://www.zetadev.com/software/aspen/
                printf "%s[%s]%s " (set_color -b blue white) (basename (dirname "$VIRTUAL_ENV")) (set_color normal)
            else
                printf "%s(%s)%s" (set_color -b blue white) (basename "$VIRTUAL_ENV") (set_color normal)
            end
        end

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
<<<<<<< HEAD
    set -gx VIRTUAL_ENV_PROMPT "(venv) "
=======
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
end
