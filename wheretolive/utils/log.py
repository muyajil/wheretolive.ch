from datetime import datetime


def get_batch_logline(self, idx, start_batch, start, item_name):
    now = datetime.now()
    logline = f"{item_name}s comitted: {idx}\t"
    logline += f"Batch Time elapsed: {now-start_batch}\t"
    logline += f"Total Time elapsed: {now-start}"
    return logline, now
