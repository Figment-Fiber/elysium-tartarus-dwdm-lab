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

## Next design stage

Complete the span inventory and amplifier layout, select the terminal equipment and 400G operating mode, and build the spectrum plan. Evaluate the day-one design and the future Olympus add/drop configuration separately. Then document commissioning, acceptance tests, and handoff criteria.
