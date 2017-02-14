# halint
a linting tool for Halite game replays

I wrote this [linter](https://en.wikipedia.org/wiki/Lint_(software)) to speed and enhance analysis of Halint game replays.  I know this would have been more useful released earlier; that's why I'm releasing it now ;)   Still thought it might be useful to people analyzing post-mortems of game results during the "finals" and will definitely be useful to anyone continuing to develop a Halite bot.  

There are two files: `halint.py` is the linter, and `halint-get` is a bash script that auto-downloads (using curl, into your current working directory) a specified replay from the Halite website, and then runs `halint.py` on it.  Incidentally, `halint.py` will accept any number of filenames on the command line, so something like  `./halint.py 445689*.hlt` is perfectly valid.

## requirements

python3 with package [tabulate](https://pypi.python.org/pypi/tabulate)

curl (required by halint-get, but not needed for running `halint.py` strictly locally)


## usage

Right-click on the game replay icon from your game feed on the Halite site, and select `copy link location`.

At a command line, `./halint-get <paste link you just copied here>`  The bash script translates the links provided by the Halite site into a curl call to pull the replay file directly from the AWS bucket (and drops it in your current working directory).  It then calls `./halint.py <replay-just-downloaded>.hlt`

If you created a replay locally or already have it downloaded, you can just `./halint.py ar1487044012-1781075238.hlt`
Halint accepts both gzipped and plaintext `.hlt` replay files.

```
travis@F555L ~ $ ./halint.py --help
usage: halint.py [-h] [--names [NAMES]] [--show_caploss_from_production]
                 [--show_overkill] [--show_flip_flops]
                 filenames [filenames ...]

positional arguments:
  filenames

optional arguments:
  -h, --help            show this help message and exit
  --names [NAMES]       Restrict lint output to these named bots.
  --show_caploss_from_production
                        Shows caploss which occured solely due to production.
  --show_overkill       Show detailed overkill frame-by-frame.
  --show_flip_flops     Show pieces that flip-flop between adjacent squares.
```

## sample output

Halint produces a lot of output (usually).  Some of it is useful, up to you to decide which is which.  The most verbose items are disabled by default, but can be enabled with the command line flags above.  Use the `--names` command line arg to limit the frame-by-frame output to just the bot(s) you care about.


```
travis@F555L ~ $ ./halint-get https://halite.io/game.php?replay=ar1487044012-1781075238.hlt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  105k  100  105k    0     0   119k      0 --:--:-- --:--:-- --:--:--  118k
Starting halint for ar1487044012-1781075238.hlt
Frame  30:     mzotkiew v34:               Cap loss at (14, 7):   2
Frame  44:       erdman v26:  Failed mining attempt at ( 6,16)
Frame  49:       erdman v26:  Failed mining attempt at ( 6,23)
Frame  52:   PeppiKokki v11:  Failed mining attempt at (15,10)
Frame  56:       erdman v26:  Failed mining attempt at ( 6,27)
Frame  58:       erdman v26:  Failed mining attempt at ( 4,19)
Frame  61:       erdman v26:  Failed mining attempt at ( 5,24)
Frame  65:   PeppiKokki v11:               Cap loss at (14,10):  11
Frame  65:     mzotkiew v34:               Cap loss at ( 8, 8):  14
Frame  66:       erdman v26:  Failed mining attempt at ( 1,19)
Frame  68:       erdman v26:  Failed mining attempt at (17, 7)
Frame  68:       erdman v26:  Failed mining attempt at (19,19)
Frame  68:       erdman v26:  Failed mining attempt at ( 5, 2)
Frame  68:       erdman v26:  Failed mining attempt at (17,28)
Frame  73:       erdman v26:  Failed mining attempt at (22,19)
Frame  80:       erdman v26:  Failed mining attempt at (24,18)
Frame  82:       erdman v26:  Failed mining attempt at (25,17)
Frame  83:       erdman v26:  Failed mining attempt at (29,25)
Frame  86:       erdman v26:  Failed mining attempt at ( 0,20)
Frame  89:       erdman v26:  Failed mining attempt at (29,22)
Frame  91:       erdman v26:  Failed mining attempt at (29,16)
Frame  91:       erdman v26:  Failed mining attempt at (25,24)
Frame  92:       erdman v26:  Failed mining attempt at (29,23)
Frame  94:       erdman v26:  Failed mining attempt at (25,25)
Frame  95:   PeppiKokki v11:               Cap loss at ( 9,11):   5
Frame  95:   PeppiKokki v11:  Failed mining attempt at ( 8,10)
Frame  96:       erdman v26:  Failed mining attempt at (28,14)
Frame  96:       erdman v26:  Failed mining attempt at (28,26)
Frame  98:       erdman v26:  Failed mining attempt at (25,16)
Frame  99:       erdman v26:               Cap loss at (11,22):  11
Frame 106:   PeppiKokki v11:               Cap loss at ( 9,11):   9
Frame 106:       erdman v26:  Failed mining attempt at (26, 8)
Frame 107:       erdman v26:  Failed mining attempt at (29,11)
Frame 111:       erdman v26:  Failed mining attempt at (26, 6)
Frame 111:       erdman v26:  Failed mining attempt at (28,10)
Frame 112:       erdman v26:  Failed mining attempt at (29,27)
Frame 114:       erdman v26:  Failed mining attempt at (29, 7)
Frame 119:       erdman v26:  Failed mining attempt at ( 3,12)
Frame 120:       erdman v26:               Cap loss at (12,27):  50
Frame 120:       erdman v26:  Failed mining attempt at (27,28)
Frame 120:       erdman v26:  Failed mining attempt at ( 1,16)
Frame 123:       erdman v26:  Failed mining attempt at (28,22)
Frame 125:       erdman v26:  Failed mining attempt at (20,13)
Frame 127:       erdman v26:  Failed mining attempt at (22,17)
Frame 127:       erdman v26:  Failed mining attempt at (23,12)
Frame 128:       erdman v26:               Cap loss at ( 8, 0):  53
Frame 128:       erdman v26:               Cap loss at (13,29):  27
Frame 128:       erdman v26:  Failed mining attempt at (24,16)
Frame 130:       erdman v26:  Failed mining attempt at ( 1,28)
Frame 131:       erdman v26:  Failed mining attempt at ( 7, 0)
Frame 131:       erdman v26:  Failed mining attempt at (23,14)
Frame 133:       erdman v26:  Failed mining attempt at (24,28)
Frame 134:       erdman v26:  Failed mining attempt at (23,23)
Frame 134:       erdman v26:  Failed mining attempt at ( 2, 2)
Frame 138:       erdman v26:  Failed mining attempt at (22,27)
Frame 139:       erdman v26:               Cap loss at (17,14):   3
Frame 139:       erdman v26:  Failed mining attempt at (24,22)
Frame 139:       erdman v26:  Failed mining attempt at (24,27)
Frame 140:       erdman v26:  Failed mining attempt at (22, 1)
Frame 140:       erdman v26:  Failed mining attempt at (23,16)
Frame 140:       erdman v26:  Failed mining attempt at (22,28)
Frame 142:       erdman v26:  Failed mining attempt at (23,28)
Frame 143:       erdman v26:  Failed mining attempt at (23,11)
Frame 144:       erdman v26:               Cap loss at ( 6,14): 164
Frame 144:       erdman v26:  Failed mining attempt at (23,29)
Frame 145:       erdman v26:               Cap loss at ( 9, 5):  96
Frame 145:       erdman v26:               Cap loss at ( 6,16):  61
Frame 145:       erdman v26:               Cap loss at (13, 4):   4
Frame 145:       erdman v26:               Cap loss at ( 9,14):  41
Frame 145:       erdman v26:  Failed mining attempt at (22,11)
Frame 145:       erdman v26:  Failed mining attempt at (23,22)
Frame 146:       erdman v26:               Cap loss at ( 8,15): 174
Frame 147:       erdman v26:  Failed mining attempt at (21, 0)
Frame 148:       erdman v26:  Failed mining attempt at ( 1,22)
Frame 149:       erdman v26:               Cap loss at ( 7,11):   2
Frame 149:       erdman v26:  Failed mining attempt at (21,11)
Frame 150:       erdman v26:               Cap loss at (12,10):  84
Frame 150:       erdman v26:               Cap loss at ( 9, 9): 134
Frame 150:       erdman v26:               Cap loss at (10,10): 111

+------------------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| Caploss                |   mzotkiew v34 |   PeppiKokki v11 |   erdman v26 |   nmalaguti v62 |   DexGroves v47 |   TOTAL |
+========================+================+==================+==============+=================+=================+=========+
| Standard               |             16 |               25 |         1015 |               0 |               0 |    1056 |
+------------------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| Merge ex Production    |              3 |               15 |          963 |             226 |               0 |    1207 |
+------------------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| StillBig ex Production |              3 |               44 |           22 |             359 |               0 |     428 |
+------------------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| TOTAL                  |             22 |               84 |         2000 |             585 |               0 |    2691 |
+------------------------+----------------+------------------+--------------+-----------------+-----------------+---------+

+----------------+------------------------+---------------+----------------------+
|                |   Prod cost from moves |   Total moves |   Prod cost per move |
+================+========================+===============+======================+
| mzotkiew v34   |                   4274 |           659 |                6.486 |
+----------------+------------------------+---------------+----------------------+
| PeppiKokki v11 |                   7656 |          1155 |                6.629 |
+----------------+------------------------+---------------+----------------------+
| erdman v26     |                  52650 |          9038 |                5.825 |
+----------------+------------------------+---------------+----------------------+
| nmalaguti v62  |                  15563 |          2657 |                5.857 |
+----------------+------------------------+---------------+----------------------+
| DexGroves v47  |                   1914 |           294 |                6.510 |
+----------------+------------------------+---------------+----------------------+

+----------------+---------+---------+---------+---------+---------+
| Move %         |   1 / 5 |   2 / 5 |   3 / 5 |   4 / 5 |   5 / 5 |
+================+=========+=========+=========+=========+=========+
| mzotkiew v34   |   0.208 |   0.262 |   0.290 |   0.500 |   0.000 |
+----------------+---------+---------+---------+---------+---------+
| PeppiKokki v11 |   0.299 |   0.322 |   0.336 |   0.341 |   0.304 |
+----------------+---------+---------+---------+---------+---------+
| erdman v26     |   0.228 |   0.281 |   0.254 |   0.259 |   0.287 |
+----------------+---------+---------+---------+---------+---------+
| nmalaguti v62  |   0.186 |   0.246 |   0.293 |   0.278 |   0.247 |
+----------------+---------+---------+---------+---------+---------+
| DexGroves v47  |   0.230 |   0.240 |   0.306 |   0.000 |   0.000 |
+----------------+---------+---------+---------+---------+---------+

Cumulative overkill
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| from / to      |   mzotkiew v34 |   PeppiKokki v11 |   erdman v26 |   nmalaguti v62 |   DexGroves v47 |   TOTAL |
+================+================+==================+==============+=================+=================+=========+
| mzotkiew v34   |              0 |               95 |            5 |             238 |               0 |     338 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| PeppiKokki v11 |            168 |                0 |            0 |             248 |               0 |     416 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| erdman v26     |              0 |               32 |            0 |            1486 |               0 |    1518 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| nmalaguti v62  |             22 |               89 |          849 |               0 |             552 |    1512 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| DexGroves v47  |              0 |                0 |            0 |             255 |               0 |     255 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
| TOTAL          |            190 |              216 |          854 |            2227 |             552 |    4039 |
+----------------+----------------+------------------+--------------+-----------------+-----------------+---------+
Replay may be available at https://halite.io/game.php?replay=ar1487044012-1781075238.hlt
Completed halint for ar1487044012-1781075238.hlt

```


