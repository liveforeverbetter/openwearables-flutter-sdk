#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
android_dir="$repo_root/example/android"
keystore_path="${ANDROID_KEYSTORE_PATH:-$android_dir/upload-keystore.jks}"
key_properties_path="$android_dir/key.properties"
key_alias="${ANDROID_KEY_ALIAS:-foreverbetter-upload}"

if [[ -e "$keystore_path" ]]; then
  echo "Keystore already exists: $keystore_path"
  echo "Leaving existing key unchanged."
  exit 0
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

if [[ -n "${ANDROID_KEYSTORE_PASSWORD:-}" ]]; then
  store_password="$ANDROID_KEYSTORE_PASSWORD"
elif command -v openssl >/dev/null 2>&1; then
  store_password="$(openssl rand -base64 32 | tr -d '=+/[:space:]' | cut -c1-32)"
else
  store_password="$(python3 - <<'PY'
import secrets
import string

alphabet = string.ascii_letters + string.digits
print(''.join(secrets.choice(alphabet) for _ in range(32)))
PY
)"
fi
key_password="${ANDROID_KEY_PASSWORD:-$store_password}"

umask 077
"$keytool_bin" -genkeypair \
  -v \
  -keystore "$keystore_path" \
  -storepass "$store_password" \
  -keypass "$key_password" \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias "$key_alias" \
  -dname "CN=ForeverBetter, OU=Engineering, O=ForeverBetter, L=Lisbon, ST=Lisbon, C=PT" \
  -noprompt

cat >"$key_properties_path" <<EOF
storePassword=$store_password
keyPassword=$key_password
keyAlias=$key_alias
storeFile=$keystore_path
EOF

echo "Created upload keystore: $keystore_path"
echo "Created local signing config: $key_properties_path"
echo "These files are ignored by Git. Back them up securely before uploading a Play release."
