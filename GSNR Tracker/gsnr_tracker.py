"""Prompt for one channel and direction, then write a GSNR review workbook."""

from datetime import datetime
from math import isfinite, log10
from pathlib import Path
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "GSNR Tracker.xlsx"
WORKSHEET = "xl/worksheets/sheet1.xml"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", NS)


def ask_number(prompt, minimum=-100, maximum=100, optional=False):
    while True:
        raw = input(f"{prompt}: ").strip()
        if optional and not raw:
            return None
        try:
            value = float(raw)
            if isfinite(value) and minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Enter a number from {minimum} to {maximum}.")


def read_inputs():
    print("GSNR check for one channel in one direction")
    print("Use the same reference bandwidth for the threshold and all SNR inputs.")
    print("Enter separate noise contributions only if none already includes another.")
    label = input("Route, direction and channel (optional): ").strip()
    while True:
        mode = input("1 = modeled end-to-end GSNR, 2 = combine noise contributions: ").strip()
        if mode in {"1", "2"}:
            break
        print("Enter 1 or 2.")
    minimum = ask_number("Minimum GSNR for the selected optic mode (dB)")
    reserve = ask_number("Required design margin (dB)", minimum=0)
    if mode == "1":
        modeled = ask_number("Modeled end-to-end GSNR (dB)")
        return {"B4": label, "B6": 1, "B7": minimum, "B8": reserve, "B10": modeled}
    ase = ask_number("ASE-only OSNR from the amplifier chain (dB)")
    nli = ask_number("Nonlinear-interference SNR (dB)")
    other = ask_number("Additional independent SNR (dB, Enter to skip)", optional=True)
    penalty = ask_number("Separate modeled penalty (dB, Enter to skip)", minimum=0, optional=True)
    return {
        "B4": label, "B6": 2, "B7": minimum, "B8": reserve,
        "B12": ase, "B13": nli, "B14": other, "B16": penalty,
    }


def qname(tag):
    return f"{{{NS}}}{tag}"


def write_report(inputs, destination):
    # Excel owns the formulas. Update only the input cells in the styled template.
    with ZipFile(TEMPLATE) as template:
        sheet = ET.fromstring(template.read(WORKSHEET))
        cells = {cell.get("r"): cell for cell in sheet.iter(qname("c"))}
        for address in ("B4", "B6", "B7", "B8", "B10", "B12", "B13", "B14", "B16"):
            cell = cells[address]
            cell.attrib.pop("t", None)
            for child in list(cell):
                cell.remove(child)
            value = inputs.get(address)
            if isinstance(value, str) and value:
                cell.set("t", "inlineStr")
                ET.SubElement(ET.SubElement(cell, qname("is")), qname("t")).text = value
            elif value is not None and value != "":
                ET.SubElement(cell, qname("v")).text = str(value)

        for cell in cells.values():
            if cell.find(qname("f")) is not None:
                cached = cell.find(qname("v"))
                if cached is not None:
                    cell.remove(cached)
                cell.attrib.pop("t", None)

        workbook_path = "xl/workbook.xml"
        workbook = ET.fromstring(template.read(workbook_path))
        calc = workbook.find(qname("calcPr"))
        if calc is None:
            calc = ET.SubElement(workbook, qname("calcPr"))
        calc.set("calcMode", "auto")
        calc.set("fullCalcOnLoad", "1")
        replacements = {
            WORKSHEET: ET.tostring(sheet, encoding="utf-8"),
            workbook_path: ET.tostring(workbook, encoding="utf-8"),
        }
        with destination.open("xb") as file, ZipFile(file, "w") as report:
            for entry in template.infolist():
                data = replacements.get(entry.filename)
                if data is None:
                    data = template.read(entry)
                report.writestr(entry, data)


def main():
    if not TEMPLATE.is_file():
        raise FileNotFoundError(f"Keep {TEMPLATE.name} next to this script.")
    inputs = read_inputs()
    if inputs["B6"] == 1:
        effective = inputs["B10"]
    else:
        ratios = [inputs[key] for key in ("B12", "B13", "B14") if inputs[key] is not None]
        effective = -10 * log10(sum(10 ** (-snr / 10) for snr in ratios))
        effective -= inputs["B16"] or 0.0
    target = inputs["B7"] + inputs["B8"]
    delta = round(effective - target, 9)
    status = "PASS GSNR CHECK" if delta >= 0 else "BELOW TARGET"
    destination = HERE / f"GSNR Review {datetime.now():%Y%m%d-%H%M%S-%f}.xlsx"
    write_report(inputs, destination)
    print(f"{status} | effective GSNR {effective:.2f} dB | target {target:.2f} dB | headroom {delta:+.2f} dB")
    print(f"Open in Excel to see the calculated results and next checks: {destination}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit("\nCancelled.")
    except (OSError, KeyError) as error:
        sys.exit(f"Could not create the report: {error}")
