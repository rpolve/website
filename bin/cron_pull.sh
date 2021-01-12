#!/usr/bin/env bash

__timestamp() {
printf "[%s] >>> %s\n" "$(date '+%F %T')" "$1"
}

LOGFILE="/tmp/$(basename -s '.sh' $0).log"
LOCKFILE="${LOGFILE/.log/.lock}"

if [ -e "$LOCKFILE" ] && kill -0 $(cat "$LOCKFILE"); then
    __timestamp "Already running." >>$LOGFILE
    exit 1
fi

trap "rm -f $LOCKFILE; exit" INT TERM EXIT
echo $$ > "$LOCKFILE"

cd $HOME/website && direnv allow || exit 1

git remote update >/dev/null 2>&1
LOCAL=$(git rev-parse @{0})
REMOTE=$(git rev-parse @{u})

if [ $LOCAL != $REMOTE ]; then
    __timestamp BEGIN
    git reset --hard HEAD &&
        git pull --recurse-submodules &&
        make
    __timestamp END
fi >>$LOGFILE 2>&1
