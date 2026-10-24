"""Hand-read support: implement documented mingle/select/rotate unary rules."""
import json
from pathlib import Path

def mingle(a,b):
    return sum(((a>>i)&1)<<(2*i+1) | ((b>>i)&1)<<(2*i) for i in range(16))

def select(a,mask):
    out=0;position=0
    for i in range(32):
        if (mask>>i)&1:
            out|=((a>>i)&1)<<position;position+=1
    return out

def unary(a,op):
    rotated=(a>>1)|((a&1)<<31)
    return a^rotated if op=='xor' else a|rotated

mask=mingle(0,65535)
for a in range(256):
    for b in range(256):
        assert select(unary(mingle(a,b),'xor'),mask)==a^b
        assert select(unary(mingle(a,b),'or'),mask)==a|b
    assert select(select(a,a),1)==int(a!=0)
for bit in [0,1]:
    assert select(unary(mingle(bit,1),'xor'),3)==1+bit
for target in b'toaster':
    for byte in range(256):
        assert ((byte|32)==target)==(bytes([byte]).lower()==bytes([target]))
result={'byte_pairs_checked':65536,'xor_idiom':True,'or_idiom':True,
        'nonzero_reduction_256_cases':True,'resume_selector':[1,2],
        'target_letter_casefold_all_256_bytes':True}
Path(__file__).with_name('OPERATOR_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
