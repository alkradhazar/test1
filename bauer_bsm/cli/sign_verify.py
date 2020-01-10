#!/usr/bin/env python3

# Signature verification tool for Signing Meter.
#
# For the following example the signature will be verified successfully:
#
#     $ sign-verify --pubkey=046858b701931d153524d03b28f8b2758d33dd6f76282184ad825e31283e076e1f8c1747f16f9df5b5123594fe867b282a2fb5ab704d5230445cc820e3880b4db7 --signature=304402205d3c7fbdc68c0484475b15051f51192230f37c3590de7060f31f7c07137089fa022035fae5dd765f558680762acc65e35e71e5862370ad1da8cbe87a8e22cb6418eb --digest=6bdab37edc9f9b29c125056eed1d7506b5f346743306eac2e3ae6789adda746d
#


from ..crypto.curves import SECP256r1
from ..crypto.util import verify_signed_digest
from argparse import ArgumentParser
from argparse import FileType
from hashlib import sha256

import string
import sys




def hex_data_or_file(arg):
    hex_digits = set(string.hexdigits)
    if all(c in hex_digits for c in arg):
        return bytes.fromhex(arg)
    else:
        return open(arg, 'rb').read()


def main():
    parser = ArgumentParser(
        description='ECDSDA signature verification tool for Signing Meter',
        epilog='HEX_OR_FILE arguments may be either immediate data as hex string or the name of a file to read the data from.')
    parser.add_argument('--verbose', action='store_true',
        help='Always output result')
    parser.add_argument('--pubkey', metavar='HEX_OR_FILE', required=True,
        type=hex_data_or_file,
        help='public key uncompressed point in SEC1 format')
    parser.add_argument('--signature', metavar='FILE', required=True,
        type=hex_data_or_file,
        help='ASN.1 encoded signature')
    # TODO: Add support for verifying data.
    parser.add_argument('--digest', metavar='HEX_DATA', required=True,
        type=hex_data_or_file,
        help='SHA-256 digest to verify signature for')

    args = parser.parse_args()


    if verify_signed_digest(SECP256r1, sha256, args.pubkey, args.signature, args.digest):
        if args.verbose:
            print('success')
        sys.exit(0)
    else:
        print('failure', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()