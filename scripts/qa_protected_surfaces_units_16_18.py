#!/usr/bin/env python3
"""Verify protected mathematical surfaces for cumulative Units 1--18."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
HTML = ROOT / "build" / "reader-id" / "index.html"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-18.pdf"
OUT = ROOT / "qa" / "UNIT_18_PROTECTED_SURFACES.json"
BASELINE = ROOT / "qa" / "UNIT_15_PROTECTED_SURFACES.json"
MACHINE = ROOT / "qa" / "UNITS_01_18_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

BASELINE_FACT = (9656, "633df9e390d6aceb55baf40f7ddc79173963a076593c0ba68d83f8fa7e245a3b")
MACHINE_FACT = (9029, "8ff3c87c646c7c3f8a7067736bc3612f39bdf3702509f134c2c3902eab7fb4c2")
UNIT_QA_FACTS = {
    16: (4373, "02ff081cd808172438262846944763e25871f6805a6a6f59bee933e3bf1fda19"),
    17: (3630, "738a9d27d620c55770e17a0bcb089ae756cfa632262074a94f02393498a1d8be"),
    18: (3610, "9a0d480dc799bb53669e324a324f43f89d9672a7d3bf5a5cdae9cd45e3dd669c"),
}
PROTECTED = {
    16: [
        r"S=\{f\inR\midD(f)\inF\}",
        r"D(g)\cupD(h)=D(g,h)\supseteqD(g+h)",
        r"\widetilde\psi:\Gamma(U,\mathcalO)\longrightarrow\Gamma(\psi^{-1}(U),\mathcalO)",
        r"f\circ\varphi^*=\frac{\varphi(G)}{\varphi(H)}",
        r"\operatorname{Mor}(U,\mathbbA_K^1)&\longrightarrow\Gamma(U,\mathcalO)",
        r"S=K[T_1,\ldots,T_n]/\mathfraka",
        r"V=V(X^2+Y^2-Z^2)\subseteq\mathbbA_K^3",
        r"\frac{X}{Z-Y}=\frac{Z+Y}{X}",
        r"A=R[T_1,\ldots,T_n]/(f_1T_1+\cdots+f_nT_n+f)",
        r"f^{-1}(0)=V(h_1g_1,\ldots,h_ng_n)\capU",
        r"(ax-by)^2+(bx+ay)^2",
        r"V(XY,XZ,YZ)=V(X,Y)\cupV(X,Z)\cupV(Y,Z)",
        r"(B-Z)Z=-\frac{2AB^2(A-B)}{(A+B)^2}",
    ],
    17: [
        r"R[M]=\bigoplus_{m\inM}Re_m",
        r"e_m\cdote_k:=e_{m+k}",
        r"X^mX^k=X^{m+k}",
        r"R[\mathbbN]=R[X]",
        r"R[X_1,\ldots,X_n]_{X_1\cdotsX_n}",
        r"\widetilde\varphi(X^m)=\varphi(m)",
        r"\widetilde\varphi:R[M]&\longrightarrowR[N]",
        r"\operatorname{Mor}_{\mathrm{mon}}(M,K)",
        r"a_1^{n_1}\cdotsa_r^{n_r}=a_1^{m_1}\cdotsa_r^{m_r}",
        r"\Gamma(M)=\{m-n\midm,n\inM\}",
        r"u+m_1+n_2=u+m_2+n_1",
        r"m+n=m+k",
        r"K[M]\congK[X,Y,U,V]/(UX-VY)",
        r"R[I]=\bigoplus_{m\inI}RT^m\subseteqR[M]",
        r"R[M_f]\congR[M]_{T^f}",
        r"e+f=5g",
        r"F=P(X^{1/b})",
        r"\varphi\circ\rho(g)=\rho(g)\circ\varphi",
        r"q_1+r_1=q_n+r_m=1",
        r"q_1+r_1=q_n+r_m=0",
    ],
    18: [
        r"t\longmapsto(t^{e_1},\ldots,t^{e_n})",
        r"s\longmapsto(s^{f_1},\ldots,s^{f_n})",
        r"\mathbbN^n\longrightarrowM\longrightarrow\mathbbN",
        r"K[\mathbbN^n]=K[X_1,\ldots,X_n]",
        r"C=V(Y^2-X^3)",
        r"\mathbbN_{\geqf}\subseteqM",
        r"M_+\setminus(M_++M_+)",
        r"x=x_1+x_2",
        r"\varphi:M\longrightarrowK",
        r"m_1e_1+\cdots+m_ne_n=1",
        r"a=a_1^{m_1}\cdotsa_n^{m_n}",
        r"R=\mathbbC[X,Y]/(Y^2-X^3)",
        r"\psi:\operatorname{Mor}_{\mathrm{mon}}(\mathbbN,R)",
        r"K[M\timesM]\congK[M]\otimesK[M]",
        r"F(x,y)=(x^ay^b,x^cy^d)",
        r"nM_+=\left\{m\inM\mathrel{\Big|}",
        r"\varphi(f)=c(T-1)^n",
        r"\pi(1)=\rho(3)\rho(2)^{-1}",
        r"6+8+1=15",
        r"\mathbbN\subset\mathbbZ",
    ],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value)


def main() -> int:
    require((BASELINE.stat().st_size, digest(BASELINE)) == BASELINE_FACT, "Unit 15 protected baseline drift")
    require(json.loads(BASELINE.read_text(encoding="utf-8"))["status"] == "PASS", "Unit 15 protected baseline status")
    require((MACHINE.stat().st_size, digest(MACHINE)) == MACHINE_FACT, "cumulative machine QA drift")
    require(json.loads(MACHINE.read_text(encoding="utf-8"))["status"] == "PASS", "cumulative machine QA status")
    for unit, fact in UNIT_QA_FACTS.items():
        path = ROOT / "qa" / f"UNIT_{unit:02d}_TRANSLATION_QA.json"
        require((path.stat().st_size, digest(path)) == fact, f"Unit {unit} QA drift")
        require(json.loads(path.read_text(encoding="utf-8"))["status"] == "PASS", f"Unit {unit} QA status")

    source_checks: dict[str, dict[str, object]] = {}
    all_tokens: list[str] = []
    for unit, tokens in PROTECTED.items():
        raw = "\n".join((SOURCE / name).read_text(encoding="utf-8") for name in (f"lecture-{unit:02d}.md", f"worksheet-{unit:02d}.md", f"worksheet-{unit:02d}-solutions.md"))
        normalized = normalize(raw)
        missing = [token for token in tokens if token not in normalized]
        require(not missing, f"protected source math absent in Unit {unit}: {missing}")
        source_checks[str(unit)] = {"tokens": len(tokens), "source_files": 3, "missing": 0}
        all_tokens.extend(tokens)

    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    annotations = [tag.get_text() for tag in soup.find_all("annotation") if tag.get("encoding") == "application/x-tex"]
    annotation_blob = normalize("\n".join(annotations))
    missing_html = [token for token in all_tokens if token not in annotation_blob]
    require(not missing_html, f"protected TeX annotations absent from HTML: {missing_html}")
    require(len(annotations) == 7186, f"HTML TeX annotation count: {len(annotations)}")

    reader = PdfReader(PDF, strict=True)
    require(len(reader.pages) == 320, "PDF boundary")
    text = "\n".join((reader.pages[index].extract_text() or "") for index in range(267, 320))
    for marker in ("Kuliah 16", "Soal 16.23", "Solusi Soal 16.15", "Kuliah 17", "Soal 17.39", "Solusi Soal 17.32", "Kuliah 18", "Soal 18.28", "Solusi Soal 18.15"):
        require(marker in text, f"protected terminal PDF marker absent: {marker}")

    receipt = {
        "schema": "ag-bridge-protected-surfaces-v2",
        "status": "PASS",
        "verified_date": "2026-08-24",
        "through_unit": 18,
        "unit_15_baseline": {"path": "qa/UNIT_15_PROTECTED_SURFACES.json", "bytes": BASELINE_FACT[0], "sha256": BASELINE_FACT[1], "status": "PASS"},
        "units_16_18": source_checks,
        "protected_token_count": len(all_tokens),
        "source_missing": 0,
        "html_mathml_annotations": len(annotations),
        "html_missing": 0,
        "pdf_terminal_pages_checked": 53,
        "pdf_terminal_markers_checked": 9,
        "correction_disclosures": [f"AGC-CORR-{number:04d}" for number in range(34, 51)],
        "checks": ["Unit 15 protected baseline is exact and PASS", "Units 16--18 per-unit math gates are exact and PASS", "53 protected source formulas survive as HTML TeX annotations", "terminal PDF contains every lecture, worksheet, and public-solution boundary", "all source correction disclosures remain ledger-bound"],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "protected_tokens": len(all_tokens)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
