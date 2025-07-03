import { Controller, Post, Body, Param } from '@nestjs/common';
import { CartService } from './cart.service';
import { AddItemToCartDto } from './dto/add-item-to-cart.dto';

@Controller('cart')
export class CartController {
  constructor(private readonly cartService: CartService) {}

  @Post(':userId/items')
  addItemToCart(@Param('userId') userId: number, @Body() addItemToCartDto: AddItemToCartDto) {
    return this.cartService.addItemToCart(userId, addItemToCartDto);
  }
}
