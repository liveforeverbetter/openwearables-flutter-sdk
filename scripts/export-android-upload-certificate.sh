#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
android_dir="$repo_root/example/android"
key_properties_path="$android_dir/key.properties"
certificate_path="$android_dir/upload-certificate.pem"

if [[ ! -f "$key_properties_path" ]]; then
  echo "Missing $key_properties_path. Run scripts/create-android-upload-key.sh first." >&2
  exit 1
fi

if [[ -n "${JAVA_HOME:-}" && -x "$JAVA_HOME/bin/keytool" ]]; then
  keytool_bin="$JAVA_HOME/bin/keytool"
elif [[ -x "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home/bin/keytool" ]]; then
  keytool_bin="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home/bin/keytool"
elif [[ -x "/opt/homebrew/opt/openjdk/bin/keytool" ]]; then
  keytool_bin="/opt/homebrew/opt/openjdk/bin/keytool"
elif command -v keytool >/dev/null 2>&1; then
  keytool_bin="$(command -v keytool)"
else
  echo "keytool is required. Install a JDK, then rerun this script." >&2
  exit 1
fi

store_file=""
store_password=""
key_alias=""

while IFS='=' read -r key value; do
  case "$key" in
    storeFile) store_file="$value" ;;
    storePassword) store_password="$value" ;;
    keyAlias) key_alias="$value" ;;
  esac
done < "$key_properties_path"

if [[ -z "$store_file" || -z "$store_password" || -z "$key_alias" ]]; then
  echo "key.properties must include storeFile, storePassword, and keyAlias." >&2
  exit 1
fi

"$keytool_bin" -export \
  -rfc \
  -keystore "$store_file" \
  -storepass "$store_password" \
  -alias "$key_alias" \
  -file "$certificate_path" >/dev/null

echo "Exported upload certificate: $certificate_path"
echo
"$keytool_bin" -list \
  -v \
  -keystore "$store_file" \
  -storepass "$store_password" \
  -alias "$key_alias" |
  sed -n '/Alias name:/p;/Owner:/p;/Valid from:/p;/SHA1:/p;/SHA256:/p'
