readings = [0.0002, 0.0005, 0.0007, 0.0009]
warning_threshold = 0.0008

latest = readings[-1]  # The last reading in the list

if latest is None:
    print("Latest BER: reading missing")
elif latest > warning_threshold:
    print(f"Latest BER: WARNING — {latest} exceeds {warning_threshold}")
else:
    print(f"Latest BER: {latest} is within the threshold")
previous = readings[-2]

if latest is None or previous is None:
    print("Change since previous interval: UNKNOWN — a reading is missing")
elif latest > previous:
    print("Change since previous interval: RISING")
else:
    print("Change since previous interval: STABLE OR FALLING")