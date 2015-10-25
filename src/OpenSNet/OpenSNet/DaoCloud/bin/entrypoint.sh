#!/bin/sh

echo "OpenSNet Starting..."

if [[ -z "$USERNAME" ]]; then
	echo "You have to set USERNAME"
	exit 1
fi

if [[ -z "$IPADDRESS" ]]; then
	echo "You have to set IPADDRESS"
	exit 1
fi

exec "$@" "-u" "$USERNAME" "-i" "$IPADDRESS" "-I" "$INTERVAL" "-t" "$TARGET" "-P" "$PORT"