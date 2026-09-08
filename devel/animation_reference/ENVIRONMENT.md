# Animation environment evidence

Recorded 2026-09-06 and corrected 2026-09-07.

## Historical host inventory

The original bounded macOS check found no Microsoft PowerPoint application in `/Applications` or
`/Users/vosslab/Applications`. LibreOffice reported version 26.2.5.2:

```text
LibreOffice 26.2.5.2 cd7284b4cbbfeb507e630c1aac019f4157393acb
```

This is retained as host inventory only. It is not a project blocker: the instructor does not own
Microsoft products, and PPTX is used because Python supports it more effectively than ODP.

## Current bridge evidence

`slide_lib/libreoffice.py` provides the supported headless bridge for PPTX-to-ODP and ODP-to-PDF.
A direct UNO Python experiment was killed after it did not provide a suitable local route. The
headless bridge works and remains the programmatic conversion boundary.

The bridge preflight calls `ps -axo command=` to require LibreOffice to be closed. The sandbox denied
that command during the original observation, so attended or unsandboxed conversion evidence may
need normal host approval.

## 2026-09-07 implementation evidence

The bounded builder was generated into disposable PPTX fixtures and LibreOffice 26.2.5.2 converted
them headlessly to ODP and then PDF with an isolated profile. Package inspection retained timing
roots, shape and paragraph targets, visible-set APPEAR behavior, and the direct-IR FADE transition.
The ODP retained editable text and drawing objects, and the PDFs showed final reveal state. This is
one-time bridge/PDF evidence, not a permanent test or click-playback claim.

An attended launch attempt reached `soffice` but macOS denied Screen Recording and Accessibility
before F5 or any slideshow click could be sent. No attended behavior conclusion follows. Grant those
permissions to the automation process before repeating the minimal ODP observation.

## Consequence

Animation evidence follows official OOXML plus actual LibreOffice importer/exporter and Impress
behavior. No PowerPoint-authored decks, runtime XML templates, PowerPoint repair dialogs, or
PowerPoint playback checks are required.
