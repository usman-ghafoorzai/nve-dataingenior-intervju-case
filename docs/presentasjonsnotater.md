# Presentasjonsnotater

README er hele presentasjonen. Denne siden brukes til øving og kontroll, ikke som et ekstra kapittel under intervjuet.

## Tidsplan

| Del | Tid | Muntlig poeng |
|---|---:|---|
| Introduksjon og 1. Problem/verdi | 0:50 | To informasjonsbehov; teknisk gjennomførbarhet var den demonstrerte verdien. |
| 2. Domene | 0:40 | Treningsdata og legemiddelkontekst gjelder samme pasient, men er forskjellige datasett. |
| 3. Krav | 0:25 | Lagring, selektiv uthenting og etterprøvbarhet ga retning til implementasjonen. |
| 4. Arkitektur | 0:55 | Forklar ansvar og de to veiene; ikke les teknologitabellen rad for rad. |
| 5.1 Push | 1:15 | Følg figuren fra kilden til persistens. Skill kvittering fra sluttresultat. |
| 5.2 Pull | 1:15 | Følg forespørselen og svaret. Forklar tidsgrense og tom respons. |
| 5.3 Sammenligning | 0:30 | Ulik trigger, mekanisme og konsument. |
| 6. Datakvalitet | 1:20 | Input, modellskifte og sluttresultat. Lokal E2E og lagringskontroll utfylte hverandre. |
| 7. Ansvar | 1:00 | Stateless integrasjonsgrense, tekniske kontrakter og hva som måtte formaliseres. |
| 8. Designvalg | 1:05 | Problem, alternativ, valg og kostnaden ved en tilpasset pull-vei. |
| 9. CI/CD | 0:40 | PR-kontroller og begrensningen ved lokal full-stack-verifikasjon. |
| 10. Videre arbeid og avslutning | 1:05 | Prioriter neste steg og avslutt med tre prinsipper. |
| **Totalt** | **11:00** | Diagramforklaringer og overganger er inkludert. |

Planen legger opp til ca. 10–12 minutter og gir margin til 15. Dette er et redaksjonelt estimat, ikke en målt fremføring. Bruk stoppeklokke ved øving. Ved tidspress: kort ned teknologitabellen og sammenligningen; behold begge flytene, kvalitet og designvalget.

De fem diagrammene kan hver forklares på 30–90 sekunder. Pek på figuren, beskriv ett viktig poeng, og gå videre. Ikke les all støttetekst høyt.

## Dekning av NVE-oppgaven

| NVE-punkt | README |
|---|---|
| Formål, problem og forretningsverdi | Del 1; potensiell gevinst skilles fra demonstrert verdi. |
| Teknologier | Del 4; teknologi knyttes til ansvar. |
| Arkitektur fra kilde til konsument | Del 2–5; samlet arkitektur og separate flyter. |
| Datakvalitet og testing | Del 5–6; validering, transformasjon, persistens/uthenting og verifikasjon. |
| Eierskap, ansvar og kontrakter | Del 7; faktisk komponentansvar skilles fra forslag til formalisering. |
| Utfordring og løsning | Del 8; arkitekturasymmetri, alternativ og trade-off. |
| Læring og forbedringer | Del 8 og 10 samt avslutning. |
| Kodeorganisering, valgfritt | Del 9; generiske ansvarsområder uten interne stier. |
| CI/CD, valgfritt | Del 9; PR til integrasjon, med eksplisitt E2E-begrensning. |

## Presisjon ved spørsmål

- «Toveis» betyr to ulike dataflyter. Pull er ikke en reversering av de innsendte treningsdataene.
- Tidsfiltrert uthenting betyr ikke komplett synkronisering eller konflikthåndtering.
- FHIR-representasjon betyr ikke at det tilpassede pull-grensesnittet er et standardkompatibelt FHIR-søk.
- Tester av struktur og mapping betyr ikke at klinisk betydning er validert av helsepersonell.
- Teknisk komponentansvar betyr ikke formelt dataeierskap eller komplett driftsorganisasjon.
- Bruk «vi» om dokumentert fellesarbeid. Konkretiser egne bidrag muntlig ut fra det du selv faktisk gjorde.

## Vedlikehold av figurer

De fem SVG-filene i `diagrammer/` genereres fra `lag_diagrammer.py` med Python 3 og standardbiblioteket. Kjør `python docs/lag_diagrammer.py` fra repoets rot etter endringer. Ingen private kilder leses av generatoren. SVG-ene vises direkte i README på GitHub.
