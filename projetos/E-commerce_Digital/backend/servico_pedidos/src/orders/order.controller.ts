import { Controller, Post, Body, Param, Get } from '@nestjs/common';
import { OrderService } from './order.service';
import { CreateOrderDto } from './dto/create-order.dto';

@Controller('orders')
export class OrderController {
  constructor(private readonly orderService: OrderService) {}

  @Post('checkout/:userId')
  checkout(@Param('userId') userId: number, @Body() createOrderDto: CreateOrderDto) {
    return this.orderService.checkout(userId, createOrderDto);
  }

  @Get()
  findAll() {
    return this.orderService.findAll();
  }
}