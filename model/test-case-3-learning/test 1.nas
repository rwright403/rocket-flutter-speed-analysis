INIT MASTER(S)
NASTRAN OP2NEW=0,SYSTEM(319)=1
ID Test,FEMAP
SOL SEFLUTTR
TIME 30
CEND
  TITLE = MSC Nastran Flutter Analysis Set
  ECHO = NONE
  DISPLACEMENT(PLOT) = ALL
  SPCFORCE(PLOT) = ALL
  STRESS(PLOT,CORNER) = ALL
  AEROF = All
  SPC = 1
  METHOD = 1
BEGIN BULK
$ ***************************************************************************
$   Written by : Femap
$   Version    : 2412.0
$   Translator : MSC Nastran
$   From Model : C:\Users\lord flashheart\Desktop\Test case 3 V1.modfem
$   Date       : Sat Mar 22 15:48:59 2025
$   Output To  : C:\Users\lord flashheart\Desktop\
$ ***************************************************************************
$
PARAM,PRGPST,NO
PARAM,POST,-1
PARAM,OGEOM,NO
PARAM,AUTOSPC,YES
PARAM,GRDPNT,0
CORD2C         1       0      0.      0.      0.      0.      0.      1.+FEMAPC1
+FEMAPC1      1.      0.      1.        
CORD2S         2       0      0.      0.      0.      0.      0.      1.+FEMAPC2
+FEMAPC2      1.      0.      1.        
AERO           0      0.      0.      0.       0       0                
EIGRL          1            400.      10       0                    MASS
PARAM,LMODES,20
PARAM,HFREQ,400.
$ Femap Constraint Set 1 : fixed
SPC1           1  123456       1
SPC1           1  123456       2
SPC1           1  123456       3
SPC1           1  123456       4
SPC1           1  123456       5
SPC1           1  123456       6
SPC1           1  123456       7
SPC1           1  123456       8
$ Femap Property 1 : 1
PSHELL         1       1    .002                                      0.
$ Femap Material 1 : ISOTROPIC Material
MAT1           1  4.5+10  1.7+10     .35   1800.      0.      0.    .001+       
+          2.5+8   1.6+8 9.999+9
GRID           1       0      0.      0.      0.       0
GRID           2       0.0289286      0.      0.       0
GRID           3       0.0578571      0.      0.       0
GRID           4       0.0867857      0.      0.       0
GRID           5       0.1157143      0.      0.       0
GRID           6       0.1446429      0.      0.       0
GRID           7       0.1735714      0.      0.       0
GRID           8       0   .2025      0.      0.       0
GRID           9       0   .2025      0.   .0275       0
GRID          10       0   .2025      0.    .055       0
GRID          11       0   .2025      0.   .0825       0
GRID          12       0   .2025      0.     .11       0
GRID          13       0   .2025      0.   .1375       0
GRID          14       0   .2025      0.    .165       0
GRID          15       0.1842857      0.    .165       0
GRID          16       0.1660714      0.    .165       0
GRID          17       0.1478571      0.    .165       0
GRID          18       0.1296429      0.    .165       0
GRID          19       0.1114286      0.    .165       0
GRID          20       0.0932143      0.    .165       0
GRID          21       0    .075      0.    .165       0
GRID          22       0   .0625      0.   .1375       0
GRID          23       0     .05      0.     .11       0
GRID          24       0   .0375      0.   .0825       0
GRID          25       0    .025      0.    .055       0
GRID          26       0   .0125      0.   .0275       0
GRID          27       0.0396429      0.   .0275       0
GRID          28       0.0667857      0.   .0275       0
GRID          29       0.0939286      0.   .0275       0
GRID          30       0.1210714      0.   .0275       0
GRID          31       0.1482143      0.   .0275       0
GRID          32       0.1753571      0.   .0275       0
GRID          33       0.0503571      0.    .055       0
GRID          34       0.0757143      0.    .055       0
GRID          35       0.1010714      0.    .055       0
GRID          36       0.1264286      0.    .055       0
GRID          37       0.1517857      0.    .055       0
GRID          38       0.1771429      0.    .055       0
GRID          39       0.0610714      0.   .0825       0
GRID          40       0.0846429      0.   .0825       0
GRID          41       0.1082143      0.   .0825       0
GRID          42       0.1317857      0.   .0825       0
GRID          43       0.1553571      0.   .0825       0
GRID          44       0.1789286      0.   .0825       0
GRID          45       0.0717857      0.     .11       0
GRID          46       0.0935714      0.     .11       0
GRID          47       0.1153571      0.     .11       0
GRID          48       0.1371429      0.     .11       0
GRID          49       0.1589286      0.     .11       0
GRID          50       0.1807143      0.     .11       0
GRID          51       0   .0825      0.   .1375       0
GRID          52       0   .1025      0.   .1375       0
GRID          53       0   .1225      0.   .1375       0
GRID          54       0   .1425      0.   .1375       0
GRID          55       0   .1625      0.   .1375       0
GRID          56       0   .1825      0.   .1375       0
CQUAD4         1       1       1       2      27      26                
CQUAD4         2       1       2       3      28      27                
CQUAD4         3       1       3       4      29      28                
CQUAD4         4       1       4       5      30      29                
CQUAD4         5       1       5       6      31      30                
CQUAD4         6       1       6       7      32      31                
CQUAD4         7       1       7       8       9      32                
CQUAD4         8       1      26      27      33      25                
CQUAD4         9       1      27      28      34      33                
CQUAD4        10       1      28      29      35      34                
CQUAD4        11       1      29      30      36      35                
CQUAD4        12       1      30      31      37      36                
CQUAD4        13       1      31      32      38      37                
CQUAD4        14       1      32       9      10      38                
CQUAD4        15       1      25      33      39      24                
CQUAD4        16       1      33      34      40      39                
CQUAD4        17       1      34      35      41      40                
CQUAD4        18       1      35      36      42      41                
CQUAD4        19       1      36      37      43      42                
CQUAD4        20       1      37      38      44      43                
CQUAD4        21       1      38      10      11      44                
CQUAD4        22       1      24      39      45      23                
CQUAD4        23       1      39      40      46      45                
CQUAD4        24       1      40      41      47      46                
CQUAD4        25       1      41      42      48      47                
CQUAD4        26       1      42      43      49      48                
CQUAD4        27       1      43      44      50      49                
CQUAD4        28       1      44      11      12      50                
CQUAD4        29       1      23      45      51      22                
CQUAD4        30       1      45      46      52      51                
CQUAD4        31       1      46      47      53      52                
CQUAD4        32       1      47      48      54      53                
CQUAD4        33       1      48      49      55      54                
CQUAD4        34       1      49      50      56      55                
CQUAD4        35       1      50      12      13      56                
CQUAD4        36       1      22      51      20      21                
CQUAD4        37       1      51      52      19      20                
CQUAD4        38       1      52      53      18      19                
CQUAD4        39       1      53      54      17      18                
CQUAD4        40       1      54      55      16      17                
CQUAD4        41       1      55      56      15      16                
CQUAD4        42       1      56      13      14      15                
$ Femap Aero Property 1 : Aero Property
PAERO1         1                                                        
$ Femap Aero Panel 1 : Aero Panel
CAERO1         1       1       0       2       2                       1+       
+             0.      0.      0.   .2025    .075      0.    .165   .1275
$ Femap Aero Spline 1 : Aero Spline
SPLINE1        1       1       1       4       1      0.     IPS    BOTH
ENDDATA
