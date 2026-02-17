extends Node
## AdManager - AdMob placeholder integration
## On mobile: shows banner at bottom if ads not removed
## On desktop: silently skips

var admob: Object = null
var banner_shown := false

func _ready() -> void:
	if GameManager.ads_removed:
		return
	if not GameManager.is_mobile:
		return
	_initialize_admob()

func _initialize_admob() -> void:
	# Check for AdMob singleton (only present when AdMob plugin is installed)
	if Engine.has_singleton("AdMob"):
		admob = Engine.get_singleton("AdMob")
		_setup_ads()
	else:
		# Plugin not installed - silently skip
		pass

func _setup_ads() -> void:
	if admob == null:
		return
	# Initialize with test IDs (replace with real IDs for production)
	var is_real := not OS.is_debug_build()
	admob.initialize("ca-app-pub-REPLACE_WITH_APP_ID", is_real)

func show_banner() -> void:
	if GameManager.ads_removed or admob == null:
		return
	if not banner_shown:
		admob.load_banner("ca-app-pub-REPLACE_WITH_BANNER_ID/REPLACE", true)
		banner_shown = true

func hide_banner() -> void:
	if admob == null:
		return
	admob.hide_banner()
	banner_shown = false

func remove_ads() -> void:
	GameManager.remove_ads()
	hide_banner()
