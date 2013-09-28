from args import parse_args
import server

if __name__ == "__main__":
    args = parse_args()
    print "Starting cortext beacon"
    print "  - Listening on port: " + str(args.port)
    print " ".join(["  - Using", "_mocked_" if args.mock else "_real_", "data"])

    if args.port < 1024:
        print "You selected a port < 1024, this requires special priveleges"  

    print "Press Ctrl-C to shut down..."
    server.start_beacon_server(args.port, args.mock)
