#!/usr/bin/env python

# Prerequisites: 
# pip install pydicom
# pip install -U pynetdicom

import argparse
import sys
import os

from pydicom.uid import (
    ExplicitVRLittleEndian,
    ImplicitVRLittleEndian,
    ExplicitVRBigEndian,
)

from pynetdicom import (
    AE,
    evt,
    AllStoragePresentationContexts,
    VerificationPresentationContexts,
)
from pynetdicom.apps.common import setup_logging
from pynetdicom._globals import ALL_TRANSFER_SYNTAXES, DEFAULT_MAX_LENGTH

from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike
from datetime import datetime


__version__ = "0.6.0"


def _setup_argparser():
    """Setup the command line arguments"""
    # Description
    parser = argparse.ArgumentParser(
        description=(
            "The Speedtest application implements a Service Class "
            "Provider (SCP) for a Storage and Verification SOP Classes and a "
            "C-MOVE Service Class User (SCU). It triggers a C-MOVE on a specified StuyInstanceUID and "
            "listens for a DICOM C-STORE message from a Service Class User "
            "(SCU). It finally measures delay for the first incoming image and total throughput from the PACS."
        ),
        usage="python3 ./speedtest.py [options] host port aec",
    )

    # Parameters
    req_opts = parser.add_argument_group("Parameters")
    req_opts.add_argument("host", help="Hostname of DICOM peer", type=str)
    req_opts.add_argument("port", help="TCP/IP port number to listen on", type=int)
    req_opts.add_argument("aec", help="Called AE title", type=str)

    # General Options
    gen_opts = parser.add_argument_group("General Options")
    gen_opts.add_argument(
        "--version", help="print version information and exit", action="store_true"
    )
    output = gen_opts.add_mutually_exclusive_group()
    output.add_argument(
        "-q",
        "--quiet",
        help="quiet mode, print no warnings and errors",
        action="store_const",
        dest="log_type",
        const="q",
    )
    output.add_argument(
        "-v",
        "--verbose",
        help="verbose mode, print processing details",
        action="store_const",
        dest="log_type",
        const="v",
    )
    output.add_argument(
        "-d",
        "--debug",
        help="debug mode, print debug information",
        action="store_const",
        dest="log_type",
        const="d",
    )
    gen_opts.add_argument(
        "-ll",
        "--log-level",
        metavar="[l]",
        help=("use level l for the logger (critical, error, warn, info, debug)"),
        type=str,
        choices=["critical", "error", "warn", "info", "debug"],
    )

    # Network Options
    net_opts = parser.add_argument_group("Network Options")
    net_opts.add_argument(
        "-aet",
        "--ae-title",
        metavar="[a]etitle",
        help="set my AE title (default: STORESCP)",
        type=str,
        default="STORESCP",
    ),
    net_opts.add_argument(
        "-p",
        "--cstore-port",
        metavar="[p]port",
        help="set my STORECSP port (default: 9999)",
        type=int,
        default="9999",
    )
    net_opts.add_argument(
        "-ta",
        "--acse-timeout",
        metavar="[s]econds",
        help="timeout for ACSE messages (default: 30 s)",
        type=float,
        default=30,
    )
    net_opts.add_argument(
        "-td",
        "--dimse-timeout",
        metavar="[s]econds",
        help="timeout for DIMSE messages (default: 30 s)",
        type=float,
        default=30,
    )
    net_opts.add_argument(
        "-tn",
        "--network-timeout",
        metavar="[s]econds",
        help="timeout for the network (default: 30 s)",
        type=float,
        default=30,
    )
    net_opts.add_argument(
        "-pdu",
        "--max-pdu",
        metavar="[n]umber of bytes",
        help=(
            f"set max receive pdu to n bytes (0 for unlimited, "
            f"default: {DEFAULT_MAX_LENGTH})"
        ),
        type=int,
        default=DEFAULT_MAX_LENGTH,
    )
    net_opts.add_argument(
        "-ba",
        "--bind-address",
        metavar="[a]ddress",
        help=(
            "The address of the network interface to "
            "listen on. If unset, listen on all interfaces."
        ),
        default="",
    )

    # Transfer Syntaxes
    ts_opts = parser.add_argument_group("Preferred Transfer Syntaxes")
    ts = ts_opts.add_mutually_exclusive_group()
    ts.add_argument(
        "-x=",
        "--prefer-uncompr",
        help="prefer explicit VR local byte order",
        action="store_true",
    )
    ts.add_argument(
        "-xe",
        "--prefer-little",
        help="prefer explicit VR little endian TS",
        action="store_true",
    )
    ts.add_argument(
        "-xb",
        "--prefer-big",
        help="prefer explicit VR big endian TS",
        action="store_true",
    )
    ts.add_argument(
        "-xi",
        "--implicit",
        help="accept implicit VR little endian TS only",
        action="store_true",
    )

    # Miscellaneous Options
    misc_opts = parser.add_argument_group("Miscellaneous Options")
    misc_opts.add_argument(
        "--no-echo", help="don't act as a verification SCP", action="store_true"
    )
    misc_opts.add_argument(
        "-s",
        "--study",
        metavar="[s]tudy",
        help=(
            f"StudyInstanceUID to retrieve "
            f"default: 1.2.250.1.213.4.5.2.1.199"
        ),
        type=str,
        default="1.2.250.1.213.4.5.2.1.199",
    )
    misc_opts.add_argument(
        "-pid",
        "--patientid",
        metavar="[p]patientid",
        help=(
            f"PatientID to retrieve "
            f"default: 199"
        ),
        type=int,
        default="199",
    )

    return parser.parse_args()

