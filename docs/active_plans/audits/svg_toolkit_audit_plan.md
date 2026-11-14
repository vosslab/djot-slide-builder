# SVG toolkit independent plan review

## Finding

- **Low — The plan's self-contained output promise is ambiguous.** `docs/active_plans/active/svg_toolkit_plan.md:54`-55 says output stays self-contained, but `docs/active_plans/active/svg_toolkit_progress.md:51` records that live fonts are deliberately unembedded and must be installed. A reader relying on the plan alone could expect identical typography on another machine without font setup. The implementation report correctly discloses the dependency (`docs/SVG_TOOLKIT_IMPLEMENTATION_REPORT.md:5`). Clarify the plan's wording to say that SVG geometry and resources are contained while the named fonts require installation, consistent with the settled decision. No font embedding mechanism is needed.

## Assessment and limits

The scope, milestone dependencies, preservation policy, and recovery register have coherent ties to the intended use. In particular, preservation of source facts and native slide content is a product requirement, and the two fresh author trials address the LLM-facing goal. Native checks and full-page visual reviews provide relevant evidence for the selected figures. The documented 351-slide build is historical, not a current whole-deck visual review; small labels, other installations, and live display remain unverified, as the final integration report says.

The recorded byte matches provide traceability between regenerated, reviewed, and embedded artifacts and support the narrow unchanged-source claim. I found no plan requirement that improved artwork match original pixels or bytes, nor a new blocking arbitrary performance threshold. If regeneration bytes differ, compare actual scientific content and rendered output, review any meaningful change, and refresh the affected proof and hashes; byte differences alone do not establish a product failure. The risk register identifies correction owners and recovery for the material acceptance risks. I found no concrete scope-creep or partial-migration finding in the inspected plan and closeout evidence.

This is a plan and evidence review, not an independent rerun of tests, full visual audit, or exhaustive review of implementation contracts. No permanent test is proposed; the test reviewer owns the separate detailed permanent-test assessment.
