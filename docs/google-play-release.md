# Google Play Release Runbook

This repo publishes the Android app from the Flutter example project:

`example/`

Current planned Play identity:

- App name: `ForeverBetter Connect`
- Package name: `xyz.foreverbetter.connect`
- Developer support email: `james@foreverbetter.xyz`
- Release artifact: `example/build/app/outputs/bundle/release/app-release.aab`

Do not create the Play Console app until the package name is final. Google Play package names cannot be changed after the app is created.

## 1. Prepare Signing

Generate the local upload key:

```sh
scripts/create-android-upload-key.sh
```

This creates ignored local files:

- `example/android/upload-keystore.jks`
- `example/android/key.properties`

Back both up securely. The upload key is required for future Play releases.

Alternatively, set these environment variables before building:

```sh
export ANDROID_KEYSTORE_PATH=/absolute/path/to/upload-keystore.jks
export ANDROID_KEYSTORE_PASSWORD=...
export ANDROID_KEY_ALIAS=foreverbetter-upload
export ANDROID_KEY_PASSWORD=...
```

## 2. Build The App Bundle

```sh
scripts/build-android-release.sh
```

The signed bundle is written to:

`example/build/app/outputs/bundle/release/app-release.aab`

## 3. Create The Play Console App

In Play Console, create a new app with:

- App name: `ForeverBetter Connect`
- Default language: English
- App or game: App
- Free or paid: Free, unless pricing is already decided
- Support email: `james@foreverbetter.xyz`

Use Play App Signing when prompted, and upload the `.aab` signed by the upload key.

## 4. Complete Required Store Setup

Complete these sections before review:

- Main store listing: name, short description, full description, screenshots, app icon, feature graphic.
- App access: explain any login, invitation code, API host, or test credentials required by reviewers.
- Ads: declare no ads unless ads are added.
- Content rating.
- Target audience and content.
- Data safety.
- Privacy policy URL.
- Health apps declaration.
- Countries and regions.

## 5. Health And Data Safety Notes

This app syncs health and fitness data using the Open Wearables SDK. Treat the Play submission as a health app, not a generic utility.

In Data safety, review and declare the data types actually collected, transmitted, stored, or shared by the released app. Based on the SDK surface, likely categories include health and fitness data such as activity, heart, respiratory, body, glucose, blood pressure, nutrition, sleep, reproductive health, and workouts.

In the Health apps declaration, explain:

- The user benefit: user-authorized wearable and health data synchronization into their ForeverBetter account.
- Why each requested data type is needed.
- That access is permission-gated and user initiated.
- How users can disconnect, stop sync, and delete/export data.
- Whether any data is shared with third parties.

Avoid requesting broad health categories that are not needed for the first public release.

## 6. Testing Track

Upload first to Internal testing.

If the Play developer account is a newly created personal account, Google requires a closed test with at least 12 opted-in testers for 14 continuous days before applying for production access.

## Official References

- Flutter Android release: https://docs.flutter.dev/deployment/android
- Android app signing: https://developer.android.com/studio/publish/app-signing
- Play app setup: https://support.google.com/googleplay/android-developer/answer/9859152
- Play testing tracks: https://support.google.com/googleplay/android-developer/answer/9845334
- New personal account closed testing: https://support.google.com/googleplay/android-developer/answer/14151465
- Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- Health apps on Google Play: https://developer.android.com/health-and-fitness/health-connect/publish
