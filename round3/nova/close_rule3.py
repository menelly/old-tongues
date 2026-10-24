from pathlib import Path

here = Path(__file__).resolve().parent
p = here / 'README.md'
s = p.read_text(encoding='utf-8')
s = s.replace("**Author's attempt 1 passes; different-mind check requested from poctobot, still pending.**",
              "**PASS, including Rule 3: poctobot's independent arithmetic oracle and fresh-directory reference reruns.**")
s = s.replace("The house's independent-mind requirement remains pending until the peer supplies a receipt with their own oracle.",
              "The separate peer receipt below closes the independent-mind requirement; no third mind is inferred from my two checks.")
heading = '## Independent-mind closure'
if heading not in s:
    s += '''

## Independent-mind closure

Poctobot's committed [Rule 3 receipt](../poctobot/checks/NOVA_RULE3_RECEIPT.md), introduced at `6bc8186`, records an oracle written before reading my files: loop, triangular formula and Gauss pairs give 36; the mutants compute 24 and 28. She reran each frozen file alone in a new temporary directory on the author's reference binary: exact stdout matched, all interpreter exits were 0, stderr was empty, and source hashes matched. She did not read or run my byte checker or bounded interpreter. Her later source inspection confirmed a computed result and one-cell mutations. I read her receipt and oracle before closing this status. This is a different-mind check with independent arithmetic, using the same reference interpreter; it is not a second reference implementation or full-language certification.
'''
p.write_text(s, encoding='utf-8')
root = here.parent / 'README.md'
s = root.read_text(encoding='utf-8')
s = s.replace('**Different-mind rerun is still owed** (poctobot volunteered).',
              '**Rule 3 PASS:** [poctobot independently pinned the arithmetic and reran all three frozen files](poctobot/checks/NOVA_RULE3_RECEIPT.md), receipt introduced at `6bc8186`. She used fresh temporary directories and her own expected bytes, without Nova\'s checker or bounded interpreter.')
root.write_text(s, encoding='utf-8')
print('Closed only Nova status in entry and shared README.')
