---
title: BINARY CLOCK
section: 1
header: User Manual
footer: BINARY CLOCK 1.0.0
date: 12 MAJ 2023
---

# DESCRIPTION
Opgaven går ud på at lave et program, der implementerer et binært ur til en Raspberry Pi, med brug af LED'erne på SenseHat'en til at vise uret som timer, minutter og sekunder. Uret skal kunne vise tiden både i 12-timers og 24-timers format, og skifte mellem en lodret og vandret visning.

Brugeren skal kunne vælge mellem disse indstillinger både ved opstart af programmet via kommandolinje argumenter og ved brug af mini-joysticket på SenseHat'en. Programmet skal håndtere forskellige afbrydelser, såsom Control-C, på en kontrolleret måde og skal give en besked både ved start og stop af programmet.

Programmet skal også implementeres som en systemd service, der starter automatisk, men også kan startes fra kommandolinjen med argumenter.

Der skal være detaljeret dokumentation af programkoden med Docstrings og en manual-side med en detaljeret brugervejledning, der blandt andet forklarer hvordan man bruger kommandolinje parametrene til at ændre display-indstillingerne, og hvordan man starter og stopper programmet som service.

# OPTIONS
VERTICAL.
true - vises uret verticalt på sensehat.
false - vises uret horisontalt på sensehat.

AM_PM
true - vises uret i 12 timers format, som AM/PM.
false - vises uret i 24 timers format.

# LAVET AF
Martin
Oskar
Rasmus


