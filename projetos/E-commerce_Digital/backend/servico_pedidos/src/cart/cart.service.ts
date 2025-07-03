import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Cart } from './entities/cart.entity';
import { CartItem } from './entities/cart-item.entity';
import { AddItemToCartDto } from './dto/add-item-to-cart.dto';

@Injectable()
export class CartService {
  constructor(
    @InjectRepository(Cart)
    private cartRepository: Repository<Cart>,
    @InjectRepository(CartItem)
    private cartItemRepository: Repository<CartItem>,
  ) {}

  async addItemToCart(userId: number, addItemToCartDto: AddItemToCartDto): Promise<Cart> {
    let cart = await this.cartRepository.findOne({ where: { userId }, relations: ['items'] });

    if (!cart) {
      cart = this.cartRepository.create({ userId });
      await this.cartRepository.save(cart);
    }

    const existingItem = cart.items.find(item => item.productId === addItemToCartDto.productId);

    if (existingItem) {
      existingItem.quantity += addItemToCartDto.quantity;
      await this.cartItemRepository.save(existingItem);
    } else {
      const newItem = this.cartItemRepository.create({ ...addItemToCartDto, cart });
      await this.cartItemRepository.save(newItem);
      cart.items.push(newItem);
    }

    return cart;
  }
}
