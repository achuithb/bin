# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    # WARNING: enabling this can cause multi-second delays due to NFS latency
    #alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -AltF'
alias dir='ls -ltF'
alias la='ls -A'
alias l='ls -CF'

alias gitupdate='git branch --set-upstream-to=master; git commit -a --fixup=HEAD; git rebase -i --autosquash'
alias gitupload='git branch --set-upstream-to=origin/master; git cl upload; git branch --set-upstream-to=master'
alias myssh='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/code/chrome/src/third_party/chromite/ssh_keys/testing_rsa $@'
alias myscp='scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/code/chrome/src/third_party/chromite/ssh_keys/testing_rsa $@'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

###BEGIN SSH-AGENT ENVIRONMENT SETUP###
# determine if ssh-agent is running properly
export SSH_AGENT_FILE=$HOME/.ssh/agent-stuff.$HOSTNAME

# Try to copy the existing agent stuff into the environment
[ -r $SSH_AGENT_FILE ] && . $SSH_AGENT_FILE &&
    ssh-add -l >/dev/null 2>&1

if [ $? != 0 ] ; then
    # start ssh-agent, and put stuff into the environment
    ssh-agent | grep -v "^echo Agent pid" > $SSH_AGENT_FILE
    . $SSH_AGENT_FILE
    ssh-add
fi
###END SSH-AGENT ENVIRONMENT SETUP ###

# for perforce
export P4CONFIG=.p4config
export P4DIFF=/home/build/public/google/tools/p4diff
export P4MERGE=/home/build/public/eng/perforce/mergep4.tcl
export P4EDITOR=$EDITOR

umask 022

# Build customizations - depot_tools, goma, gold.
PATH=$HOME/code/bin:$HOME/code/depot_tools:$HOME/code/goma:/usr/local/gold/bin:$PATH

# for Eclipse
export profile=final
export ECLIPSE_VERSION=eclipse38
export ECLIPSE_MEM_MAX="3072M"
export ECLIPSE_MEM_START="2048M"

#for goma
GOMA_DIR=${HOME}/code/goma

# for gyp
export GYP_GENERATORS="ninja"

#for pyauto
export PYTHONPATH=/usr/local/buildtools/current/sitecustomize

# linux sandbox
export CHROME_DEVEL_SANDBOX=/usr/local/sbin/chrome-devel-sandbox

# The next line updates PATH for the Google Cloud SDK.
if [ -f /usr/local/google/home/achuith/code/google-cloud-sdk/path.bash.inc ]; then
  source '/usr/local/google/home/achuith/code/google-cloud-sdk/path.bash.inc'
fi

# The next line enables shell command completion for gcloud.
if [ -f /usr/local/google/home/achuith/code/google-cloud-sdk/completion.bash.inc ]; then
  source '/usr/local/google/home/achuith/code/google-cloud-sdk/completion.bash.inc'
fi
