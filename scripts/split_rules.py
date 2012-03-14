#! /usr/bin/python
"""
Splits the ERULES.PRG file, from the game "The Adventures of Robin Hood", into
multiple files based on logical sections.

Also joins the split files back into one.

Could be useful for data mangling particular sections, in order to work out what they do.

Refer to:
https://github.com/jestarjokin/microcosm-re/wiki/Rules-File-Format

TODO:
- Supply input/output file names as arguments
- Support for non-English rules files (can be solved by above)
"""
from __future__ import with_statement

import logging
from optparse import OptionParser
import struct
import sys

SECTION_2_ENTRY_SIZE = 82
SECTION_3_ENTRY_SIZE = 2
SECTION_4_ENTRY_SIZE = 2
SECTION_5_ENTRY_SIZE = 2
SECTION_6_ENTRY_SIZE_1 = 2
SECTION_6_ENTRY_SIZE_2 = 1
SECTION_7_SIZE = 60
SECTION_9_ENTRY_SIZE = 8
SECTION_10_SIZE = 122 # cheating; there's really a few different parts to section 10

def join_rules():
    files_to_join = [
        'ERULES_%d.PRG' % i for i in xrange(11)
    ]
    with file('ERULES_new.PRG', 'wb') as new_rules:
        for section_file_name in files_to_join:
            with file(section_file_name, 'rb') as section_file:
                new_rules.write(section_file.read())

def split_rules():
    with file('ERULES.PRG', 'rb') as rules:
        with file('ERULES_0.PRG', 'wb') as section_0:
            section_0.write(rules.read(2)) # skip header
        with file('ERULES_1.PRG', 'wb') as section_1:
            logging.debug("Section 1 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s1_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries: %d" % s1_num_entries)
            section_1.write(data)
            section_1.write(rules.read(s1_num_entries))
        with file('ERULES_2.PRG', 'wb') as section_2:
            logging.debug("Section 2 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s2_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries: %d" % s2_num_entries)
            section_2.write(data)
            section_2.write(rules.read(s2_num_entries * SECTION_2_ENTRY_SIZE))
        with file('ERULES_3.PRG', 'wb') as section_3:
            logging.debug("Section 3 start: 0x%X" % rules.tell())
            data = rules.read(4)
            s3_num_entries, s3_data_size = struct.unpack('<2H', data)
            logging.debug("- Num entries: %d" % s3_num_entries)
            logging.debug("- Data size: %d" % s3_data_size)
            section_3.write(data)
            section_3.write(rules.read(s3_num_entries * SECTION_3_ENTRY_SIZE))
            section_3.write(rules.read(s3_data_size))
        with file('ERULES_4.PRG', 'wb') as section_4:
            logging.debug("Section 4 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s4_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries: %d" % s4_num_entries)
            section_4.write(data)
            section_4.write(rules.read(s4_num_entries * SECTION_4_ENTRY_SIZE))
        with file('ERULES_5.PRG', 'wb') as section_5:
            logging.debug("Section 5 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s5_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries: %d" % s5_num_entries)
            section_5.write(data)
            section_5.write(rules.read(s5_num_entries * SECTION_5_ENTRY_SIZE))
        with file('ERULES_6.PRG', 'wb') as section_6:
            logging.debug("Section 6 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s6_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries part 1: %d" % s6_num_entries)
            section_6.write(data)
            section_6.write(rules.read(s6_num_entries * SECTION_6_ENTRY_SIZE_1))
            data = rules.read(2)
            s6_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries part 2: %d" % s6_num_entries)
            section_6.write(data)
            section_6.write(rules.read(s6_num_entries * SECTION_6_ENTRY_SIZE_2))
        with file('ERULES_7.PRG', 'wb') as section_7:
            logging.debug("Section 7 start: 0x%X" % rules.tell())
            logging.debug("- Section size: %d" % SECTION_7_SIZE)
            section_7.write(rules.read(SECTION_7_SIZE))
        with file('ERULES_8.PRG', 'wb') as section_8:
            logging.debug("Section 8 start: 0x%X" % rules.tell())
            data = rules.read(1)
            s8_num_entries, = struct.unpack('<B', data)
            logging.debug("- Num entries: %d" % s8_num_entries)
            data_2 = rules.read(s8_num_entries)
            total_data_size = sum(
                struct.unpack('<' + str(s8_num_entries) + 'B', data_2)
            )
            logging.debug("- Data size: %d" % total_data_size)
            section_8.write(data)
            section_8.write(data_2)
            section_8.write(rules.read(total_data_size))
        with file('ERULES_9.PRG', 'wb') as section_9:
            logging.debug("Section 9 start: 0x%X" % rules.tell())
            data = rules.read(2)
            s9_num_entries, = struct.unpack('<H', data)
            logging.debug("- Num entries: %d" % s9_num_entries)
            section_9.write(data)
            section_9.write(rules.read(s9_num_entries * SECTION_9_ENTRY_SIZE))
        with file('ERULES_10.PRG', 'wb') as section_10:
            logging.debug("Section 10 start: 0x%X" % rules.tell())
            logging.debug("- Section size: %d" % SECTION_10_SIZE)
            section_10.write(rules.read(SECTION_10_SIZE))


def configure_logging():
    logging.basicConfig(format="", level=logging.DEBUG)


def validate_args(args, options):
    if (options.join and options.split) or \
        (not options.join and not options.split):
        logging.error("Please pass either the 'join' or 'split' options (but not both).")
        return False
    return True


def main(args):
    configure_logging()
    oparser = OptionParser(usage="%prog [-j|-s]",
        version="1.0")

    oparser.add_option("-j", "--join", action="store_true",
        dest="join", default=False,
        help="Join previously separated rules.")
    oparser.add_option("-s", "--split", action="store_true",
        dest="split", default=False,
        help="Split a rules file.")

    options, args = oparser.parse_args()

    if not validate_args(args, options):
        oparser.print_help()
        return 1

    try:
        if options.split:
            logging.info("Splitting rules file.")
            split_rules()
        elif options.join:
            logging.info("Joining rules files.")
            join_rules()
        logging.info("Done!")
    except Exception, e:
        logging.exception("Unhandled exception: \n")
        return 2

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
