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
    PARTS.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="{height}" '
                 f'viewBox="0 0 1040 {height}" role="img" aria-labelledby="title desc">')
    PARTS.append(f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>')
    PARTS.append('<defs>')
    for name, color in [("neutral", MUTED), ("push", PUSH), ("pull", PULL)]:
        PARTS.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                     f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')
    PARTS.append('</defs><g font-family="Arial, Helvetica, sans-serif">')
    PARTS.append(f'<rect width="1040" height="{height}" rx="16" fill="#ffffff"/>')
    text(30, 37, title, 25, weight=700)
    text(30, 66, subtitle, 17, MUTED)


def box(x, y, w, h, title, lines=(), color=BLUE, fill="#eff5fd"):
    PARTS.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                 f'fill="{fill}" stroke="{color}" stroke-width="1.4"/>')
    text(x + 17, y + 29, title, 19, color, 700)
    for i, line in enumerate(lines):
        text(x + 17, y + 56 + 23 * i, line, 17)


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
    PARTS[0] = PARTS[0].replace('width="1040"', 'width="1200"').replace('1040 ', '1200 ')
    # Samme hvite flate, svart overskrift og diskrete rammer i alle analysefigurene.
    for i, part in enumerate(PARTS):
        if '<rect width="1040"' in part:
            PARTS[i] = part.replace('1040', '1200').replace('rx="16"', 'rx="0"')
        elif '<text x="30" y="37"' in part:
            PARTS[i] = part.replace('font-size="25"', 'font-size="30"').replace(INK, '#111111')


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
    end("02-use-case.svg")


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
    end("03-domene.svg")


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
    end("04-informasjonsflyt.svg")


def architecture():
    begin("Felles arkitektur, to veier", "Logiske komponenter i den implementerte PoC-en", 578,
          "Kilde og konsument bruker integrasjonsgrensen. Push går via FHIR-serveren og Subscription "
          "til mapping og repository. Pull går direkte til mapping- og uthentingslaget. "
          "EPJ-tjenestene bruker PostgreSQL for persistens.")
    PARTS.append('<rect x="558" y="92" width="456" height="425" rx="14" fill="#f8fafc" '
                 'stroke="#aebaca" stroke-dasharray="7 5"/>')
    text(578, 119, "SIMULERT EPJ-MILJØ", 15, MUTED, 700)
    box(30, 233, 200, 104, "Kilde / konsument", ["Sender treningsdata", "Ber om kontekst"])
    box(298, 233, 210, 104, "Integrasjonsgrense", ["Validerer / tilpasser", "Koordinerer kall"])
    box(582, 150, 190, 102, "FHIR-server", ["Utveksling", "Subscription"], PUSH, "#fff4eb")
    box(582, 336, 190, 102, "Mapping", ["Modellskifte", "Uthenting / filter"])
    box(812, 336, 180, 102, "Repository", ["openEHR", "Lagrer / henter"])
    arrow([(230, 279), (298, 279)], both=True)
    arrow([(405, 233), (405, 192), (582, 192)], "push")
    text(414, 178, "PUSH", 16, PUSH, 700)
    arrow([(677, 252), (677, 336)], "push")
    text(692, 299, "Hendelse", 16, PUSH)
    arrow([(405, 337), (405, 387), (582, 387)], "pull", both=True)
    text(417, 374, "PULL", 16, PULL, 700)
    text(417, 414, "Forespørsel / svar", 16, PULL)
    arrow([(772, 387), (812, 387)], both=True)
    text(582, 483, "PostgreSQL: persistens for EPJ-tjenestene", 17, MUTED)
    text(30, 554, "Pull går direkte til uthentingslaget. Docker Compose samordnet det lokale miljøet.", 17, MUTED)
    end("05-arkitektur.svg")


def flow(name, title, subtitle, labels, color, fill, kind, footer, desc):
    begin(title, subtitle, 444, desc)
    positions = [(30, 105), (385, 105), (740, 105), (740, 282), (385, 282), (30, 282)]
    for i, ((x, y), (head, lines)) in enumerate(zip(positions, labels), 1):
        box(x, y, 270, 105, f"{i}. {head}", lines, color, fill)
    arrow([(300, 157), (385, 157)], kind)
    arrow([(655, 157), (740, 157)], kind)
    arrow([(875, 210), (875, 282)], kind)
    arrow([(740, 334), (655, 334)], kind)
    arrow([(385, 334), (300, 334)], kind)
    text(30, 427, footer, 17, MUTED)
    end(name)


