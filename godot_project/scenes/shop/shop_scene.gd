extends Control

var shop_id: String = ""
var shop_data: Dictionary = {}
var shop_items: Array = []
var selected_item_index: int = -1
var sell_mode: bool = false

@onready var shop_name_label: Label = $Background/VBoxContainer/ShopNameLabel
@onready var item_list: ItemList = $Background/VBoxContainer/ContentRow/ItemListContainer/ItemList
@onready var gil_label: Label = $Background/VBoxContainer/ContentRow/PlayerInfoContainer/GilLabel
@onready var description_label: Label = $Background/VBoxContainer/ContentRow/PlayerInfoContainer/DescriptionLabel
@onready var item_description_label: Label = $Background/VBoxContainer/ItemDescriptionLabel
@onready var buy_button: Button = $Background/VBoxContainer/ButtonRow/BuyButton
@onready var sell_button: Button = $Background/VBoxContainer/ButtonRow/SellButton
@onready var exit_button: Button = $Background/VBoxContainer/ButtonRow/ExitButton


func _ready() -> void:
	buy_button.pressed.connect(_on_buy_pressed)
	sell_button.pressed.connect(_on_sell_pressed)
	exit_button.pressed.connect(_on_exit_pressed)
	item_list.item_selected.connect(_on_item_selected)

	if shop_id != "":
		_load_shop(shop_id)
	_refresh_gil()


func setup(id: String) -> void:
	shop_id = id
	if is_inside_tree():
		_load_shop(shop_id)


func _load_shop(id: String) -> void:
	if not ShopDatabase:
		push_warning("ShopDatabase autoload not found.")
		return
	shop_data = ShopDatabase.get_shop(id)
	if shop_data.is_empty():
		push_warning("Shop not found: " + id)
		return
	shop_name_label.text = shop_data.get("name", "Shop")
	shop_items = shop_data.get("items", [])
	_populate_item_list()


func _populate_item_list() -> void:
	item_list.clear()
	selected_item_index = -1
	item_description_label.text = ""
	description_label.text = "Select an item."

	if sell_mode:
		var inventory: Array = []
		if GameManager:
			inventory = GameManager.get_inventory()
		for entry in inventory:
			var item_name: String = entry.get("name", "???")
			var sell_price: int = int(entry.get("price", 0) * 0.5)
			item_list.add_item("%s  [%d G]" % [item_name, sell_price])
	else:
		for item in shop_items:
			var item_name: String = item.get("name", "???")
			var price: int = item.get("price", 0)
			item_list.add_item("%s  [%d G]" % [item_name, price])


func _refresh_gil() -> void:
	var gil: int = 0
	if GameManager:
		gil = GameManager.get_gil()
	gil_label.text = "Gil: %d" % gil


func _on_item_selected(index: int) -> void:
	selected_item_index = index
	var desc: String = ""
	if sell_mode:
		var inventory: Array = GameManager.get_inventory() if GameManager else []
		if index < inventory.size():
			desc = inventory[index].get("description", "")
	else:
		if index < shop_items.size():
			desc = shop_items[index].get("description", "")
	description_label.text = desc if desc != "" else "No description."
	item_description_label.text = desc


func _on_buy_pressed() -> void:
	if sell_mode:
		sell_mode = false
		buy_button.text = "Buy"
		sell_button.text = "Sell"
		_populate_item_list()
		return

	if selected_item_index < 0 or selected_item_index >= shop_items.size():
		return

	var item: Dictionary = shop_items[selected_item_index]
	var price: int = item.get("price", 0)
	var current_gil: int = GameManager.get_gil() if GameManager else 0

	if current_gil < price:
		description_label.text = "Not enough Gil!"
		return

	if GameManager:
		GameManager.spend_gil(price)
		GameManager.add_item(item)
	_refresh_gil()
	description_label.text = "Purchased %s." % item.get("name", "item")


func _on_sell_pressed() -> void:
	sell_mode = not sell_mode
	if sell_mode:
		buy_button.text = "Cancel"
		sell_button.text = "Confirm Sell"
		_populate_item_list()
	else:
		# Confirm sell
		if selected_item_index >= 0:
			var inventory: Array = GameManager.get_inventory() if GameManager else []
			if selected_item_index < inventory.size():
				var item: Dictionary = inventory[selected_item_index]
				var sell_price: int = int(item.get("price", 0) * 0.5)
				if GameManager:
					GameManager.gain_gil(sell_price)
					GameManager.remove_item_at(selected_item_index)
				_refresh_gil()
				description_label.text = "Sold for %d Gil." % sell_price
		sell_mode = false
		buy_button.text = "Buy"
		sell_button.text = "Sell"
		_populate_item_list()


func _on_exit_pressed() -> void:
	SceneTransition.back()
