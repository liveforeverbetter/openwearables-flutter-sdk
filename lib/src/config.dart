/// Configuration for the OpenWearablesHealthSdk plugin.
class OpenWearablesHealthSdkConfig {
  const OpenWearablesHealthSdkConfig({this.host = defaultHost});

  /// The default host used when none is provided to `configure()`.
  ///
  /// This is the hosted ForeverBetter health API. Apps built on ForeverBetter
  /// do not need to pass a host; point elsewhere only for self-hosted or
  /// custom OpenWearables backends.
  static const String defaultHost = 'https://api.foreverbetter.xyz';

  /// The host URL for the API (e.g. `https://api.example.com`).
  ///
  /// Only the host part — the SDK appends `/api/v1/...` paths automatically.
  final String host;

  @override
  String toString() => 'OpenWearablesHealthSdkConfig(host: $host)';
}
