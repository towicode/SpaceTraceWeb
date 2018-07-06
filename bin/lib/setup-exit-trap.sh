#!/usr/bin/env sh
# Hagan Franks 2016-09-13 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu

exitscript()
{
  # echo "exit called: $?"
  exit $?
}

trap exitscript EXIT

return 0