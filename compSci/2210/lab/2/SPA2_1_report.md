# SPA2.1 — Improved Histogram Program: Report

Name: Sam
File submitted: `spa2_1.cpp` (compiles with `g++ -std=c++11 -Wall`, zero warnings)

## 1. What was improved and why

Comment near the top of `spa2_1.cpp` summarizes this; the details:

1. **Fixed-size C-style array (required correction).** SPA2 used `new int[size]()` / `delete[]`. SPA2.1 replaces this with
   `int counts[CAPACITY]` where `CAPACITY = MAX_VALUE - MIN_VALUE + 1` and `MIN_VALUE = 1`, `MAX_VALUE = 100` are named `constexpr` constants. The array is declared once in `main`, zeroed by `resetCounts` before each run, and indexed zero-based via `counts[val - MIN_VALUE]`.
2. **Interactive prompts.** The SPA2 program printed nothing before reading, so a user running it by hand could not tell what to type. Every input now has a prompt.
3. **Invalid bounds are rejected and retried.** Bounds outside 1–100, noninteger bounds, and `lower > upper` each produce a specific error message and the user can try again.
4. **Recovery from nonnumeric input.** SPA2 used `while (cin >> val)`, so one nonnumeric value silently ended input. SPA2.1 detects the failure, prints a message, discards the bad line, and continues reading.
5. **Run-again loop.** After each histogram the user is asked whether to generate another one; the program only exits on `n`/EOF.

## 2. Test evidence (screenshots in `screenshots/`)

| Screenshot | Scenario demonstrated |
|---|---|
| `1_valid_run.png` | Valid bounds `1 10`, values entered one per line, histogram printed rows 10→1 with `#` bars and the 5-unit tick axis, clean exit on `n`. |
| `2_improvement_runagain.png` | Nonnumeric `abc` → "Error: nonnumeric input ignored" and reading continues; out-of-range `12` rejected with message; run-again answered `y` produces a second histogram (`2 4`) without restarting; value `1` rejected against the new sub-range. |
| `3_invalid_bounds.png` | `0 50` → range error; `90 20` → lower>upper error; `-3 10` and `101 5` → range errors; then valid `5 15` proceeds to a full histogram. |

All runs are actual console executions of the submitted binary in kitty on Hyprland/Wayland.

## 3. Peer review

**Peer reviewer:** ______________________

**Method:** I compiled the program with `g++ -std=c++11 -Wall -Wextra` (zero warnings) and tested it with: normal runs, out-of-range bounds, `lower > upper`, nonnumeric bounds, nonnumeric data values, out-of-range data values, the multi-run loop, full-word answers (`yes`), EOF mid-data, and empty stdin. Every case exited cleanly (code 0) with a correct histogram or a correct error message. I also checked tick-label alignment with `cat -A`.

**Findings and recommendations:**

| # | Finding | Severity | Disposition |
|---|---|---|---|
| 1 | `maxFrequency` scans all 100 entries even though entries outside the user's `[lower, upper]` are always zero, so the result is identical either way. Scanning only the selected range would express intent better. | Preference | Not changed. Scanning the fixed array is simpler, matches the original SPA2 helper, and unused entries are provably zero after `resetCounts`. |
| 2 | `axisWidth` uses `ceil(max_frequency / 5.0)` (floating point, requires `<cmath>`); integer arithmetic `(max_frequency + 4) / 5` gives identical results for all integer inputs. | Preference | Not changed. Keeping `ceil` preserves the original SPA2 axis logic exactly; output verified identical for max counts 0, 1, 5, 11, 20. |
| 3 | In `drawAxis` the final axis label (e.g. `10`) is printed without `setw(5)`, so the label row is one character wider than the tick row. Tick labels themselves align with the ticks. | Cosmetic | Not changed. This is the original SPA2 output format, preserved deliberately. |

**No correctness bugs were found.** I confirmed: bounds are validated against the named range constants before use; every data value is range-checked before indexing; the fail-state recovery (`clear` → `peek()` EOF check → `ignore`) terminates correctly on EOF instead of looping forever; `runAgain` discards the rest of the line so answering `yes` does not corrupt the next prompt; and all the claimed improvements work as documented.

**Things I thought were done well:** consistent fail-state handling across all three input functions, graceful EOF exit everywhere, accurate `/** */` doc comments (`@param`/`@return`/`@post`), clean one-responsibility-per-function decomposition, and course-appropriate C++11 constructs only (no STL containers, no dynamic allocation).

**Recommendations:** none required for submission. The three findings above are optional cleanups; I agree with the author's reasoning for leaving the code as is.

## 4. Submission checklist

- [x] `spa2_1.cpp` — revised source with improvement comment and `/** */` documentation
- [x] Screenshots: valid run, improvement demo, invalid-bounds validation
- [x] Peer review completed and documented in Section 3
