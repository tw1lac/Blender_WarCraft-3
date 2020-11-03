def parse_tracks(r):
    tracksCount = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(tracksCount):
        time = r.getf('<I')[0]