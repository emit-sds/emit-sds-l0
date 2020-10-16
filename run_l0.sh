#!/bin/bash
# TODO: Update this if you don't have ZSH

IN_FILE=$1
OUT_DIR=$2
REPORT_LOG=$3
CCSDS_CHECK_SCRIPT=$4
 
if [ -d ${OUT_DIR} ]; then
    rm -r ${OUT_DIR}
fi
mkdir -p ${OUT_DIR}
 
if [ -f ${REPORT_LOG} ]; then
    rm ${REPORT_LOG}
fi
 

$5 --input-file ${IN_FILE} --output-dir ${OUT_DIR}
PROC_FILE=`ls ${OUT_DIR}/*.bin | sort | tail -1`
LAST_OUTPUT_FILE=`basename ${PROC_FILE} | cut -d'.' -f1`
NEW_REPORT_FILE=${OUT_DIR}/${LAST_OUTPUT_FILE}_report.txt

mv ${OUT_DIR}/1482_report.txt ${NEW_REPORT_FILE}

ORIG_SIZE=`stat -f%z ${IN_FILE}`
PROC_SIZE=`stat -f%z ${PROC_FILE}`
PROC_PKT_CNT=`grep "Packet count" ${NEW_REPORT_FILE} | cut -d":" -f2 | xargs`

# A HOSC EHS packet consists of a 16-byte `Primary Header`, followed by a
# 12-byte `Secondary Header`, and then followed by a CCSDS Packet.
HOSC_HEADER_SIZE=28

CCSDS_CNT_CHECK=`python ${CCSDS_CHECK_SCRIPT} ${PROC_FILE} 2>&1 | tail -1`

echo "-----------------------------" >> ${REPORT_LOG}
echo "${IN_FILE} Proc Report" >> ${REPORT_LOG}
echo "-----------------------------" >> ${REPORT_LOG}
echo "Processed File: ${PROC_FILE}" >> ${REPORT_LOG}
echo "Report File: ${NEW_REPORT_FILE}\n" >> ${REPORT_LOG}
echo "Original File Size: ${ORIG_SIZE}" >> ${REPORT_LOG}
echo "Processed File Size: ${PROC_SIZE}" >> ${REPORT_LOG}
echo "CCSDS Count Check: ${CCSDS_CNT_CHECK}" >> ${REPORT_LOG}
echo "Processed Packet Count: ${PROC_PKT_CNT}" >> ${REPORT_LOG}
echo "Removed Header Size: $((${HOSC_HEADER_SIZE} * ${PROC_PKT_CNT}))" >> ${REPORT_LOG}
echo "File Size Match: $(($ORIG_SIZE - ${HOSC_HEADER_SIZE} * ${PROC_PKT_CNT} == ${PROC_SIZE}))" >> ${REPORT_LOG}
echo "\n"
echo "Any incorrectly ordered packet errors (Nothing here is good):" >> ${REPORT_LOG}
echo `grep "Encountered an out of order packet" ${NEW_REPORT_FILE}` >> ${REPORT_LOG}
echo `grep "Encountered out of order PSC" ${NEW_REPORT_FILE}` >> ${REPORT_LOG}
echo "\n"
#echo "Processed CCSDS Packet Count Check: $((${CCSDS_CNT_CHECK} == ${PROC_PKT_CNT}))" >> ${REPORT_LOG}
if [[ ${CCSDS_CNT_CHECK} == ${PROC_PKT_CNT}  ]]
then
    echo "Processed CCSDS Packet Count Check: 1" >> ${REPORT_LOG}
else
    echo "Processed CCSDS Packet Count Check: 0" >> ${REPORT_LOG}
fi
echo "\n"

