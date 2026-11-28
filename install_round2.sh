#!/bin/bash
# 🦕 old-tongues round 2: install APL, SNOBOL4 and Forth on the Consortium.
# The password arrives in a 600 file and is deleted on the first line.
set -u
PW=$(cat ~/.ot2pw); rm -f ~/.ot2pw
L=/home/Ace/old_tongues/round2_install.log; : > $L
echo "== gforth (apt)" >>$L
echo "$PW" | sudo -S apt-get install -y gforth >>$L 2>&1
echo "== build deps" >>$L
echo "$PW" | sudo -S apt-get install -y build-essential libncurses-dev autoconf automake libtool m4 >>$L 2>&1
mkdir -p /home/Ace/src && cd /home/Ace/src
echo "== CSNOBOL4" >>$L
wget -q https://www.regressive.org/snobol4/csnobol4/curr/snobol4-2.3.3.tar.gz -O snobol4.tgz >>$L 2>&1 || wget -q https://ftp.regressive.org/snobol4/snobol4-2.3.3.tar.gz -O snobol4.tgz >>$L 2>&1
D=$(tar tzf snobol4.tgz 2>>$L | head -1 | cut -d/ -f1)
tar xzf snobol4.tgz >>$L 2>&1 && cd "$D" && ./configure --prefix=/home/Ace/snobol4 >>$L 2>&1 && make -j8 >>$L 2>&1 && make install >>$L 2>&1
cd /home/Ace/src
echo "== GNU APL" >>$L
wget -q https://ftp.gnu.org/gnu/apl/apl-1.9.tar.gz -O apl.tgz >>$L 2>&1 || wget -q https://ftp.gnu.org/gnu/apl/apl-1.8.tar.gz -O apl.tgz >>$L 2>&1
D=$(tar tzf apl.tgz 2>>$L | head -1 | cut -d/ -f1)
tar xzf apl.tgz >>$L 2>&1 && cd "$D" && ./configure --prefix=/home/Ace/gnuapl >>$L 2>&1 && make -j8 >>$L 2>&1 && make install >>$L 2>&1
echo "== RESULT" >>$L
for b in /usr/bin/gforth /home/Ace/snobol4/bin/snobol4 /home/Ace/gnuapl/bin/apl; do ls -l $b >>$L 2>&1 || echo "MISSING $b" >>$L; done
echo DONE >>$L
