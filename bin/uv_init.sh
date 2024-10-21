#!/bin/bash
# Initialize the UV tool on Ubuntu.

declare scriptName=uv_init.sh
declare version="0.1"
declare target=

declare IS_VERBOSE=0
declare IS_DEBUG=0
declare IS_TRIAL=0
declare ERRORS=0

#set -e
declare SOURCED=0
[[ "${BASH_SOURCE[0]}" != "${0}" ]] && SOURCED=1
(( SOURCED == 1 )) && SCRIPT="Sourced script $SCRIPTNAME"
declare SCRIPTDIR=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))

#------------------------------------------------------------------------------
declare COLOR_BLACK='\E[30m'
declare COLOR_RED='\E[31m'
declare COLOR_GREEN='\E[32m'
declare COLOR_YELLOW='\E[38;5;226m' # Nicer yellow over '\E[33m'
declare COLOR_BLUE='\E[38;5;027m' # Better contrast  over '\E[34m'
declare COLOR_MAGENTA='\E[35m'
declare COLOR_CYAN='\E[36m'
declare COLOR_WHITE='\E[37m'
declare COLOR_DEFAULT='\E[0m'

declare COLOR_BRIGHT_RED='\E[31;1m'
declare COLOR_BRIGHT_GREEN='\E[32;1m'
declare COLOR_BRIGHT_YELLOW='\E[33;1m'
declare COLOR_BRIGHT_BLUE='\E[34;1m'
declare COLOR_BRIGHT_MAGENTA='\E[35;1m'
declare COLOR_BRIGHT_CYAN='\E[36;1m'
declare COLOR_BRIGHT_WHITE='\E[37;1m'

