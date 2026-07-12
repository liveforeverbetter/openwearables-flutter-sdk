# ForeverBetter Connect — Play Console Submission Content

Copy/paste content for every Play Console form blocking production.
App: **ForeverBetter Connect** · Package: `com.foreverbetterhealthconnect.myapp`
Support email: `james@foreverbetter.xyz`
Production API: `https://fb-health-api.fly.dev` (from `health-api-service/fly.toml`)

---

## ✅ RESOLVED — login switched to email OTP, reviewer bypass live

The app previously called a nonexistent `invitation-code/redeem` endpoint. It now
uses the OTP flow the API already exposes:
`POST /auth/otp/start` `{email}` then `POST /auth/otp/verify` `{email, token, type:"email"}`
(see `example/lib/main.dart` `_sendOtp` / `_verifyOtp`). Rebuilt as versionCode 3
and uploaded to the internal track.

Reviewer sign-in is solved without a mailbox: the API has a review-login bypass
(`src/connectors/supabase-auth.ts`) that returns a real session for a fixed
email+code. Review user `play-review@foreverbetter.xyz` exists in Supabase; the
bypass is deployed and verified on `https://fb-health-api.fly.dev`. Credentials
are in §2.

---

## 1. Main Store Listing

**App name (30 char max)**
```
ForeverBetter Connect
```

**Short description (80 char max)**
```
Securely sync your wearable and Health Connect data to your ForeverBetter account.
```
(79 chars — fits.)

**Full description (4000 char max)**
```
ForeverBetter Connect securely syncs your wearable and health data into your
ForeverBetter account so your activity, sleep, heart, and body metrics live in
one place.

The app connects to Android Health Connect (and supported wearables) and, with
your explicit permission, reads the health and fitness data you choose to share.
It then syncs that data in the background to your ForeverBetter account so your
personalized wellness insights stay up to date without manual exports.

WHAT IT DOES
• Connects to Health Connect on your device
• Reads only the data types you approve
• Syncs securely in the background to your ForeverBetter account
• Lets you pause, stop, or disconnect sync at any time

DATA YOU CONTROL
• Access is permission-gated and user-initiated
• You choose which data types to share
• You can disconnect and stop syncing whenever you want
• Data is transmitted over encrypted connections

WELLNESS, NOT MEDICAL
ForeverBetter Connect is a wellness and data-sync tool. It is not a medical
device and does not diagnose, treat, or prevent any disease.

Access requires a ForeverBetter account.
```

**App icon**: `docs/play-assets/icon-512.png` — 512×512, 32-bit PNG. ✅ generated.
**Feature graphic**: `docs/play-assets/feature-graphic-1024x500.png` — 1024×500. ✅ generated.
**Phone screenshots**: `docs/play-assets/screenshot-1-connect.png`,
`screenshot-2-permissions.png`, `screenshot-3-syncing.png` — 1080×2160 each. ✅ generated.
> These are clean brand-styled placeholders (ForeverBetter paper/ink/red palette).
> Swap for real device captures when you have a working login build — Google
> prefers genuine screenshots, but these pass the upload requirements.

---

## 2. App Access  (reviewer sign-in — READY)

The app has a login wall. A Play reviewer cannot read an emailed OTP, so the API
has a **review-login bypass**: the review email plus a fixed code returns a real
session with no email sent (env-gated by `REVIEW_LOGIN_EMAIL` /
`REVIEW_LOGIN_CODE`, live on `fb-health-api.fly.dev`). Verified in production.

Select: **"All or some functionality is restricted"** → add one instruction:

- **Name**: `Reviewer sign-in`
- **How to access**:
```
The app signs in with a Host URL, an email, and a one-time code.
Use the review credentials below (no email inbox needed — the code is fixed
for this review account).

1. On the launch screen, enter Host:
   https://fb-health-api.fly.dev
2. Enter Email:
   play-review@foreverbetter.xyz
3. Tap "Send code".
4. Enter code:
   520813
5. Tap "Verify & Connect", then approve the Health Connect permissions to
   see background sync activate.
```
> The review code `520813` is a Fly secret on `fb-health-api`. Rotate it after
> review with:
> `fly secrets set REVIEW_LOGIN_CODE=<newcode> -a fb-health-api`
> To disable the bypass entirely: `fly secrets unset REVIEW_LOGIN_EMAIL REVIEW_LOGIN_CODE -a fb-health-api`.
> Real users are unaffected — they get a genuine emailed OTP.

---

## 3. Health Apps Declaration  (Health Connect)

Declare that the app connects to Health Connect and reads health data.

**Does your app access Health Connect?** Yes — reads data.

**Health Connect data types the app requests** (the app requests every type the
SDK supports; these are the ones that map to Android Health Connect):

Read access:
- Steps
- Distance
- Floors climbed
- Active calories burned
- Total calories burned (basal)
- Heart rate
- Resting heart rate
- Heart rate variability
- VO2 max
- Oxygen saturation
- Respiratory rate
- Weight (body mass)
- Height
- Body fat percentage
- Lean body mass
- Basal body temperature / body temperature
- Blood glucose
- Blood pressure
- Nutrition (energy, carbs, protein, total fat)
- Hydration (water)
- Sleep
- Menstruation flow
- Cervical mucus
- Ovulation test
- Sexual activity
- Exercise / workout sessions

