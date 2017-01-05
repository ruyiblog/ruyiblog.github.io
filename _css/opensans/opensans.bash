#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for WEIGHT in 300 400 700 800; do

cat << EOF
@font-face {
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: ${WEIGHT};
  src: url(data:application/x-font-woff;charset=utf-8;base64,$(cat ${DIR}/${WEIGHT}.woff | base64 -w 0)) format('woff');
}
EOF

done
