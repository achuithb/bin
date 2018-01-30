alias dir='ls -ltF'

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
if [ -f '/usr/local/google/home/achuith/code/google-cloud-sdk/path.bash.inc' ]; then source '/usr/local/google/home/achuith/code/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/usr/local/google/home/achuith/code/google-cloud-sdk/completion.bash.inc' ]; then source '/usr/local/google/home/achuith/code/google-cloud-sdk/completion.bash.inc'; fi
