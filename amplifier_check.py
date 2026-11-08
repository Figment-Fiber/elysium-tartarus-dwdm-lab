import csv
from pathlib import Path

LAUNCH_DBM = -2.0
MIN_AMP_INPUT_DBM = -22.0
MAX_AMP_INPUT_DBM = -10.0
TERMINALS = {"Elysium", "Tartarus"}

inventory = Path(__file__).with_name("span_inventory.csv")

with inventory.open(encoding="utf-8-sig", newline="") as file:
    for span in csv.DictReader(file):
        directions = [
            ("FWD", span["to_site"], float(span["forward_loss_db"])),
            ("REV", span["from_site"], float(span["reverse_loss_db"])),
        ]

        for direction, receiver, loss_db in directions:
            rx_dbm = LAUNCH_DBM - loss_db

            if receiver in TERMINALS:
                result = "Terminal RX: check optic limits"
            else:
                in_range = MIN_AMP_INPUT_DBM <= rx_dbm <= MAX_AMP_INPUT_DBM
                status = "IN RANGE" if in_range else "REVIEW INPUT"
                result = f"Starting gain {loss_db:.1f} dB | {status}"

            print(f"{span['span_id']} {direction} | {receiver} | "
                  f"RX {rx_dbm:.1f} dBm/ch | {result}")