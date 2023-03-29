# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

<<<<<<< HEAD
alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'
=======
alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; test "\!:*" != "nondestructive" && unalias deactivate'
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
setenv VIRTUAL_ENV "/Users/potato_cat/Desktop/onboarding_team_7/venv"
=======
setenv VIRTUAL_ENV "/Users/choyumin/Desktop/sparta/onboarding/onboarding_team_7/venv"
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
<<<<<<< HEAD
    set prompt = "(venv) $prompt"
    setenv VIRTUAL_ENV_PROMPT "(venv) "
=======
    if ("venv" != "") then
        set env_name = "venv"
    else
        if (`basename "VIRTUAL_ENV"` == "__") then
            # special case for Aspen magic directories
            # see http://www.zetadev.com/software/aspen/
            set env_name = `basename \`dirname "$VIRTUAL_ENV"\``
        else
            set env_name = `basename "$VIRTUAL_ENV"`
        endif
    endif
    set prompt = "[$env_name] $prompt"
    unset env_name
>>>>>>> c160edca4ffc7efe18c2dcd02e4b294a6e2f6679
endif

alias pydoc python -m pydoc

rehash