def quality():
    begin("Kvalitet gjennom begge flytene", "Dokumenterte kontrollnivåer · struktur, modellskifte og faktisk resultat", 395,
          "Begge flytene har inputvalidering og transformasjonstester. Push-verifikasjon omfatter "
          "FHIR-resultat og separat kontroll av openEHR-persistens. Pull-verifikasjon omfatter "
          "AQL-uthenting, tidsfiltrering og respons med data eller tom liste.")
    headers = ["VALIDER", "TRANSFORMER", "LAGRE / HENT", "VERIFISER"]
    for x, heading in zip([30, 285, 540, 795], headers):
        text(x, 108, heading, 16, MUTED, 700)
    push = [("Push · input", ["DTO-struktur", "API-grense"]),
            ("Mapping", ["Kilde → FHIR", "FHIR → openEHR"]),
            ("Persistens", ["FHIR-resultat", "EHRbase-inspeksjon"]),
            ("Sluttresultat", ["Forventet struktur", "i lagrede data"])]
    pull = [("Pull · forespørsel", ["Pasienttilknytning", "Tidsgrense"]),
            ("Mapping / parsing", ["openEHR → FHIR", "→ konsumentformat"]),
            ("Uthenting", ["AQL-verifikasjon", "Tidsfiltrering"]),
            ("Sluttresultat", ["Utvalgt kontekst", "eller tom liste"])]
    for y, data, color, fill, kind in [(124, push, PUSH, "#fff4eb", "push"),
                                      (244, pull, PULL, "#edf9f6", "pull")]:
        for i, (head, lines) in enumerate(data):
            x = 30 + i * 255
            box(x, y, 225, 100, head, lines, color, fill)
            if i < 3:
                arrow([(x + 225, y + 50), (x + 255, y + 50)], kind)
    text(30, 377, "Unit tests og API-tester + lokal E2E og manuell kontroll. Full-stack E2E var utenfor standard CI.", 17, MUTED)
    end("08-datakvalitet.svg")


if __name__ == "__main__":
    use_case()
    domain()
    information()
    architecture()
    flow("06-push.svg", "Push: nye treningsdata inn", "Initiert av kilden · les øvre rad mot høyre, deretter ned og tilbake", [
        ("Kilden sender", ["Syntetiske øktdata", "Knyttet til pasient"]),
        ("Integrasjonsgrense", ["Validerer input", "Kildeformat → FHIR"]),
        ("FHIR-server", ["Lagrer ressurs", "Subscription videresender"]),
        ("Mapping", ["Semantisk transformasjon", "FHIR → openEHR"]),
        ("Klinisk repository", ["Strukturert composition", "Persistent lagring"]),
        ("Kontroll av resultat", ["FHIR-representasjon", "Faktisk openEHR-innhold"]),
    ], PUSH, "#fff4eb", "push",
         "Kvittering ved innsending og kontroll av ferdig lagring er ulike verifikasjonspunkter.",
         "Syntetiske treningsdata går fra kilde via inputvalidering og FHIR-representasjon til "
         "Subscription, mapping til openEHR, lagring og kontroll av faktisk resultat.")
    flow("07-pull.svg", "Pull: klinisk kontekst tilbake", "Initiert av konsumenten · les øvre rad mot høyre, deretter ned og tilbake", [
        ("Konsumenten spør", ["Valgt pasient", "Sist kjente oppdatering"]),
        ("Integrasjonsgrense", ["Validerer forespørselen", "Koordinerer uthenting"]),
        ("Uthentingslag", ["Journaloppslag / tidsfilter", "AQL-basert uthenting"]),
        ("Klinisk repository", ["Strukturert klinisk kontekst", "openEHR"]),
        ("Mapping", ["openEHR → FHIR", "Legemiddelkontekst"]),
        ("Respons via grensen", ["FHIR → konsumentformat", "Data eller tom liste"]),
    ], PULL, "#edf9f6", "pull",
         "Verifikasjon: uthentet innhold, tidsfilter og respons. Ingen egen polling i integrasjonsgrensen.",
         "En validert forespørsel går til uthentingslaget og repositoryet. Utvalgt klinisk kontekst "
         "transformeres fra openEHR via FHIR til konsumentformat. Ingen nye data gir tom liste.")
    quality()
    print("Opprettet sju SVG-diagrammer i docs/diagrammer/.")