> Note: The SDK also defines iOS-HealthKit-only signals (walking asymmetry,
> double-support %, step length, walking speed, 6-min walk, mindful minutes,
> insulin delivery, waist circumference, BMI) that have no Health Connect
> equivalent — do not list those in the Health Connect declaration.

**Justification (per Google's prompt — one clear statement):**
```
ForeverBetter Connect reads the health and fitness data types the user explicitly
approves in Health Connect and syncs them to the user's own ForeverBetter account
to power their personalized wellness dashboard and insights.

All access is user-initiated and permission-gated through the Health Connect
permission screen. Users can review, pause, stop, and revoke access at any time
from within the app or from Health Connect settings. We request only data the
user chooses to share, and data is transmitted over encrypted connections to the
user's account. We do not sell this data or use it for advertising.
```

**Do you request data in the background?** Yes — background sync keeps the
account current after the user grants permission.

**Privacy policy URL** (must be publicly reachable and mention Health Connect):
```
https://foreverbetter.xyz/privacy
```
> ⚠️ Two issues found in `website/src/app/privacy/page.tsx`:
> 1. The page's canonical/OG domain is `betterforever.xyz` and the contact is
>    `privacy@betterforever.xyz` — inconsistent with `foreverbetter.xyz`. Confirm
>    which domain is live and that `/privacy` actually resolves there.
> 2. The current text covers biomarkers, genomics, and payments but says nothing
>    about **Health Connect, wearable sync, or the ForeverBetter Connect app**.
>    Google requires the policy to disclose Health Connect data handling,
>    retention, and deletion. Add a section before submitting. Draft:
> ```
> ForeverBetter Connect (Android)
> The ForeverBetter Connect app reads health and fitness data from Android
> Health Connect that you explicitly authorize (activity, heart, sleep, body,
> and related metrics) and syncs it to your ForeverBetter account. Access is
> permission-gated and user-initiated. Data is transmitted over encrypted
> connections, is never sold, and is never used for advertising. You can stop
> syncing or disconnect at any time in the app or in Health Connect settings,
> and request deletion at privacy@foreverbetter.xyz.
> ```

---

## 4. Data Safety

**Does your app collect or share user data?** Yes.

**Is data encrypted in transit?** Yes.
**Can users request data deletion?** Yes — via disconnect/stop-sync in-app and
by contacting `james@foreverbetter.xyz`.

**Data types collected** (all under "Health and fitness" + "Personal info"):

| Category | Type | Collected | Shared | Purpose |
|---|---|---|---|---|
| Health & fitness | Health info (activity, heart, body, sleep, glucose, blood pressure, nutrition, reproductive, workouts) | Yes | No | App functionality |
| Personal info | User IDs | Yes | No | App functionality, account management |
| App activity | Diagnostics / crash logs (Sentry) | Yes | No | Crash reporting, app stability |

**For each health type**: Collected = Yes, Shared = No, Processed ephemerally =
No (it is synced/stored to the account), Required (not optional) = user chooses
per Health Connect permission, Purpose = App functionality.

> Diagnostics: the app bundles Sentry crash reporting (`sentry.mntm.dev`).
> Declare "Crash logs" and "Diagnostics" under App activity, purpose = App
> stability / crash reporting.

---

## 5. Content Rating (questionnaire)

- Category: **Health & Fitness / Utility** (not a game).
- Violence, sexual content, profanity, controlled substances: **No** to all.
- User-generated content / social features: **No**.
- Does the app share user location: **No**.
- Expected result: rated **Everyone / PEGI 3**.
> Note: the reproductive-health data types are health metrics, not sexual
> content — answer the "sexual content" questions No.

---

## 6. Target Audience and Content

- **Target age group**: 18 and over (health data app; avoid the child/mixed-age
  compliance burden).
- **Appeals to children?** No.
- **Store presence directed at families?** No.

---

## 7. Ads

- **Does your app contain ads?** No.

---

## 8. Countries / Regions

- Select target markets. Portugal + EU + US at minimum, or "All countries" if
  you want the widest reach. (You decide distribution.)

---

## Status checklist

Resolved from repo analysis:
- ✅ **Host URL**: `https://fb-health-api.fly.dev` (from `fly.toml`).
- ✅ **Login flow**: app switched to email OTP; rebuilt as versionCode 3, on internal track.
- ✅ **Reviewer sign-in**: bypass deployed + verified in prod. Creds in §2
  (`play-review@foreverbetter.xyz` / `520813`).
- ✅ **Store graphics**: icon, feature graphic, 3 screenshots generated in
  `docs/play-assets/`.
- ✅ **Store listing copy**: written above.
- ✅ **Health Connect data types**: enumerated from `lib/health_data_type.dart`.

Still needs your input / a code change:
1. **Privacy policy** — fix the `betterforever.xyz` vs `foreverbetter.xyz` domain
   mismatch and add the Health Connect section (draft provided in §3).
2. **Real screenshots** (optional but preferred) once you sign in with the
   reviewer credentials on a device.

## Two blockers unrelated to forms
- **New personal Play account**: Google may require a **closed test with 12+
  testers for 14 days** before granting production access. If your account is
  new/personal, do the closed test first. (`docs/google-play-release.md:110`
  already flags this.)
- **Service-account 48h hold**: brand-new API service accounts can't push to
  production for ~48h. Both of these are separate from the forms above.
