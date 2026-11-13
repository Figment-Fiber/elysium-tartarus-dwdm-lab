# GNPy span modeling

This synthetic lab models the first 160 km of the proposed 1,440 km Elysium–Tartarus terrestrial DWDM line system. Its first planned activation is a 400G circuit. These partial-route checks use the bundled GNPy 3.0.1 spectrum and generic low-gain EDFAs. Full-route 400G qualification requires the selected modem profile, expected loading, and equipment data.

| Span | Endpoints | Length | Forward loss | Reverse loss |
| --- | --- | ---: | ---: | ---: |
| W01 | Elysium to W-Hut-01 | 78 km | 16.20 dB | 16.50 dB |
| W02 | W-Hut-01 to W-Hut-02 | 82 km | 17.40 dB | 17.20 dB |

Each direction uses total loss divided by distance as an effective attenuation coefficient. The [inventory](../span_inventory.csv) supplies the directional losses. Separate connector and splice loss entries are zero in these models because their loss is included in the span total. For W01, the effective coefficients are 0.2077 and 0.2115 dB/km, rounded for display. A model with discrete splice events needs their locations and losses separated from distributed attenuation.

## Reproduce the runs

From the repository root in PowerShell with uv and Python 3.12:

```powershell
uv tool run --python 3.12 --from gnpy==3.0.1 gnpy-transmission-example .\gnpy-lab\GNPy_W01.json Elysium W-Hut-01 --show-channels
uv tool run --python 3.12 --from gnpy==3.0.1 gnpy-transmission-example .\gnpy-lab\GNPy_W01.json W-Hut-01 Elysium --show-channels
uv tool run --python 3.12 --from gnpy==3.0.1 gnpy-transmission-example .\gnpy-lab\GNPy_W01_W02.json Elysium W-Hut-02 --show-channels
uv tool run --python 3.12 --from gnpy==3.0.1 gnpy-transmission-example .\gnpy-lab\GNPy_W01_W02.json W-Hut-02 Elysium --show-channels
```

## Results

Channel 36 is centered at 193.100 THz. Its OSNR, SNR NLI, and GSNR use signal bandwidth. The final CLI summary uses a separate 0.1 nm reference.

| Path | Ch. 36 RX (dBm) | Ch. 36 OSNR ASE (dB) | Ch. 36 SNR NLI (dB) | Ch. 36 GSNR (dB) | Final CLI GSNR (dB, 0.1 nm) |
| --- | ---: | ---: | ---: | ---: | ---: |
| W01 forward | −2.00 | 29.73 | 30.17 | 26.93 | 31.12 |
| W01 reverse | −2.00 | 29.54 | 30.24 | 26.87 | 31.06 |
| W01 + W02 forward | −2.01 | 26.39 | 28.06 | 24.13 | 28.31 |
| W01 + W02 reverse | −2.01 | 26.46 | 28.07 | 24.18 | 28.36 |

The runs reproduced all four directional inventory losses. GNPy reported a default ROADM equipment-library warning. These topologies contain no ROADMs.

## Engineering notes

- A hut provides space to land fiber and house line equipment. In the two-span model, W-Hut-01 houses an in-line EDFA, and W-Hut-02 is the temporary receiver site.
- The W-Hut-01 EDFA receives −16.20 dBm per channel in both forward runs. With the test receiver immediately after it, the demo auto-design uses a −2.00 dBm target and 14.20 dB gain. When that EDFA feeds W02, GNPy targets −1.00 dBm and uses 15.20 dB gain. After W02's 17.40 dB loss, the next EDFA receives −18.40 dBm per channel.
- Equipment gain and total power limits constrain the launch settings available at the expected loading. Compare end-to-end GSNR across those settings. An EDFA restores signal power and adds ASE noise. Additional fiber can contribute nonlinear interference. In the forward comparison, channel 36 receive power stayed near −2 dBm while GSNR dropped 2.80 dB.
- At Olympus, landing the west and east spans on fiber panels up front can simplify later changes. A ROADM can express the Elysium–Tartarus wavelength while dropping another wavelength locally. Inserting it into a live patch path may require an outage or a qualified alternate path. If the first service is regenerated optically–electrically–optically at Olympus, assess each optical section against its receiver requirements.
