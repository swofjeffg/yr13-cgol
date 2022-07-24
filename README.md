# Level 3 Computer Science GUI Project
Project for YR13 computer science where I replicate Conway's game of life.

## Seed formatting
The seed format requires a bit of explanation to understand how it fully works

Say we have a 4x4 grid;
```
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 0, 0, 0]
```

And I want just the inner 2x2 grid to be on;
```
[0, 0, 0, 0]
[0, 1, 1, 0]
[0, 1, 1, 0]
[0, 0, 0, 0]
```

The seed would be;
```
2-2:12-3:13-2:13-3:1
```

To break it down, '22:1' means that column 2, row 2, is in state 1 (on), '23:1' column 3, row 2, is in state 1 and so on...
Off tiles do not have to be declared, as the assumed state is off

## Version checklist (progress tracker)
### v0.00
- [ ] Created a working and reliable game engine
- [ ] Created a save function, with seed readability

### v0.10
- [ ] Created basic skeleton GUI
- [ ] Easy to generate/enter seeds
- [ ] Basic grid displaying CGOL (Conway's game of life)