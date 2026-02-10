"""
Shop System
Handles buying and selling items, equipment, and magic spells
"""

from data.items import ITEMS
from data.equipment import EQUIPMENT
from data.spells import SPELLS

class ShopSystem:
    """Manages shop transactions"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_shop = None
        self.shop_inventory = []

    def open_shop(self, shop_id):
        """
        Open shop

        Args:
            shop_id: Shop identifier

        Returns:
            dict: Shop data
        """
        from data.shops import SHOPS

        shop = SHOPS.get(shop_id)
        if not shop:
            return None

        self.current_shop = shop
        self.shop_inventory = self.get_shop_inventory(shop)

        return shop

    def get_shop_inventory(self, shop):
        """
        Get shop inventory

        Args:
            shop: Shop data

        Returns:
            list: Inventory items
        """
        inventory = []
        shop_type = shop.get('type')

        # Item shop
        if shop_type == 'item':
            for item_id in shop.get('items', []):
                item_data = ITEMS.get(item_id)
                if item_data:
                    inventory.append({
                        'id': item_id,
                        'name': item_data['name'],
                        'price': item_data['price'],
                        'type': 'item',
                        'description': item_data['description']
                    })

        # Weapon/Armor shop
        elif shop_type == 'equipment':
            for equip_id in shop.get('equipment', []):
                equip_data = EQUIPMENT.get(equip_id)
                if equip_data:
                    inventory.append({
                        'id': equip_id,
                        'name': equip_data['name'],
                        'price': equip_data['price'],
                        'type': 'equipment',
                        'equipment_type': equip_data['type'],
                        'description': equip_data.get('description', ''),
                        'stats': equip_data.get('stats', {})
                    })

        # Magic shop
        elif shop_type == 'magic':
            for spell_id in shop.get('spells', []):
                spell_data = SPELLS.get(spell_id)
                if spell_data:
                    # Price based on spell level
                    price = spell_data['level'] * 100

                    inventory.append({
                        'id': spell_id,
                        'name': spell_data['name'],
                        'price': price,
                        'type': 'spell',
                        'level': spell_data['level'],
                        'description': spell_data.get('description', '')
                    })

        # General shop (mixed)
        elif shop_type == 'general':
            # Add items
            for item_id in shop.get('items', []):
                item_data = ITEMS.get(item_id)
                if item_data:
                    inventory.append({
                        'id': item_id,
                        'name': item_data['name'],
                        'price': item_data['price'],
                        'type': 'item'
                    })

            # Add equipment
            for equip_id in shop.get('equipment', []):
                equip_data = EQUIPMENT.get(equip_id)
                if equip_data:
                    inventory.append({
                        'id': equip_id,
                        'name': equip_data['name'],
                        'price': equip_data['price'],
                        'type': 'equipment'
                    })

        return inventory

    def buy_item(self, item_id, quantity=1):
        """
        Buy item from shop

        Args:
            item_id: Item identifier
            quantity: Quantity to buy

        Returns:
            dict: Transaction result
        """
        # Find item in shop inventory
        shop_item = None
        for item in self.shop_inventory:
            if item['id'] == item_id:
                shop_item = item
                break

        if not shop_item:
            return {
                'success': False,
                'error': 'Item not available'
            }

        total_cost = shop_item['price'] * quantity

        # Check if player can afford
        if self.game_state.gil < total_cost:
            return {
                'success': False,
                'error': 'Not enough Gil',
                'cost': total_cost,
                'gil': self.game_state.gil
            }

        # Process purchase based on type
        if shop_item['type'] == 'item':
            # Add to inventory
            self.game_state.add_item_to_inventory(item_id, quantity)

        elif shop_item['type'] == 'equipment':
            # Add to equipment inventory
            if 'equipment_inventory' not in self.game_state.__dict__:
                self.game_state.equipment_inventory = {}

            if item_id not in self.game_state.equipment_inventory:
                self.game_state.equipment_inventory[item_id] = 0

            self.game_state.equipment_inventory[item_id] += quantity

        elif shop_item['type'] == 'spell':
            # Cannot buy multiple spells
            if quantity > 1:
                return {
                    'success': False,
                    'error': 'Cannot buy multiple spells'
                }

            # Must select character to learn spell
            return {
                'success': False,
                'error': 'Must select character',
                'requires_character_selection': True
            }

        # Deduct Gil
        self.game_state.gil -= total_cost

        return {
            'success': True,
            'item': shop_item,
            'quantity': quantity,
            'cost': total_cost,
            'remaining_gil': self.game_state.gil
        }

    def buy_spell_for_character(self, spell_id, char_id):
        """
        Buy spell for specific character

        Args:
            spell_id: Spell identifier
            char_id: Character identifier

        Returns:
            dict: Transaction result
        """
        from utils.level_up_system import learn_spell_from_shop

        # Find spell in shop inventory
        shop_spell = None
        for item in self.shop_inventory:
            if item['id'] == spell_id and item['type'] == 'spell':
                shop_spell = item
                break

        if not shop_spell:
            return {
                'success': False,
                'error': 'Spell not available'
            }

        # Check if character can learn this spell
        char = self.game_state.characters.get(char_id)
        if not char:
            return {
                'success': False,
                'error': 'Invalid character'
            }

        # Check if already learned
        if spell_id in char.get('learned_spells', []):
            return {
                'success': False,
                'error': 'Already learned'
            }

        # Check if can afford
        if self.game_state.gil < shop_spell['price']:
            return {
                'success': False,
                'error': 'Not enough Gil'
            }

        # Teach spell
        success = learn_spell_from_shop(self.game_state, char_id, spell_id)

        if not success:
            return {
                'success': False,
                'error': 'Character cannot learn this spell'
            }

        # Deduct Gil
        self.game_state.gil -= shop_spell['price']

        return {
            'success': True,
            'spell': shop_spell,
            'character': char_id,
            'cost': shop_spell['price'],
            'remaining_gil': self.game_state.gil
        }

    def sell_item(self, item_id, quantity=1):
        """
        Sell item to shop

        Args:
            item_id: Item identifier
            quantity: Quantity to sell

        Returns:
            dict: Transaction result
        """
        # Check if player has item
        if not self.game_state.has_item_in_inventory(item_id, quantity):
            return {
                'success': False,
                'error': 'Don\'t have item'
            }

        # Get item data
        item_data = ITEMS.get(item_id)
        if not item_data:
            return {
                'success': False,
                'error': 'Invalid item'
            }

        # Calculate sell price (50% of buy price)
        sell_price = int(item_data['price'] * 0.5) * quantity

        # Remove from inventory
        self.game_state.remove_item_from_inventory(item_id, quantity)

        # Add Gil
        self.game_state.gil += sell_price

        return {
            'success': True,
            'item_id': item_id,
            'quantity': quantity,
            'gil_earned': sell_price,
            'total_gil': self.game_state.gil
        }

    def sell_equipment(self, equip_id, quantity=1):
        """
        Sell equipment to shop

        Args:
            equip_id: Equipment identifier
            quantity: Quantity to sell

        Returns:
            dict: Transaction result
        """
        # Check if player has equipment
        if 'equipment_inventory' not in self.game_state.__dict__:
            return {
                'success': False,
                'error': 'Don\'t have equipment'
            }

        if equip_id not in self.game_state.equipment_inventory:
            return {
                'success': False,
                'error': 'Don\'t have equipment'
            }

        if self.game_state.equipment_inventory[equip_id] < quantity:
            return {
                'success': False,
                'error': 'Don\'t have enough'
            }

        # Get equipment data
        equip_data = EQUIPMENT.get(equip_id)
        if not equip_data:
            return {
                'success': False,
                'error': 'Invalid equipment'
            }

        # Calculate sell price (50% of buy price)
        sell_price = int(equip_data['price'] * 0.5) * quantity

        # Remove from inventory
        self.game_state.equipment_inventory[equip_id] -= quantity

        # Add Gil
        self.game_state.gil += sell_price

        return {
            'success': True,
            'equipment_id': equip_id,
            'quantity': quantity,
            'gil_earned': sell_price,
            'total_gil': self.game_state.gil
        }

    def can_afford(self, price):
        """
        Check if player can afford price

        Args:
            price: Price in Gil

        Returns:
            bool: Can afford
        """
        return self.game_state.gil >= price

    def get_sell_price(self, item_id, item_type='item'):
        """
        Get sell price for item

        Args:
            item_id: Item identifier
            item_type: 'item' or 'equipment'

        Returns:
            int: Sell price
        """
        if item_type == 'item':
            item_data = ITEMS.get(item_id)
            if item_data:
                return int(item_data['price'] * 0.5)

        elif item_type == 'equipment':
            equip_data = EQUIPMENT.get(equip_id)
            if equip_data:
                return int(equip_data['price'] * 0.5)

        return 0

    def close_shop(self):
        """Close current shop"""
        self.current_shop = None
        self.shop_inventory = []

    def is_shop_open(self):
        """Check if shop is open"""
        return self.current_shop is not None

    def get_buyback_items(self):
        """
        Get recently sold items for buyback

        Returns:
            list: Buyback items (not implemented yet)
        """
        # TODO: Implement buyback system
        return []
