# leela_lite

Very simple PUCT to experiment with leela networks in Python.

## New UCI

LeelaLite now has a very lightweight uci interface. The `leelalite.sh` shell script is a wrapper around
`engine.py`. The engine ignores arguments to `go`, except the `nodes` parameter, in which case it will
search the specified number of nodes. It just runs a search at whatever nodes were specified as an
argument to the python script.

You'll have to change the paths in `leelalite.sh` to reflect your installation. See the next section
for installation instructions.

Also, there's a LRU nn eval cache (thanks @Trevor) and lazy instantiation that make leela_lite run a
whole lot faster.

## NN Network Server

TBD

## Quickstart

- make sure you have at least python 3.6 installed
- setup a python virtual environment with python3.6+, for example: `virtualenv -p python3.6 ~/envs/lcztools`
- load your virtual environment: `. ~/envs/lcztools/bin/activate`
- install pytorch: `pip install torch torchvision`
- git clone the repo `https://github.com/so-much-meta/lczero_tools.git` and checkout the tag `0.1.0`
- change dirs to the repo and install so you can edit `pip install -e .`
- run leela_lite with weights file and number of nodes: `python leela_lite.py weights_9149.txt.gz 200` (for example)

Leela Lite will play a game against itself and spit out the pgn:

```
Turn: White
thinking...
best:  c4c3
. . . . . . . .
. . . . . P . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . K . . . . .
. . . . Q . . .
. . k . . . . .
Turn: Black
thinking...
best:  c1b1
. . . . . . . .
. . . . . P . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . K . . . . .
. . . . Q . . .
. k . . . . . .
Turn: White
thinking...
best:  e2b2
Game over... result is 1-0
. . . . . . . .
. . . . . P . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . K . . . . .
. Q . . . . . .
. k . . . . . .
Turn: Black
[Event "?"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "1-0"]

1. d4 d5 2. c4 e6 3. Nc3 Nf6 4. Nf3 dxc4 5. e3 a6 6. a4 c5 7. Bxc4 Nc6
8. O-O Be7 9. dxc5 Qxd1 10. Rxd1 Bxc5 11. Bf1 Ke7 12. Bd2 Rd8 13. Rac1 Bb4
14. Be1 Rxd1 15. Rxd1 Bd7 16. Na2 Bxe1 17. Rxe1 Rc8 18. Rc1 Nd5
19. Nd2 Ne5 20. Rxc8 Bxc8 21. e4 Nb6 22. f4 Ng6 23. a5 Na4 24. b3 Nc5
25. g3 Bd7 26. Kf2 Bc6 27. Ke3 e5 28. f5 Nf8 29. Nb4 Kd6 30. Nc4+ Kc7
31. Nxc6 bxc6 32. Nxe5 f6 33. b4 fxe5 34. bxc5 Nd7 35. Bxa6 Nxc5 36. Be2 Nb3
37. a6 Nd4 38. Bc4 Kb6 39. g4 Nc2+ 40. Kd2 Nd4 41. h4 Nf3+ 42. Ke2 Nxh4
43. g5 h6 44. gxh6 gxh6 45. f6 Ng6 46. Kf3 h5 47. f7 Nf8 48. Kg3 Ka7
49. Kh4 Kb6 50. Kxh5 Ka7 51. Kh6 Kb6 52. Kg7 Nd7 53. Be6 Kxa6 54. Bxd7 c5
55. Kf6 c4 56. Kxe5 c3 57. Ba4 Ka5 58. Bc2 Kb4 59. Kd5 Ka3 60. Kc4 Kb2
61. Ba4 c2 62. Bxc2 Kxc2 63. e5 Kd2 64. e6 Ke2 65. e7 Kd2 66. e8=Q Kc2
67. Qe2+ Kc1 68. Kc3 Kb1 69. Qb2# 1-0
```

## What it needs

- [x] Non hacky clone of LeelaBoard so it doesn't run so darn slow
- [X] UCI interface
- [ ] Noise for variety
- TBD
