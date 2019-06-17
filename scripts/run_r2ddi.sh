#!/bin/sh

RSCRIPT="/usr/bin/Rscript"

# Rscript lib_R/r2ddi_v2016.2_en.R &
# Rscript lib_R/r2ddi_v2016.2_de.R &

${RSCRIPT} ./lib_R/r2ddi_v2017.0_de.R &
${RSCRIPT} ./lib_R/r2ddi_v2017.0_en.R &
