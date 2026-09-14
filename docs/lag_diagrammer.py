"""Lag sju selvstendige SVG-diagrammer fra sanitiserte begreper.

Krever bare Python 3. Ingen private filer eller nettverk brukes.
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent / "diagrammer"
INK = "#172b44"
MUTED = "#526477"
PUSH = "#a54b13"
PULL = "#08776f"
BLUE = "#2159a5"
PARTS = []


def text(x, y, value, size=18, color=INK, weight=400, anchor="start"):
    PARTS.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
                 f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def begin(title, subtitle, height, description):
    PARTS.clear()
    PARTS.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
                 f'viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">')
    PARTS.append(f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>')
    PARTS.append('<defs>')
    for name, color in [("neutral", MUTED), ("push", PUSH), ("pull", PULL)]:
        PARTS.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                     f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')
    PARTS.append('</defs><g font-family="Arial, Helvetica, sans-serif">')
    PARTS.append(f'<rect width="1200" height="{height}" rx="0" fill="#ffffff"/>')
    text(30, 37, title, 30, "#111111", weight=700)
    text(30, 66, subtitle, 17, MUTED)


def arrow(points, kind="neutral", both=False, dashed=False):
    color = {"neutral": MUTED, "push": PUSH, "pull": PULL}[kind]
    pts = " ".join(f"{x},{y}" for x, y in points)
    extra = f' marker-start="url(#{kind})"' if both else ""
    extra += ' stroke-dasharray="6 5"' if dashed else ""
    PARTS.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.3" '
                 f'stroke-linejoin="round" marker-end="url(#{kind})"{extra}/>')


def end(name):
    PARTS.append('</g></svg>')
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text("\n".join(PARTS) + "\n", encoding="utf-8")


def sheet(title, subtitle, height, description):
    begin(title, subtitle, height, description)


def panel(x, y, w, h, fill="#eaf3ff", dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    PARTS.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
                 f'fill="{fill}" stroke="#87919c" stroke-width="1.2"{dash}/>')


def centered(x, y, lines, size=19, weight=400, color=INK):
    for i, line in enumerate(lines):
        text(x, y + i * 25, line, size, color, weight, "middle")


def concept(x, y, w, h, lines, fill="#dcecff"):
    panel(x, y, w, h, fill)
    centered(x + w / 2, y + h / 2 - (len(lines)-1)*12.5 + 7, lines, 20, 700)


def association(points, label=None, lx=0, ly=0):
    pts = " ".join(f"{x},{y}" for x, y in points)
    PARTS.append(f'<polyline points="{pts}" fill="none" stroke="#444444" stroke-width="2"/>')
    if label:
        text(lx, ly, label, 17, MUTED, anchor="middle")


def actor(x, y, label, color):
    PARTS.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#ffffff" stroke="{color}" stroke-width="3"/>')
    association([(x, y+17), (x, y+69)])
    association([(x-31, y+37), (x+31, y+37)])
    association([(x-29, y+109), (x, y+69), (x+29, y+109)])
    text(x, y+140, label, 20, weight=700, anchor="middle")


def use_case():
    sheet("Use Case", "Hvem trenger å gjøre hva?", 575,
          "Kildeapplikasjonen overfører treningsdata til strukturert lagring. Konsumenten henter relevant "
          "klinisk kontekst. Det simulerte EPJ-miljøet deltar som støttesystem for begge handlinger.")
    panel(300, 100, 555, 405)
    centered(577, 135, ["Integrasjonsløsning"], 22, 700)
    actor(130, 163, "Kildeapplikasjon", PUSH)
    actor(130, 356, "Konsument", PULL)
    concept(948, 260, 222, 110, ["Simulert", "EPJ-miljø"], "#fff3cd")
    association([(130, 232), (377, 232)])
    association([(130, 425), (377, 425)])
    association([(778, 232), (905, 232), (905, 292), (948, 292)])
    association([(778, 425), (905, 425), (905, 340), (948, 340)])
    for cy, lines, color, fill in [(232, ["Overføre treningsdata", "til strukturert lagring"], PUSH, "#ffe6c9"),
                                   (425, ["Hente relevant", "klinisk kontekst"], PULL, "#dff2e2")]:
        PARTS.append(f'<ellipse cx="577" cy="{cy}" rx="200" ry="61" fill="{fill}" stroke="{color}" stroke-width="2"/>')
        centered(577, cy-7, lines, 22)
    text(30, 550, "Aktørene viser systemroller. Samme applikasjon kan være både kilde og konsument.", 18, MUTED)
    end("01-use-case.svg")


def domain():
    sheet("Domenemodell", "Hvilke begreper og data handler flytene om?", 540,
          "En pasient gjennomfører treningsøkter som gir treningsdata. Kildeapplikasjonen produserer "
          "dataene. Klinisk kontekst gjelder pasienten og finnes i det simulerte EPJ-miljøet.")
    concept(35, 130, 225, 90, ["Pasient"], "#dcecff")
    concept(410, 130, 240, 90, ["Treningsøkt"], "#fff2bf")
    concept(860, 130, 305, 90, ["Treningsdata"], "#f6dde2")
    concept(35, 325, 260, 95, ["Klinisk kontekst", "(legemiddelinformasjon)"], "#eaddf4")
    concept(440, 325, 290, 95, ["Simulert EPJ-miljø"], "#dff0df")
    concept(890, 325, 275, 95, ["Kildeapplikasjon", "(også konsument)"], "#dcecff")
    arrow([(260, 175), (410, 175)])
    text(335, 158, "gjennomfører", 18, MUTED, anchor="middle")
    arrow([(650, 175), (860, 175)])
    text(755, 158, "gir", 18, MUTED, anchor="middle")
    arrow([(148, 325), (148, 220)])
    text(166, 274, "gjelder", 18, MUTED)
    arrow([(440, 372), (295, 372)])
    text(367, 355, "inneholder", 18, MUTED, anchor="middle")
    arrow([(1027, 325), (1027, 220)])
    text(1045, 274, "produserer", 18, MUTED)
    arrow([(165, 420), (165, 475), (1027, 475), (1027, 420)])
    text(590, 461, "kan brukes av", 18, MUTED, anchor="middle")
    text(30, 522, "Hver økt gjelder én pasient. Helsepersonell er tiltenkt bruker; klinisk bruk ble ikke evaluert.", 18, MUTED)
    end("02-domene.svg")


def information():
    sheet("Informasjonsflyt", "Hvilken informasjon skal flyte hvor?", 568,
          "Treningsdata går fra kilde via integrasjonsgrensen til EPJ. Konsumenten ber om klinisk "
          "kontekst og får denne tilbake via integrasjonsgrensen. Dette er forskjellige datasett.")
    for x, w, label, fill in [(30, 255, "Kilde / konsument", "#eaf3ff"),
                              (465, 260, "Integrasjonsgrense", "#f0eafa"),
                              (905, 265, "Simulert EPJ-miljø", "#e8f3e8")]:
        panel(x, 110, w, 372, fill)
        text(x+w/2, 144, label, 21, weight=700, anchor="middle")
    centered(157, 213, ["Treningsdata", "oppstår her"], 20, 700)
    centered(595, 213, ["Formidler", "treningsdata"], 20, 700)
    centered(1037, 213, ["Treningsdata", "lagres strukturert"], 20, 700)
    for a,b in [(285,465),(725,905)]:
        arrow([(a, 247), (b, 247)], "push")
        text((a+b)/2, 230, "Treningsdata", 18, PUSH, anchor="middle")
    centered(157, 393, ["Konsumenten trenger", "klinisk kontekst"], 20, 700)
    centered(595, 393, ["Formidler utvalgt", "klinisk kontekst"], 20, 700)
    centered(1037, 393, ["Klinisk kontekst", "finnes her"], 20, 700)
    for a,b in [(285,465),(725,905)]:
        arrow([(a, 320), (b, 320)], "pull", dashed=True)
        text((a+b)/2, 303, "Ber om kontekst", 17, PULL, anchor="middle")
        arrow([(b, 445), (a, 445)], "pull")
        text((a+b)/2, 430, "Klinisk kontekst", 17, PULL, anchor="middle")
    text(30, 523, "Heltrukket pil: dataretning. Stiplet pil: forespørselen som initierer pull.", 18, MUTED)
    text(30, 550, "Pull gjelder legemiddelkontekst, ikke en retur av treningsdataene fra push.", 18, MUTED)
    end("03-informasjonsflyt.svg")


def technical_box(x, y, w, h, title, lines, fill="#ffffff"):
    panel(x, y, w, h, fill)
    centered(x+w/2, y+29, [title], 20, 700)
    centered(x+w/2, y+56, lines, 18)


def architecture():
    sheet("Teknisk arkitektur", "Hvordan realiseres de to dataflytene?", 825,
          "Fire logiske lag: applikasjon, integrasjon, semantisk mapping og klinisk datalag. "
          "Push bruker FHIR-server og Subscription. Pull bruker en separat forespørselsstyrt uthentingsvei. "
          "EHRbase og HAPI FHIR bruker PostgreSQL til persistens.")
    for y, h, label, line in [(105, 128, "Applikasjonslag", "Kilde og konsument"),
                              (258, 158, "Integrasjonslag", "Validering og utveksling"),
                              (441, 139, "Semantisk mapping", "Transformasjon og uthenting"),
                              (605, 155, "Klinisk datalag", "Strukturert lagring")]:
        panel(20, y, 1160, h, "#e4f0ff")
        text(37, y+43, label, 21, weight=700)
        text(37, y+69, line, 16, MUTED)
    panel(680, 273, 490, 476, "none", dashed=True)
    centered(1057, 300, ["Simulert", "EPJ-miljø"], 18, 700, MUTED)
    technical_box(300, 132, 240, 77, "Kilde / konsument", ["Sender eller spør"], "#fff3cd")
    technical_box(300, 285, 240, 105, "Integrasjonsgrense", ["NestJS / TypeScript", "Validerer og tilpasser"], "#f0eafa")
    technical_box(715, 285, 230, 105, "FHIR-server", ["HAPI FHIR", "Ressurser / Subscription"], "#ffe6c9")
    technical_box(715, 467, 230, 87, "Mapping / uthenting", ["Java / Spring"], "#f0eafa")
    technical_box(715, 633, 230, 99, "EHRbase", ["openEHR-representasjon", "Lagrer og henter"], "#e5f3e5")
    technical_box(1000, 633, 160, 99, "PostgreSQL", ["Persistent", "lagring"], "#fff3cd")
    arrow([(420, 209), (420, 285)], both=True)
    arrow([(540, 330), (715, 330)], "push")
    text(627, 316, "Push · FHIR", 18, PUSH, anchor="middle")
    arrow([(830, 390), (830, 467)], "push")
    text(847, 432, "Subscription", 17, PUSH)
    arrow([(420, 390), (420, 511), (715, 511)], "pull", both=True)
    text(558, 470, "Pull · separat uthentingsvei", 17, PULL, anchor="middle")
    text(558, 493, "Forespørsel / svar", 17, PULL, anchor="middle")
    arrow([(830, 554), (830, 633)], both=True)
    text(847, 596, "Lagre / hente", 17, MUTED)
    arrow([(945, 682), (1000, 682)], both=True)
    text(30, 792, "HAPI FHIR bruker også PostgreSQL for tjenestedata. Docker Compose samordnet testmiljøet.", 18, MUTED)
    end("04-arkitektur.svg")


def push_flow():
    sheet("Push – fra kilde til strukturert lagring", "Kilden initierer innsending; en hendelse driver videresendingen", 543,
          "Kildeapplikasjonen sender syntetiske treningsdata. Integrasjonsgrensen validerer og "
          "transformerer til FHIR. Subscription videresender til semantisk mapping og openEHR-lagring. "
          "Verifikasjon av FHIR-resultat og persistens er vist som en separat kontrollaktivitet.")
    panel(20, 99, 1160, 175, "#eaf3ff")
    text(38, 128, "Kilde, integrasjon og utveksling", 19, weight=700)
    panel(400, 322, 780, 172, "#eaf3ff")
    text(418, 350, "Mapping og klinisk lagring", 19, weight=700)
    technical_box(40, 153, 280, 99, "Kildeapplikasjon", ["Syntetiske treningsdata", "Pasienttilknytning"], "#fff3cd")
    technical_box(460, 153, 280, 99, "Integrasjonsgrense", ["Validerer input", "Kildeformat → FHIR"], "#f0eafa")
    technical_box(880, 153, 280, 99, "FHIR-server", ["Lagrer Observation"], "#ffe6c9")
    technical_box(880, 370, 280, 99, "Semantisk mapping", ["FHIR → openEHR"], "#f0eafa")
    technical_box(460, 370, 280, 99, "Klinisk repository", ["Lagrer composition", "Strukturert persistens"], "#e5f3e5")
    technical_box(40, 370, 280, 99, "Verifikasjon", ["FHIR-resultat og", "lagret openEHR-innhold"], "#f2f3f5")
    arrow([(320, 203), (460, 203)], "push")
    text(390, 187, "Input", 18, PUSH, anchor="middle")
    arrow([(740, 203), (880, 203)], "push")
    text(810, 187, "FHIR", 18, PUSH, anchor="middle")
    arrow([(1020, 252), (1020, 370)], "push")
    text(1036, 303, "Subscription", 17, PUSH)
    arrow([(880, 419), (740, 419)], "push")
    text(810, 405, "openEHR", 18, PUSH, anchor="middle")
    arrow([(460, 419), (320, 419)], dashed=True)
    text(390, 405, "Kontroller", 17, MUTED, anchor="middle")
    text(30, 524, "Stiplet pil viser kontroll av resultatet. En kvittering ved innsending bekrefter ikke hele kjeden.", 18, MUTED)
    end("05-push.svg")


def pull_flow():
    sheet("Pull – fra klinisk kontekst til konsument", "Konsumenten initierer en forespørsel om utvalgt kontekst", 543,
          "Forespørselen inneholder valgt pasient og kjent oppdateringstid. Etter validering koordineres "
          "journaloppslag og tidsfiltrert AQL-uthenting. openEHR-konteksten transformeres til FHIR og "
          "videre til konsumentformat. Ingen nye data gir en tom liste.")
    panel(20, 99, 1160, 175, "#eaf3ff")
    text(38, 128, "Forespørsel og uthenting", 19, weight=700)
    panel(20, 322, 1160, 172, "#eaf3ff")
    text(38, 350, "Klinisk kontekst tilbake til konsumenten", 19, weight=700)
    technical_box(40, 153, 280, 99, "Konsument", ["Valgt pasient", "Sist kjente oppdatering"], "#fff3cd")
    technical_box(460, 153, 280, 99, "Integrasjonsgrense", ["Validerer forespørselen", "Koordinerer kall"], "#f0eafa")
    technical_box(880, 153, 280, 99, "Uthentingslag", ["Journaloppslag", "AQL / tidsfiltrering"], "#f0eafa")
    technical_box(880, 370, 280, 99, "Klinisk repository", ["Strukturert klinisk kontekst", "openEHR"], "#e5f3e5")
    technical_box(460, 370, 280, 99, "Mapping", ["openEHR → FHIR", "Legemiddelkontekst"], "#f0eafa")
    technical_box(40, 370, 280, 99, "Respons via grensen", ["FHIR → konsumentformat", "Data eller tom liste"], "#dff2e2")
    arrow([(320, 203), (460, 203)], "pull")
    text(390, 187, "Forespørsel", 17, PULL, anchor="middle")
    arrow([(740, 203), (880, 203)], "pull")
    text(810, 187, "Pasient / tid", 17, PULL, anchor="middle")
    arrow([(1020, 252), (1020, 370)], "pull")
    text(1036, 303, "Uthenting", 17, PULL)
    arrow([(880, 419), (740, 419)], "pull")
    text(810, 405, "openEHR", 18, PULL, anchor="middle")
    arrow([(460, 419), (320, 419)], "pull")
    text(390, 405, "FHIR", 18, PULL, anchor="middle")
    text(30, 524, "Verifikasjon: riktig utvalg, tidsfilter og respons. Integrasjonsgrensen har ingen egen polling.", 18, MUTED)
    end("06-pull.svg")


def quality():
    sheet("Datakvalitet og verifisering", "Kontrollmodell for begge flytene – ikke et teknisk sekvensdiagram", 425,
          "Validering, transformasjon og lagring eller uthenting skilles fra kontrollen av resultatet. "
          "Push kontrolleres med FHIR-resultat og EHRbase-inspeksjon. Pull kontrolleres med "
          "AQL/API-verifikasjon av utvalg og forventet respons, inkludert tom liste.")
    xs = [30, 325, 620, 915]
    for x, heading in zip(xs, ["VALIDER", "TRANSFORMER", "LAGRE / HENT", "VERIFISER"]):
        text(x+10, 114, heading, 19, weight=700)
    push = [("Push · input", ["DTO-struktur", "API-grense"]),
            ("Mapping", ["Kilde → FHIR", "FHIR → openEHR"]),
            ("Persister", ["openEHR composition", "i klinisk repository"]),
            ("Kontroller persistens", ["FHIR-resultat og", "EHRbase-inspeksjon"])]
    pull = [("Pull · forespørsel", ["Pasienttilknytning", "Tidsgrense"]),
            ("Mapping / parsing", ["openEHR → FHIR", "→ konsumentformat"]),
            ("Hent utvalg", ["Pasient og tidsfilter", "fra klinisk repository"]),
            ("Kontroller respons", ["AQL-/API-kontroll", "Riktig utvalg / tom liste"])]
    for y, data, fill in [(133, push, "#fff0df"), (264, pull, "#e7f4e9")]:
        panel(20, y, 1160, 108, fill)
        for i, (head, lines) in enumerate(data):
            x = xs[i]
            text(x+10, y+30, head, 19, weight=700)
            for j, line in enumerate(lines):
                text(x+10, y+58+j*24, line, 18)
            if i<3:
                arrow([(x+246, y+53), (x+287, y+53)])
    text(30, 407, "Unit tests og API-tester ble supplert med lokal E2E og manuell verifikasjon av den samlede flyten.", 18, MUTED)
    end("07-datakvalitet.svg")


if __name__ == "__main__":
    use_case()
    domain()
    information()
    architecture()
    push_flow()
    pull_flow()
    quality()
    print("Opprettet sju SVG-diagrammer i docs/diagrammer/.")