#------------------------------------------------------------------------------
function __outc() {
  if [[ $# -eq 0 ]]; then
    echo "ERROR -- __outc() called with no args"
    RC=$RC_ERROR
  elif [[ $# -eq 1 ]]; then
    echo "$1"
  else
    local col="$1"
    local str="$2"
    echo -e "$IND$col$str$COLOR_DEFAULT"
  fi
}

function __out_() {
  local col="$1"
  local str="$2"
  echo -en "$IND$col$str$COLOR_DEFAULT"
}

#------------------------------------------------------------------------------
function _outw() {
  # wrap the given function's output with color
  local col=$1
  shift
  output="$("$@" 2>&1)"
  echo -e "$col$output$COLOR_DEFAULT"
}

function _sys()     { __outc "$COLOR_WHITE"         "[SYS] $*" ;}
function _err()     { __outc "$COLOR_RED"           "[ERR] $*" ; (( ERRORS++ )) ; return 0 ;}
function _ok()      { __outc "$COLOR_GREEN"         "[OK] $*"  ;}
function _dcmd()    { __outc "$COLOR_MAGENTA"       "[CMD] $*" ;}
function _warn()    { __outc "$COLOR_YELLOW"        "$*" ;}
function _warn_()   { __out_ "$COLOR_YELLOW"        "$*" ;}
function _good()    { __outc "$COLOR_BRIGHT_GREEN"  "$*" ;}
function _good_()   { __out_ "$COLOR_BRIGHT_GREEN"  "$*" ;}
function _fail()    { __outc "${COLOR_RED}- **FAILED** " "$*" ; (( ERRORS++ )); (( FAILED++ )) ;}
function _info()    { __outc "$COLOR_BRIGHT_CYAN"   "$*" ;}
function _info_()   { __out_ "$COLOR_BRIGHT_CYAN"   "$*" ;}
function _msg()     { __outc "$COLOR_CYAN"          "$*" ;}
function _msg_()    { __out_ "$COLOR_CYAN"          "$*" ;}
function _note()    { __outc "$COLOR_MAGENTA"       "$*" ;}
function _note_()   { __out_ "$COLOR_MAGENTA"       "$*" ;}
function _out()     { __outc "$COLOR_BRIGHT_WHITE"  "$*" ;}
function _out_()    { __out_ "$COLOR_BRIGHT_WHITE"  "$*" ;}
function _warning() { __outc "$COLOR_YELLOW"        "$*" ;}
function _error()   { __outc "$COLOR_RED"           "$*"; (( ERRORS++ )) ; return 0 ;}
function _error_()  { __out_ "$COLOR_RED"           "$*"; (( ERRORS++ )) ; return 0 ;}
function _dbg() { (( IS_DEBUG )) && __outc "$COLOR_MAGENTA" "[DBG] $*" ;}
function _not_implemented() { _err "'$@' is not implemented yet!" ;}

#------------------------------------------------------------------------------
function _is_help() {
  [[ "$1" == '?'    ]] && return 0
  [[ "$1" == '-?'   ]] && return 0
  [[ "$1" == 'h'    ]] && return 0
  [[ "$1" == '-h'   ]] && return 0
  [[ "$1" == '--h'* ]] && return 0
  return 1
}

function _is_arg() {
  local arg=$1
  local flag=$2
  local long=$3
  [[ "$flag" == ''        ]] && return 1
  [[ "$arg"  == "-$flag"  ]] && return 0
  [[ "$long" == ''        ]] && return 1
  [[ "$arg"  == "--$long" ]] && return 0
  return 1
}

function _cmd() {
  local c="$@"
  _dcmd "$c"
  (( IS_TRIAL )) || eval "$c"
  RV=$?
  (( RV )) && _warn "Command [$c] returned [$RV]"
  return $RV
}

#------------------------------------------------------------------------
function scriptUsage()
{
  _out
  _good "Usage: $scriptName [args]"
  _out
  _msg "- Initialize the 'uv' tool for use on a debian based Linux distro."
  _out
  _out "  Args:"
  _msg "    run  : runs the installer and exits."
  _out
  _out "  Options:"
  _msg "    -h, --help     display this help and exit"
  _msg "    -t, --trial    trial mode. Show the commands that would execute"
  _out
  _out "Runs silently and returns if uv is already installed."
  exit
}

#------------------------------------------------------------------------
function init_uv_check()
{
  local cmd="$1"
  local cmd_help_arg="$2"
  local cmd_ok="$3"
  local cmd_path="$(type -p $cmd)"
  (( IS_VERBOSE )) && _good "- Located '$cmd' at '$cmd_path'"
  if [[ -z "$cmd_path" ]] ; then
    _error "*** '$cmd' is missing."
  else
    (( IS_VERBOSE )) && _good "The '$cmd' is available."
    x=$($cmd $cmd_help_arg)
    if [[ "$x" == *"$cmd_ok"* ]] ; then
      (( IS_VERBOSE )) && _good "- '$cmd' command installation validated."
    else
      _error "*** '$cmd' check failed!"
    fi
  fi
}

#------------------------------------------------------------------------
function install_missing()
{
  local cmd="$1"
  local cmd_install="$2"
  local cmd_path="$(type -p $cmd)"
  (( IS_VERBOSE )) && _good "- Located '$cmd' at '$cmd_path'"
  if [[ -z "$cmd_path" ]] ; then
    _msg "- Installing '$cmd' with 'cmd_install'."
    _cmd $cmd_install
  fi
}

#------------------------------------------------------------------------
function main()
{
  for arg in $@ ; do _is_help $arg && scriptUsage ; done
  _is_arg "$1" t trial   && IS_TRIAL=1
  _is_arg "$1" v verbose && IS_VERBOSE=1
  init_uv_check 'curl' '--help' 'Usage: curl'
  init_uv_check 'uv'   '--help' 'Python package manager'
  init_uv_check 'uvx'  '--help' 'Run a command'
  if (( ERRORS )) ; then
    install_missing 'curl' 'sudo apt install -y curl'
    install_missing 'uvx'  'curl -LsSf https://astral.sh/uv/install.sh | sh'
  fi
}

#------------------------------------------------------------------------
main $@
