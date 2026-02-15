#!/usr/bin/env python3
import argparse
import json
import logging
import socket
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from models import ReadSummary, FastqSummary

# -------------------------
# Constants (configuration)
# -------------------------
OUTPUT_JSON = 'fastq_summary.json'

# -------------------------
# Logging setup
# -------------------------
parser = argparse.ArgumentParser(description='Summarize FASTQ file and output JSON summary')
parser.add_argument(
    '-l', '--loglevel',
    required=False,
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    default='WARNING',
    help='Set the logging level (default: WARNING)'
)
parser.add_argument(
    '-f', '--fastqfile',
    type=str,
    required=True,
    help='The path to the input FASTQ file'
)
parser.add_argument(
    '-e', '--encoding',
    choices=['fastq-sanger', 'fastq-solexa', 'fastq-illumina'],
    default='fastq-sanger',
    help='The FASTQ encoding format (default: fastq-sanger)'
)
parser.add_argument(
    '-o', '--output',
    type=str,
    default=OUTPUT_JSON,
    help=f'The path to the output JSON file (default: {OUTPUT_JSON})'
)
args = parser.parse_args()

format_string = (
    f'[%(asctime)s {socket.gethostname()}] '
    '%(module)s.%(funcName)s:%(lineno)s - %(levelname)s - %(message)s'
)
logging.basicConfig(level=args.loglevel, format=format_string)

# -------------------------
# Functions
# -------------------------
def summarize_record(record: SeqRecord) -> ReadSummary:
    """
    Given a single FASTQ record, extract basic read statistics and
    return them as a ReadSummary instance

    Args:
        record: A single FASTQ SeqRecord produced by BioPython's SeqIO
            parser, containing the read ID, sequence, and per-base Phred
            quality scores.

    Returns:
        ReadSummary: A ReadSummary instance containing the read ID, sequence,
            total number of bases, and average phred quality score.
    """
    logging.debug(f"Summarizing recored '{record.id}'")
    phred_scores = record.letter_annotations['phred_quality']
    average_phred = sum(phred_scores) / len(phred_scores)

    return ReadSummary(
        id=record.id,
        sequence=str(record.seq),
        total_bases=len(record.seq),
        average_phred=round(average_phred, 2)
    )

def summarize_fastq_file(fastq_file: str, encoding: str) -> FastqSummary:
    """
    Given as FASTQ file, this function iterates over all reads in the file,
    summarizes each read, and returns the results as a FastqSummary instance.

    Args:
        fastq_file: Path to the input FASTQ file
        encoding: FASTQ format string used by BioPython to interpret sequence
            and quality score data.

    Returns:
        FastqSummary: A FastqSummary instance containing summaries for all reads
            in the input FASTQ file.
    """
    logging.info(f"Reading FASTQ file '{fastq_file}'")
    reads_list = []

    with open(fastq_file, 'r') as f:
        for record in SeqIO.parse(f, encoding):
            reads_list.append(summarize_record(record))

    logging.info(f"Finished reading {len(reads_list)} reads")
    return FastqSummary(reads=reads_list)

def write_summary_to_json(summary: FastqSummary, output_file: str) -> None:
    """
    Given a FastqSummary instance, serialize the data and write it to a JSON file.

    Args:
        summary: A FastqSummary object containing per-read summary data.
        output_file: Path to the output JSON file.

    Returns:
        None: This function does not return a value; it writes output to disk.
    """
    logging.info(f"Writing summary to '{output_file}'")
    with open(output_file, 'w') as outfile:
        json.dump(summary.model_dump(), outfile, indent=2)
    logging.info(f"Finished writing '{output_file}'")

def main():
    logging.info("Starting FASTQ summary workflow")

    try:
        summary = summarize_fastq_file(args.fastqfile, args.encoding)
        write_summary_to_json(summary, args.output)
    except FileNotFoundError:
        logging.error(f"Input FASTQ file '{args.fastqfile}' not found. Exiting.")
        sys.exit(1)

    logging.info("FASTQ summary workflow complete")

if __name__ == '__main__':
    main()
