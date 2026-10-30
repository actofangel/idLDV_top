# idLDV
The Identity of Leonardo da Vinci

(Project2)

[Visit our Wiki](https://github.com/actofangel/idLDV/wiki)

[Web Resource](https://github.com/actofangel/idLDV/wiki/Links1)

## Site structure

A static site ready for GitHub Pages (branch `main`, root). Each page is a single HTML file with its styles inline.

| File | Content |
|---|---|
| `index.html` | Overview and the three kinds of statement (fact, interpretation, hypothesis) |
| `method.html` | Method: layer purity, source admission rules, verifiability |
| `last-supper.html` | Three-layer analysis model of the Last Supper and working hypotheses |
| `database.html` | Reference database viewer (reads `data/*.json`) |
| `sources.html` | Admitted source categories and registered sources |

## Reference database

```
data/
  works.json                  works (fact layer only)
  datings.json                datings (fact or interpretation layer)
  attributions.json           attributions (interpretation layer only)
  source_records.json         source records (admitted categories only)
  interpretation_claims.json  interpretation claims and working hypotheses
  schema/                     JSON schema for each collection
```

Run the validator after adding records. It also runs in GitHub Actions on every push that changes `data/` or `tools/`.

```bash
pip install jsonschema
python3 tools/validate.py
```

Checks: schema conformance, every source reference points to a record in `source_records.json`, no interpretation or hypothesis record carries certainty "fact", unique ids and referential integrity. Interpretation claims without a falsification condition, and geometric claims without a verification script, produce warnings.
