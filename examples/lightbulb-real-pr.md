# Real PR: a Copilot change that was reverted eight months later

This is a real pull request, reviewed after the fact. The two other walkthroughs in this folder are invented; this one is not.

| | |
|---|---|
| Repository | [Tyrrrz/LightBulb](https://github.com/Tyrrrz/LightBulb), a Windows app that adjusts screen gamma, about 2.8k stars |
| PR | [#413](https://github.com/Tyrrrz/LightBulb/pull/413) "Unload UI when hidden to tray to reduce passive CPU/RAM usage" |
| Author | GitHub Copilot coding agent |
| Merged | 2026-03-02, after dozens of review rounds, with a clean build and codecov reporting every changed line covered |
| Bug report | [#467](https://github.com/Tyrrrz/LightBulb/issues/467), 2026-10-21: the Settings button stays disabled if you minimize while Settings is open |
| Revert | [#474](https://github.com/Tyrrrz/LightBulb/pull/474), 2026-11-06: "It didn't reduce resource usage much and complicated window and state management." |

## How the review was run

Step 1 went to a sub-agent with a clean context. It received three things only:

- the diff of #413,
- the repository checked out at the PR's base commit (`612bccde`),
- one sentence of intent: close the main window instead of hiding it when the app goes to tray, to cut idle CPU and RAM, while the gamma logic and tray icon keep running.

It was not told that the PR was later reverted. It had no network access and no later history.

## Step 1: bugs

What the fresh-context reviewer reported, with its own labels:

- **[PLAUSIBLE] Closing the window while a dialog is open leaves the dialog awaiting forever.** The Hide button now calls `Close()`, which destroys the dialog host. The awaited dialog never completes, so the dialog lock is never released.
  This is bug #467. `ShowSettingsAsync` is an async `[RelayCommand]` (`MainViewModel.cs`, lines 169-171 at the base commit), so the Settings button stays disabled while that await hangs. Not reproduced here: there was no Windows machine to run the app.
- **[CONFIRMED by reading] `--start-hidden` skips the main view model's initialization.** The hidden path only initializes the dashboard. The update check timer, pending-update finalization and the first-run dialog never run until the user opens the window.
- **[PLAUSIBLE] The window is shown before theme and settings load**, which can flash the default theme for one frame.
- **[CONFIRMED by reading] `_isInitialized` is set before the awaits**, so an interrupted initialization never retries.

## Step 2: context

- **Requirement match.** Issue [#328](https://github.com/Tyrrrz/LightBulb/issues/328) asked to reduce passive CPU and RAM. Nothing in the PR or its comments measures either; the comments are coverage reports and formatting fixes. The reviewer also flagged this: "no evidence of reduced CPU/RAM; measure working set and idle CPU before and after."
  This is the reason the maintainer gave for the revert.
- **Neighbors.** The Settings bug lives in the dialog code, which the diff does not touch. Reading the diff line by line would not show it.

## Step 3: sign-off

An honest approval comment for #413 would have read: *"Verified the build and coverage. Did not measure CPU or RAM, did not run the hidden-start path, did not test closing the window with a dialog open."* Those three gaps are what shipped.

## What this case does and does not show

- It shows that both problems behind the revert were findable before merge, from the diff, the base code and the intent.
- It does not show a detection rate. This PR was picked because it was already known to be reverted. The main bug finding was flagged as plausible, not reproduced.
