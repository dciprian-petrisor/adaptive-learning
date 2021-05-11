#!/bin/bash -e

if ! [[ -z ${var+x} ]]; then
  echo "HOME variable is not defined. Please define it and try again.";
  exit 1;
fi

if ! [[ -f "$HOME/.secrethub/credential" ]]; then
    echo "Failed to find credential file in $HOME/.secrethub/credential"
    exit 1;
fi

SECRETHUB_CREDENTIAL=$(cat "$HOME/.secrethub/credential")

export SECRETHUB_CREDENTIAL