# Elysium–Tartarus DWDM Feasibility Lab

This is a fictional portfolio project for a new 400G terrestrial DWDM line. The sites, survey results, and vendor model outputs are synthetic.

## Management brief

Management approved the business case and secured a signed order for an unprotected, point-to-point 400G wavelength. Elysium and Tartarus are existing facilities. The assignment is to design the optical line between them, qualify the fiber path, and prepare a recommendation that management can use to authorize procurement.

The plan is to lease a dark fiber pair on existing terrestrial cable infrastructure and use existing intermediate facilities for amplification where feasible. Olympus is an existing site on the route. It has two unconfirmed 100G quote requests, so the design should preserve the option to add and drop wavelengths there later. Hades Gateway is a separate future extension from Tartarus.

## Candidate route

| Segment | Routed fiber distance | Day-one role |
| --- | ---: | --- |
| Elysium → Olympus | 640 km | West section of the 400G path |
| Olympus → Tartarus | 800 km | East section of the 400G path |
| **Elysium → Tartarus** | **1,440 km** | **End-to-end 400G service** |
| Tartarus → Hades Gateway | 320 km | Future extension |

The day-one design uses one G.652.D single-mode fiber pair, with one strand per direction. Olympus is on the route, but the day-one service has no local add/drop requirement there.

```text
Day one: Elysium -- 640 km -- Olympus -- 800 km via E-Hut-01 and other huts -- Tartarus
Future:  Tartarus -- 320 km -- Hades Gateway
```

## Route survey and facilities review

Engineering set G.652.D as the baseline and asked Fiber Sourcing to flag any alternatives or mixed fiber types. The survey request called for the endpoint demarcations, routed span lengths, installed fiber types, measured losses, and locations where the pair could be accessed. Facilities was asked to check rack space, DC power, cooling, and fiber panel access at the endpoints and intermediate huts.

The provider identified a candidate pair and confirmed access to the proposed amplifier huts. The preliminary survey identified one span east of Olympus that exceeded the standard amplifier design’s **22 dB** screening limit. It measured **24.5 dB over 114 km**. Both strands showed similar loss, and the supplied OTDR traces showed no single high-loss event to correct.

The measured average was approximately **0.215 dB/km**, including splice and connector losses. Similar results on both strands made an isolated one-strand defect less likely. Historical tests are still needed to establish whether the loss has been stable or is increasing.

## Decision 01 — Split the long span east of Olympus

The simulated vendor study compared keeping the 114 km span with a different amplifier against leasing an existing hut to split it. The project requires at least **1.5 dB of end-to-end design margin**.

| Option | Predicted margin | Result against requirement |
| --- | ---: | --- |
| Keep the 114 km span with a different amplifier | 1.2 dB | 0.3 dB short |
| Split the span at the existing hut | 2.4 dB | 0.9 dB above requirement |

**Recommendation:** Lease the existing hut, subject to verification. The split introduces cost and schedule work, but it is the only option in this comparison that meets the required margin.

Before authorizing the lease:

- Compare historical loss tests on the same strands, at the same wavelength and between the same test points, to check for deterioration.

- Confirm the two proposed sections’ measured losses of **13.4 dB** and **11.8 dB**. Reconcile their sum with the **24.5 dB** original measurement using the provider’s test boundaries.

- Confirm hut access, rack space, DC power, cooling, fiber panel access, and lease timing.

- Verify the final equipment configuration meets the 400G margin requirement in both directions.

## Decision 02 — 400G operating mode and spectrum

Use **Mode B** in the available **100 GHz** end-to-end slot. Both options deliver 400G. GSNR values are synthetic and represent the weaker direction. The required design margin is 1.5 dB above the optic minimum.

| Mode | Slot width | Optic minimum GSNR | Day-one GSNR | Day-one margin | GSNR with Olympus add/drop | Margin with Olympus add/drop |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 75 GHz | 15.0 dB | 17.4 dB | 2.4 dB | 16.1 dB | 1.1 dB |
| **B** | **100 GHz** | **14.5 dB** | **17.0 dB** | **2.5 dB** | **16.8 dB** | **2.3 dB** |

Mode B meets the margin requirement in both layouts and leaves 0.8 dB above the requirement after the Olympus upgrade. It uses 25 GHz more spectrum than Mode A. Confirm the center frequency, slot edges and adjacent-channel compatibility before issuing the provisioning plan.

## Commissioning and customer handoff

Before I hand the wave over, I want two reports from the final path.

1. **Optical line report.** I’d ask for launch and receive power at the specified ports, pre-FEC BER against the selected mode’s limit, and Q or SNR margin where the modem reports it. I’d check both directions for zero new uncorrectable FEC events and review any loss-of-signal or loss-of-lock alarms during the agreed test window.
2. **End-to-end service acceptance report.** I’d have the tech test from the Elysium customer demarc to the Tartarus customer demarc using the agreed 400GbE traffic profile. I’d review the delivered rate and frame loss, plus latency or delay variation if the service calls for it. If we agreed to a 24-hour BERT, I’d ask for the error count and 24 hours of valid, synchronized test time on the final path.

I’d save both reports with the circuit configuration and handoff record. Before adding Olympus later, I’d rerun the optical model with the proposed add/drop configuration and test the existing 400G through path during the change.

## Supporting tools and design status

From the project folder, run:

```powershell
python .\amplifier_check.py
python ".\GSNR Tracker\gsnr_tracker.py"
```

The [span inventory](span_inventory.csv) and amplifier checker screen per-direction receive power and calculate starting gain. The [GSNR Tracker](GSNR%20Tracker/README.md) screens modeled results against the optic threshold and design reserve, then creates an Excel report. To check the selected mode after adding Olympus, enter **14.5 dB** as the optic minimum, **1.5 dB** as the design margin, and **16.8 dB** as the modeled GSNR. The result clears the target by **0.8 dB**.

Exact equipment models, channel assignment, vendor qualification, and field acceptance are still to be verified in a real deployment.
