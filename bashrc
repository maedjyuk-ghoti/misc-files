# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
. /etc/bashrc
fi

# User specific aliases and functions
alias ssr=simplescreenrecorder
alias pc=pyclean.sh

# Aliases
alias doc="cd ~/Documents"
alias vg="cd ~/Documents/372vidya/BEG_cpsc372_sum14/Core"

alias ll="ls -l"
alias la="ls -a"
alias l.="ls -al"

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

alias v=vim
alias c=clear
alias m=make
alias mc="make clean"

# Add environment variable COCOS_CONSOLE_ROOT for cocos2d-x
export COCOS_CONSOLE_ROOT=/home/clouds/cocos2d-x/tools/cocos2d-console/bin
export PATH=$COCOS_CONSOLE_ROOT:$PATH

# Add environment variable ANT_ROOT for cocos2d-x
export ANT_ROOT=/usr/bin
export PATH=$ANT_ROOT:$PATH
