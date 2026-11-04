# Independent hand-check of frozen C2 oracle

Tuple order: apparent_age, response_delay, corrected_age_value, corrected_initial_age, resident_time, current_age. Computed manually from the input, independently of candidate code or oracle evaluation.

|Case|Calculation|Six-value tuple|
|---|---|---|
|1|100-100=0; 100-100=0; 0+0=0; max(0,0)=0; 100-100=0; 0+0=0|(0,0,0,0,0,0)|
|2|100-90=10; delay=0; corrected=0; max(10,0)=10; resident=0|(10,0,0,10,0,10)|
|3|100-110=-10 clamped to 0; all other terms zero|(0,0,0,0,0,0)|
|4|100-100=0; 100-90=10; 20+10=30; max=30; resident=0|(0,10,30,30,0,30)|
|5|100-80=20; 100-90=10; 5+10=15; max=20; 130-100=30; 20+30=50|(20,10,15,20,30,50)|
|6|100-100=0; 100-95=5; 5+5=10; max=10; 140-100=40; 10+40=50|(0,5,10,10,40,50)|
|7|1-0=1; 1-0=1; 0+1=1; max=1; 3-1=2; 1+2=3|(1,1,1,1,2,3)|
|8|10-10=0; delay=0; 100+0=100; max=100; resident=0|(0,0,100,100,0,100)|
|9|60-50=10; 60-45=15; 0+15=15; max=15; 75-60=15; 15+15=30|(10,15,15,15,15,30)|
|10|60-60=0; 60-45=15; 0+15=15; max=15; 75-60=15; 15+15=30|(0,15,15,15,15,30)|
|11|apparent=delay=0; corrected=2147483648; max=2147483648; resident=2147483648; sum=4294967296|(0,0,2147483648,2147483648,2147483648,4294967296)|
|12|0-(-20)=20; delay=0; corrected=0; max=20; resident=10; sum=30|(20,0,0,20,10,30)|

All twelve complete frozen output objects match these tuples exactly.

Invalids: 13 request=2 > response=1; 14 response=2 > now=1; 15 Age=-1; 16 date=false (JSON boolean is not an integer despite Python bool inheriting int); 17 missing required date_value. All five expected exit1 outcomes match the frozen contract. Negative Date in case12 is intentionally valid; local times and Age remain nonnegative.

Coverage gap, not oracle defect: none of the twelve valid frozen inputs omits age_value, so the frozen finite counter alone cannot demonstrate default0. Invalid cases 13,14,16,17 omit Age but are invalid for unrelated reasons. Fresh candidate assertions must cover valid omitted Age and missing/null/noninteger Date separately.
