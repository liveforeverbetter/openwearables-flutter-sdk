#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
example_dir="$repo_root/example"

cd "$example_dir"
flutter pub get
flutter test
flutter build appbundle --release

echo "Android App Bundle:"
echo "$example_dir/build/app/outputs/bundle/release/app-release.aab"
