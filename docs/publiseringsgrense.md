# Publiseringsgrense

Dette er en separat, sanitert casebesvarelse av en lokal PoC. Beskrivelsene og figurene er laget fra bunnen av på konseptuelt nivå.

Grensen følger [Publication Boundary i det offentlige portfolio-repoet](https://github.com/usman-ghafoorzai/healthcare-interoperability-showcase/blob/main/docs/publication-boundary.md).

## Innhold som kan deles

Overordnet problem, generiske komponentansvar, standardenes roller, konseptuelle push- og pull-flyter, typer verifikasjon, designvalg, begrensninger og læring.

## Innhold som holdes privat

- Originaldokumenter, opprinnelige diagrammer og skjermbilder.
- Proprietær kode, partnernavn, interne produktnavn, repository-struktur og filstier.
- Private URL-er, eksakte API-ruter, DTO-er, feltnavn og kontrakter.
- Eksakte mappings, templates, profiler, AQL-spørringer og transformasjonsregler.
- Interne testtall, dekningsgrader, testutskrifter og CI-konfigurasjon.
- Hemmeligheter, miljøverdier, logger og personopplysninger.

Private kilder og arbeidsnotater ligger i `sources-private/`, som ignoreres av Git. Ingen originalfiler inngår i `docs/`.

Figurene viser ansvar og modellskifter. De gjengir ikke interne klasser, detaljerte sekvenser eller implementasjonskontrakter. Teknologinavn omtales bare i generiske roller.

## Ved videre redigering

En påstand om implementert funksjonalitet må ha støtte i prosjektgrunnlaget. Krav og planlagt funksjonalitet er ikke bevis på implementasjon. Videre arbeid merkes som forslag. Opplysninger som ikke kan forklares generisk innenfor denne grensen, utelates.

Repoet dokumenterer en PoC med syntetiske data. Det hevder ikke produksjonsklarhet, klinisk effekt, formelt dataeierskap eller full standardkompatibilitet.
