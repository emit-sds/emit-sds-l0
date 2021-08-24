#!/bin/bash

IN_DIR=$1
OUT_DIR=$2
REPORT_LOG=$3
CCSDS_CHECK_SCRIPT=$4
L0_PROC_EXE=$5
 
if [ -d ${OUT_DIR} ]; then
    rm -r ${OUT_DIR}
fi
mkdir -p ${OUT_DIR}
 
if [ -f ${REPORT_LOG} ]; then
    rm ${REPORT_LOG}
fi
 

${L0_PROC_EXE} --input-dir ${IN_DIR} --output-dir ${OUT_DIR}
IN_FILE=${IN_DIR}/*hsc.bin
PROC_FILE=`ls ${OUT_DIR}/*.bin | sort | tail -1`
LAST_OUTPUT_FILE=`basename ${PROC_FILE} | cut -d'.' -f1`
REPORT_FILE=`ls ${OUT_DIR}/*_report.txt | sort | tail -1`

RENAMED_PROC_FILE=${OUT_DIR}/${LAST_OUTPUT_FILE}_l0_ccsds.bin
RENAMED_REPORT_FILE=${OUT_DIR}/${LAST_OUTPUT_FILE}_l0_ccsds_report.txt

mv ${PROC_FILE} ${RENAMED_PROC_FILE}
mv ${REPORT_FILE} ${RENAMED_REPORT_FILE}

ORIG_SIZE=`stat -c %s ${IN_FILE}`
PROC_SIZE=`stat -c %s ${RENAMED_PROC_FILE}`
PROC_PKT_CNT=`grep "Packet count" ${RENAMED_REPORT_FILE} | cut -d":" -f2 | xargs`

# A HOSC EHS packet consists of a 16-byte `Primary Header`, followed by a
# 12-byte `Secondary Header`, and then followed by a CCSDS Packet.
HOSC_HEADER_SIZE=28

CCSDS_CNT_CHECK=`python ${CCSDS_CHECK_SCRIPT} ${RENAMED_PROC_FILE} 2>&1 | tail -1`

echo "-----------------------------" >> ${REPORT_LOG}
echo "${PROC_FILE} Proc Report" >> ${REPORT_LOG}
echo "-----------------------------" >> ${REPORT_LOG}
echo "Processed File: ${RENAMED_PROC_FILE}" >> ${REPORT_LOG}
echo "Report File: ${RENAMED_REPORT_FILE}\n" >> ${REPORT_LOG}
echo "Original File Size: ${ORIG_SIZE}" >> ${REPORT_LOG}
echo "Processed File Size: ${PROC_SIZE}" >> ${REPORT_LOG}
echo "CCSDS Count Check: ${CCSDS_CNT_CHECK}" >> ${REPORT_LOG}
echo "Processed Packet Count: ${PROC_PKT_CNT}" >> ${REPORT_LOG}
echo "Removed Header Size: $((${HOSC_HEADER_SIZE} * ${PROC_PKT_CNT}))" >> ${REPORT_LOG}
echo "File Size Match: $((${ORIG_SIZE} - ${HOSC_HEADER_SIZE} * ${PROC_PKT_CNT} == ${PROC_SIZE}))" >> ${REPORT_LOG}
echo "\n"
echo "Any incorrectly ordered packet errors (Nothing here is good):" >> ${REPORT_LOG}
echo `grep "Encountered an out of order packet" ${RENAMED_REPORT_FILE}` >> ${REPORT_LOG}
echo `grep "Encountered out of order PSC" ${RENAMED_REPORT_FILE}` >> ${REPORT_LOG}
echo "\n"
echo "Processed CCSDS Packet Count Check: $((${CCSDS_CNT_CHECK} == ${PROC_PKT_CNT}))" >> ${REPORT_LOG}
echo "\n"

