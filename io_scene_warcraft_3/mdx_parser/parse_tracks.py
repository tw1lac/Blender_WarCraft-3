def parse_tracks(r):
    tracks_count = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(tracks_count):
        time = r.getf('<I')[0]
