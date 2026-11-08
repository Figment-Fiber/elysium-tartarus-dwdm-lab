# DWDM GSNR Tracker

Screen one optical channel in one direction. Repeat for the reverse direction and each configuration being compared.

Keep `GSNR Tracker.xlsx` beside the Python script. From that folder, run `python .\gsnr_tracker.py` in PowerShell. Python prints the result and creates a dated Excel report. Open the report in Excel to calculate the worksheet and see the recommendations. You can also edit the yellow inputs in the template directly.

1. Enter the minimum GSNR for the selected optic and mode, then enter the project's required design margin. Excel adds the two to get the approval target.
2. Use a modeled end-to-end GSNR when you already have one. Alternatively, enter separate end-of-path ASE-only OSNR and nonlinear-interference SNR values. An optional third input can represent an independent contribution such as transmitter noise. Enter a separate filter or other modeled penalty only when it has not already been included.
3. Use the same reference bandwidth for the requirement and all supplied values. Enter SNR or OSNR ratios in dB. Receive power in dBm and amplifier noise figure in dB are different measurements. A modem requirement stated as OSNR at 0.1 nm needs a compatible comparison basis before use.

The component method converts each SNR to a linear noise-to-signal ratio, adds those ratios, and converts back to dB. The design margin is the effective GSNR minus the optic minimum. Headroom is the effective GSNR minus the approval target.

The workbook starts with the synthetic Elysium–Tartarus example. A 15.0 dB optic minimum and a 1.5 dB required margin give a 16.5 dB target. An assumed 17.4 dB end-to-end GSNR leaves 2.4 dB above the optic minimum and 0.9 dB above the approval target.

This tool screens entered results. Use a route model for link feasibility and verify receive power and acceptance tests before turning up service. See the [GNPy physical model](https://gnpy.readthedocs.io/en/master/model.html).
