#!/usr/bin/env bash

# Run on separate sessions to speed up processing
for d in {0000..0500};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {0501..1000};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {1001..1500};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {1501..2000};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {2001..2200};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {2201..2300};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {2301..2400};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {2401..2500};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done

for d in {2501..2657};
do
  if [[ -d $d ]]; then
    for f in $(ls $d | cut -d '.' -f 1);
    do
      echo $d/$f && ../bin/ris2xml -un $d/$f.ris | ../bin/xml2bib --no-bom -sd -nl > $d/$f.bib;
    done
  fi
done