total_size = 0
first_image_received = False
time_firstimage = datetime.now()

def handle_store(event):
    global total_size, first_image_received, time_firstimage
    """Handle a C-STORE service request"""
    ds = event.dataset
    with BytesIO() as buffer:
        # create a DicomFileLike object that has some properties of DataSet
        memory_dataset = DicomFileLike(buffer)
        # write the dataset to the DicomFileLike object
        dcmwrite(memory_dataset, ds)
        total_size += memory_dataset.tell()
        if first_image_received == False:
            time_firstimage = datetime.now()
            print("First image received")
            print(time_firstimage)
            first_image_received = True
    # Ignore the request and return Success
    return 0x0000



def main(args=None):
    """Run the application."""
    if args is not None:
        sys.argv = args

    args = _setup_argparser()
    if args.version:
        print(f"storescp.py v{__version__}")
        sys.exit()

    APP_LOGGER = setup_logging(args, "storescp")
    APP_LOGGER.debug(f"storescp.py v{__version__}")
    APP_LOGGER.debug("")

    # Set Transfer Syntax options
    transfer_syntax = ALL_TRANSFER_SYNTAXES[:]

    if args.prefer_uncompr:
        transfer_syntax.remove(ImplicitVRLittleEndian)
        transfer_syntax.append(ImplicitVRLittleEndian)
    elif args.prefer_little:
        transfer_syntax.remove(ExplicitVRLittleEndian)
        transfer_syntax.insert(0, ExplicitVRLittleEndian)
    elif args.prefer_big:
        transfer_syntax.remove(ExplicitVRBigEndian)
        transfer_syntax.insert(0, ExplicitVRBigEndian)
    elif args.implicit:
        transfer_syntax = [ImplicitVRLittleEndian]

    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Create application entity
    ae = AE(ae_title=args.ae_title)

    # Add presentation contexts with specified transfer syntaxes
    for context in AllStoragePresentationContexts:
        ae.add_supported_context(context.abstract_syntax, transfer_syntax)

    if not args.no_echo:
        for context in VerificationPresentationContexts:
            ae.add_supported_context(context.abstract_syntax, transfer_syntax)

    ae.maximum_pdu_size = args.max_pdu

    # Set timeouts
    ae.network_timeout = args.network_timeout
    ae.acse_timeout = args.acse_timeout
    ae.dimse_timeout = args.dimse_timeout

    ae.start_server((args.bind_address, args.cstore_port), block=False, evt_handlers=handlers)

    time_start = datetime.now()
    time_start.microsecond
    print("-----STARTING SPEEDTEST------")
    print(time_start)

    commandline = ("python3 -m pynetdicom movescu " + args.host + " " + str(args.port) + " -aec " + args.aec + 
         " -v  -k QueryRetrieveLevel=PATIENT -k PatientID=" + str(args.patientid) + " -k StudyInstanceUID=" + args.study + " -aem " + args.ae_title)
    print("Executing C-MOVE: ")
    print(commandline)
    os.system(commandline)

    time_stop = datetime.now()
    print("-----STOP------")
    print(time_stop)

    latency = time_firstimage - time_start
    if time_firstimage < time_start:
        print("Something went wrong, no images received. Aborting Speedtest.")
        return
    
    total_duration =  time_stop - time_start

    throughput = ((total_size * 8 ) / total_duration.total_seconds()) / 1000000

    print("-----RESULTS-----")
    print("LATENCY: " + str(latency))
    print("THROUGHPUT: " + str(throughput) + " Mbps" )


if __name__ == "__main__":
    main()
